import sys
import os
import FreeCAD
import Part

def convert_fcstd_to_step(fcstd_path):
    step_path = os.path.splitext(fcstd_path)[0] + ".step"
    doc = FreeCAD.openDocument(fcstd_path)
    
    # Собираем только видимые объекты, у которых есть твердотельная геометрия (Shape)
    shapes = []
    for obj in doc.Objects:
        if hasattr(obj, "Shape") and not obj.Shape.isNull():
            # В консольном режиме ViewObject может отсутствовать, проверяем Visibility
            if getattr(obj, "Visibility", True):
                shapes.append(obj)
                
    if shapes:
        Part.export(shapes, step_path)
        print(f"[FreeCAD Hook] Успешно экспортирован: {step_path}")
    else:
        print(f"[FreeCAD Hook] Нет видимой геометрии в {fcstd_path}")
        
    FreeCAD.closeDocument(doc.Name)

# FreeCAD (freecadcmd) запускает скрипты с __name__ == имя файла,
# а не "__main__", поэтому проверка выполняется по наличию аргументов.
for file_path in sys.argv[1:]:
    if file_path.lower().endswith(".fcstd"):
        if os.path.exists(file_path):
            convert_fcstd_to_step(file_path)
        else:
            print(f"[FreeCAD Hook] Файл не найден: {file_path}")
