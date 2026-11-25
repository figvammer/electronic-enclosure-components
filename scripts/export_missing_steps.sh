#!/bin/sh
# Генерирует .step для всех .FCStd, у которых ещё нет одноимённого .step.
# Использование: sh scripts/export_missing_steps.sh

FREECAD_CMD="/Applications/FreeCAD.app/Contents/Resources/bin/freecadcmd"
EXPORT_SCRIPT="scripts/export_steps.py"

if [ ! -x "$FREECAD_CMD" ]; then
    echo "FreeCAD не найден: $FREECAD_CMD" >&2
    exit 1
fi

find . -name "*.FCStd" -not -path "./.git/*" | sort | while IFS= read -r fcstd; do
    step_file="${fcstd%.*}.step"
    if [ -f "$step_file" ]; then
        echo "Пропуск (STEP уже есть): $fcstd"
    else
        echo "Конвертация: $fcstd"
        "$FREECAD_CMD" "$EXPORT_SCRIPT" "$(pwd)/${fcstd#./}" 2>&1 | grep -E "\[FreeCAD Hook\]|Error|Exception" || true
    fi
done
