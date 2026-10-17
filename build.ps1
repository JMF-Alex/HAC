$ErrorActionPreference = "Stop"
Set-Location -Path $PSScriptRoot

$Entry = "src\main.py"
$ExeName = "HAC_Autoclicker"
$Icon = "src\assets\icon.ico"

python -m PyInstaller --onefile --noconsole --name $ExeName --icon $Icon --add-data "$Icon;assets" $Entry
if ($LASTEXITCODE -ne 0) {
    Write-Host "Build failed (exit code $LASTEXITCODE)" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit $LASTEXITCODE
}

Remove-Item -Path "build" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item -Path "$ExeName.spec" -Force -ErrorAction SilentlyContinue

Write-Host "$ExeName.exe successfully generated!" -ForegroundColor Green
Read-Host "Press Enter to exit"