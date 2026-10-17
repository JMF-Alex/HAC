$ErrorActionPreference = "Stop"
Set-Location -Path $PSScriptRoot

$Entry   = "src\main.py"
$ExeName = "HAC_Autoclicker"
$Icon    = "src\assets\icon.ico"

function Wait-ForKey {
    if (-not $env:CI) {
        Read-Host "Press Enter to exit" | Out-Null
    }
}

python -m PyInstaller --onefile --noconsole --name $ExeName --icon $Icon --add-data "$Icon;assets" $Entry
if ($LASTEXITCODE -ne 0) {
    Write-Host "Build failed (exit code $LASTEXITCODE)" -ForegroundColor Red
    Wait-ForKey
    exit $LASTEXITCODE
}

Remove-Item -Path "build" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item -Path "$ExeName.spec" -Force -ErrorAction SilentlyContinue

Write-Host "$ExeName.exe successfully generated!" -ForegroundColor Green
Wait-ForKey