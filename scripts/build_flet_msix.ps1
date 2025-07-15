param (
    [switch]$InstallAfter
)

# === Загрузка конфигурации ===
$configPath = Join-Path $PSScriptRoot "msixconfig.json"
if (-not (Test-Path $configPath)) {
    Write-Error "[ERROR] Конфигурационный файл 'msixconfig.json' не найден."
    exit 1
}

$config = Get-Content $configPath | ConvertFrom-Json

$AppName = $config.AppName
$PublisherCN = $config.PublisherCN
$Version = $config.Version
$CertPfx = Join-Path $PSScriptRoot $config.CertPfx
$CertPassword = $config.CertPassword
$IconPath = Join-Path $PSScriptRoot $config.IconPath
$ManifestFile = Join-Path $PSScriptRoot $config.ManifestFile

$BaseDir = $PSScriptRoot
$BuildDir = Join-Path $BaseDir "build/windows"
$LayoutDir = Join-Path $BaseDir "flet_msix_layout"
$MsixOutput = Join-Path $BaseDir "$AppName.msix"

# === Проверка утилит ===
function Require-Tool($name) {
    if (-not (Get-Command $name -ErrorAction SilentlyContinue)) {
        Write-Error "[ERROR] '$name' не найден. Установи его и попробуй снова."
        exit 1
    }
}

Require-Tool uv
Require-Tool flet

# === Поиск MakeAppx.exe и SignTool.exe ===
function Find-SdkTool($toolName) {
    $paths = @(
        "${env:ProgramFiles(x86)}\Windows Kits\10\bin\*\x64\$toolName.exe",
        "${env:ProgramFiles}\Windows Kits\10\bin\*\x64\$toolName.exe"
    )
    $found = Get-ChildItem -Path $paths -File -ErrorAction SilentlyContinue | Sort-Object FullName -Descending | Select-Object -First 1
    if (-not $found) {
        Write-Error "[ERROR] '$toolName.exe' не найден. Установи Windows SDK."
        exit 1
    }
    return $found.FullName
}

$MakeAppx = Find-SdkTool "MakeAppx"
$SignTool = Find-SdkTool "signtool"

# === Генерация сертификата (если нужно) ===
if (-not (Test-Path $CertPfx)) {
    Write-Host "[INFO] Создание самоподписанного сертификата..."
    $cert = New-SelfSignedCertificate `
        -Type CodeSigningCert `
        -Subject $PublisherCN `
        -CertStoreLocation "Cert:\CurrentUser\My" `
        -KeyExportPolicy Exportable `
        -KeySpec Signature `
        -HashAlgorithm sha256 `
        -NotAfter (Get-Date).AddYears(10)

    $pwd = ConvertTo-SecureString -String $CertPassword -Force -AsPlainText
    Export-PfxCertificate -Cert $cert -FilePath $CertPfx -Password $pwd

    Import-PfxCertificate -FilePath $CertPfx -CertStoreLocation "Cert:\CurrentUser\Root" -Password $pwd
    Write-Host "[INFO] Сертификат создан и импортирован в Trusted Root."
}

# === Сборка Flet-приложения ===
Write-Host "[BUILD] Сборка flet-приложения..."
Remove-Item -Recurse -Force $LayoutDir -ErrorAction SilentlyContinue
uv run flet build windows
if ($LASTEXITCODE -ne 0) {
    Write-Error "[ERROR] Flet сборка не удалась."
    exit 1
}

# === Подготовка layout ===
Write-Host "[STEP] Подготовка layout..."
New-Item -ItemType Directory -Path $LayoutDir -Force | Out-Null
Copy-Item "$BuildDir\*" -Destination $LayoutDir -Recurse -Force
Copy-Item $ManifestFile -Destination "$LayoutDir\AppxManifest.xml" -Force

if (Test-Path $IconPath) {
    Copy-Item $IconPath -Destination "$LayoutDir\logo.png" -Force
}

# === Проверка бинарника ===
$exe = Join-Path $LayoutDir "halter.exe"
if (-not (Test-Path $exe)) {
    Write-Error "[ERROR] Не найден 'halter.exe' в $LayoutDir."
    exit 1
}

# === Упаковка MSIX ===
Write-Host "[PACK] Упаковка MSIX..."
if (Test-Path $MsixOutput) { Remove-Item $MsixOutput -Force }
& "$MakeAppx" pack /d "$LayoutDir" /p "$MsixOutput"
if (-not (Test-Path $MsixOutput)) {
    Write-Error "[ERROR] MSIX не был создан."
    exit 1
}

# === Подпись ===
Write-Host "[SIGN] Подписываю .msix..."
& "$SignTool" sign /fd SHA256 /f "$CertPfx" /p "$CertPassword" "$MsixOutput"
Write-Host "[OK] Подпись завершена."

# === Установка ===
if ($InstallAfter) {
    Write-Host "[INSTALL] Установка приложения..."
    Add-AppxPackage $MsixOutput
    Write-Host "[DONE] Приложение установлено."
}

Write-Host "`n[FINISHED] MSIX-пакет создан: $MsixOutput"
