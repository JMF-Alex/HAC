
#!/usr/bin/env bash
set -e

cd "$(dirname "$0")"

SCRIPT="src/main.py"
EXE_NAME="HAC_Autoclicker"
ICON="src/assets/icon.ico"

python -m PyInstaller \
    --clean \
    --onefile \
    --noconsole \
    --name "$EXE_NAME" \
    --hidden-import=tkinter \
    --hidden-import=_tkinter \
    --add-data "$ICON:assets" \
    "$SCRIPT"

rm -rf build
rm -f "$EXE_NAME.spec"

echo "$EXE_NAME successfully generated!"
