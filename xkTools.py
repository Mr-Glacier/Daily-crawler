# this is myself tools
import os


# 读取整个文件内容
def readFile(save_path, save_name):
    try:
        with open(save_path + save_name, mode='r', encoding='utf-8') as file:
            content = file.read()
        return content
    except Exception as e:
        print(f'{e}')


# 写文件
def writeFile(save_path, save_name, content):
    try:
        with open(save_path + save_name, mode='w', encoding='utf-8') as file:
            file.write(content)
    except Exception as e:
        print(f'{e}')


# 获取文件夹下全部的文件名称
def getFolderFileNames(save_path):
    try:
        file_names = os.listdir(save_path)
        if '.DS_Store' in file_names:
            file_names.remove('.DS_Store')
        return file_names
    except Exception as e:
        print(f'{e}')


# 按行读取文件
def readFileByLine(save_path, save_name):
    try:
        list_lin = []
        with open(save_path + save_name, mode='r', encoding='utf-8') as file:
            for line in file:
                list_lin.append(line)
        return list_lin
    except Exception as e:
        print(f'{e}')


# 创建文件夹
def createFolder(folder_path):
    try:
        if not os.path.exists(folder_path):
            os.mkdir(folder_path)
    except Exception as e:
        print(f'{e}')