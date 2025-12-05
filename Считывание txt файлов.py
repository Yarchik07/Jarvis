import os

def read_txt_files(name):
    drives = ['C:', 'D:', 'E:']
    
    for drive in drives:
        for root, dirs, files in os.walk(drive + '\\'):
            for file in files:
                #содержит ли файл то что мы сказали и приписывает .txt
                if name in file and file.endswith('.txt'):
                    path = os.path.join(root, file)
                    with open(path, 'r', encoding='utf-8') as f:
                        text = f.read()
                    
                #функция работает по принципу поиска файлов