import os

def quick_txt(name):#сюда голосовой ввод
    path = os.path.join(os.path.expanduser("~"), "Documents", name + '.txt')
    with open(path, 'w', encoding='utf-8') as f:
        content = #сюда голосовой ввод
        f.write(content)
    return path
