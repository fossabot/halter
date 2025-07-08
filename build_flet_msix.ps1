# build_flet_msix.ps1
# Полный билд flet-приложения в MSIX с автогенерацией и установкой сертификата

param (
    [switch]$InstallAfter
)

# === Конфигурация ===
$AppName = "FletApp"
$PublisherCN = "CN=FletDeveloper"
$Version = "1.0.0.0"
$CertName = "FletCert"
$CertPassword = "YourStrongPassword123"
$BaseDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$CertPfx = Join-Path $BaseDir "$CertName.pfx"
$LayoutDir = Join-Path $BaseDir "flet_msix_layout"
$MsixPath = Join-Path $BaseDir "$AppName.msix"

# === Проверка зависимостей ===
function Require-Tool($name) {
    if (-not (Get-Command $name -ErrorAction SilentlyContinue)) {
        Write-Error "Не найдено '$name'. Установи его и попробуй снова."
        exit 1
    }
}

Require-Tool flet
Require-Tool makeappx
Require-Tool signtool

# === Создание сертификата ===
if (-not (Test-Path $CertPfx)) {
    Write-Host "Создаю самоподписанный сертификат..."
    $cert = New-SelfSignedCertificate -Type CodeSigningCert -Subject $PublisherCN `
        -CertStoreLocation "Cert:\CurrentUser\My" -KeyExportPolicy Exportable `
        -HashAlgorithm SHA256 -KeyLength 2048

    Export-PfxCertificate -Cert $cert -FilePath $CertPfx `
        -Password (ConvertTo-SecureString $CertPassword -AsPlainText -Force)
    Write-Host "Сертификат создан: $CertPfx"
}

# === Импорт сертификата в Trusted Root (если нужно) ===
$store = New-Object System.Security.Cryptography.X509Certificates.X509Store("Root","CurrentUser")
$store.Open("ReadWrite")
$certObj = New-Object System.Security.Cryptography.X509Certificates.X509Certificate2
$certObj.Import($CertPfx, $CertPassword, [System.Security.Cryptography.X509Certificates.X509KeyStorageFlags]::PersistKeySet)

if (-not ($store.Certificates | Where-Object { $_.Thumbprint -eq $certObj.Thumbprint })) {
    Write-Host "Импортирую сертификат в Trusted Root..."
    $store.Add($certObj)
    Write-Host "Сертификат добавлен в хранилище."
}
$store.Close()

# === Сборка flet-приложения ===
Write-Host "Собираю flet-приложение..."
Remove-Item $LayoutDir -Recurse -Force -ErrorAction Ignore
uv run flet build windows

# === Создание MSIX-пакета ===
Write-Host "Создаю .msix..."
if (Test-Path $MsixPath) {
    Remove-Item $MsixPath -Force
}
makeappx pack /d $LayoutDir /p $MsixPath | Out-Null

# === Подпись пакета ===
Write-Host "Подписываю .msix..."
signtool sign /fd SHA256 /f $CertPfx /p $CertPassword $MsixPath | Out-Null
Write-Host "Подпись завершена."

# === Установка (если флаг указан) ===
if ($InstallAfter) {
    Write-Host "Устанавливаю приложение..."
    Add-AppxPackage $MsixPath
    Write-Host "Приложение установлено."
}
