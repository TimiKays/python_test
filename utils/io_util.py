import os
import hashlib

from win32comext import shell
from win32comext.shell import shellcon


def get_all_files(dir_path, files):
    '''遍历路径下的所有文件和文件夹，返回每个文件的路径'''

    # 遍历文件夹和文件
    for f in os.listdir(dir_path):
        full_f = os.path.join(dir_path, f)
        if os.path.isdir(full_f):
            # 如果是文件夹，就递归
            get_all_files(full_f, files)
        else:
            # 如果是文件，就把路径保存到files列表
            files.append(full_f)
    return files


def get_file_details(dir_path):
    urls = []
    get_all_files(dir_path, urls)
    files = []

    for file in urls:
        m = hashlib.md5()
        with open(file, 'rb') as f:
            for line in f:
                m.update(line)
        md5code = m.hexdigest()
        detail = {}
        detail['file'] = file
        detail['md5'] = md5code
        size = os.path.getsize(file)
        dir = os.path.dirname(file)
        filename = os.path.basename(file)
        type = filename.split('.')[-1]
        detail['size'] = size
        detail['dir'] = dir
        detail['filename'] = filename
        detail['type'] = type
        files.append(detail)
    return files


import send2trash


def safe_del_files(file_list):
    for filename in file_list:
        send2trash.send2trash(filename)
        # res = shell.SHFileOperation((0, shellcon.FO_DELETE, filename, None,
        #                              shellcon.FOF_SILENT | shellcon.FOF_ALLOWUNDO | shellcon.FOF_NOCONFIRMATION, None,
        #                              None))  # 删除文件到回收站
        # if not res[1]:
        #     os.system('del ' + filename)
        print('已删除到回收站：', filename)


def clean_empty_dir(path):
    if os.path.isdir(path):
        count=0
        empty_dirs = []
        get_all_empty_dirs(path, empty_dirs)
        emptys=len(empty_dirs)
        while emptys>0:
            safe_del_files(empty_dirs)
            count += emptys
            empty_dirs=[]
            if os.path.exists(path):
                get_all_empty_dirs(path, empty_dirs)
                emptys=len(empty_dirs)
            else:
                break
        return '已删除该路径的下的{}个空文件夹。'.format(count)
    else:
        return '该路径不是文件夹.'

def get_all_empty_dirs(path,list):
    # 遍历文件夹和文件
    contains=os.listdir(path)
    if len(contains)==0:
        list.append(path)
    for f in contains:
        full_f = os.path.join(path, f)
        # 对所有的文件夹递归
        if os.path.isdir(full_f):
            get_all_empty_dirs(full_f, list)
