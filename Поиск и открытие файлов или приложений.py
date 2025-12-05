import os

def open_file_or_folder(name):
    # Диски для поиска
    drives = ['C:', 'D:', 'E:', 'F:', 'G:']
    
    for drive in drives:
        for root, dirs, files in os.walk(drive + '\\'):
            # Ищем папку
            if name in dirs:
                path = os.path.join(root, name)
                os.startfile(path)
                return True
            
            # Ищем файл
            for file in files:
                if name in file:
                    path = os.path.join(root, file)
                    os.startfile(path)
                    return True
    
    return False

# Использование
open_file_or_folder("ТанцыШманцы")