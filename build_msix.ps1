$AppName = "FletApp"
$BuildDir = "build/windows"
$LayoutDir = "flet_msix_layout"
$ManifestFile = "AppxManifest.xml"
$MsixOutput = "FletApp.msix"

# Проверка MakeAppx.exe
$makeAppx = "${env:ProgramFiles(x86)}\Windows Kits\10\bin\10.0.22621.0\\x64\MakeAppx.exe"
if (-not (Test-Path $makeAppx)) {
    Write-Error "❌ Установи Windows SDK с MakeAppx.exe"
    exit 1
}

# Сборка Flet
Write-Host "⚙️ Сборка Flet..."
uv run flet build windows
if ($LASTEXITCODE -ne 0) {
    Write-Error "❌ Flet сборка не удалась"
    exit 1
}

# Подготовка layout
Remove-Item -Recurse -Force $LayoutDir -ErrorAction SilentlyContinue
New-Item -ItemType Directory -Path $LayoutDir | Out-Null
Copy-Item "$BuildDir\*" -Destination $LayoutDir -Recurse -Force
Copy-Item "src/assets/icon.png" -Destination "$LayoutDir\logo.png" -Force

# Проверка наличия main.exe
if (-not (Test-Path "$LayoutDir\halter.exe")) {
    Write-Error "❌ main.exe не найден в $LayoutDir."
    exit 1
}

# Копируем манифест
Copy-Item $ManifestFile -Destination "$LayoutDir\AppxManifest.xml" -Force

# Упаковка
Write-Host "Упаковка MSIX..."
& "$makeAppx" pack /d "$LayoutDir" /p "$MsixOutput"

if (Test-Path $MsixOutput) {
    Write-Host "MSIX готов: $MsixOutput"
} else {
    Write-Error "MSIX не был создан."
}

