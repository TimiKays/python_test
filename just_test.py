# # import os
# # # 导入模块中的方法
# # from utils.io_util import get_all_files
# # files= get_all_files(r'F:\生活\图片(不上传到硬盘)\AM 1、美图\06、服装', [])
# # for f in files:
# #     print(os.path.getsize(f))
#
# # # 导入模块中的变量
# # import utils.size as s
# # print(s.width)
#
# from PyQt5 import QtWidgets
# from PyQt5.QtWidgets import QFileDialog, QWidget
# from PyQt5.QtCore import QFileInfo
#
#
# class MyWindow(QWidget):
#     def __init__(self):
#         super(MyWindow, self).__init__()
#         self.myButton = QtWidgets.QPushButton(self)
#         self.myButton.setObjectName("btn")
#         self.myButton.setText("按钮")
#         self.myButton.clicked.connect(self.msg)
#
#     def msg(self):
#         directory1 = QFileDialog.getExistingDirectory(self, "选择文件夹", "/")
#         print(directory1)  # 打印文件夹路径
#
#         fileName, filetype = QFileDialog.getOpenFileName(self, "选择文件", "/", "All Files (*);;Text Files (*.txt)")
#         print(fileName, filetype)  # 打印文件全部路径（包括文件名和后缀名）和文件类型
#         print(fileName)  # 打印文件全部路径（包括文件名和后缀名）
#         fileinfo = QFileInfo(fileName)
#         print(fileinfo)  # 打印与系统相关的文件信息，包括文件的名字和在文件系统中位置，文件的访问权限，是否是目录或符合链接，等等。
#         file_name = fileinfo.fileName()
#         print(file_name)  # 打印文件名和后缀名
#         file_suffix = fileinfo.suffix()
#         print(file_suffix)  # 打印文件后缀名
#         file_path = fileinfo.absolutePath()
#         print(file_path)  # 打印文件绝对路径（不包括文件名和后缀名）
#
#         files, ok1 = QFileDialog.getOpenFileNames(self, "多文件选择", "/", "所有文件 (*);;文本文件 (*.txt)")
#         print(files, ok1)  # 打印所选文件全部路径（包括文件名和后缀名）和文件类型
#
#         fileName2, ok2 = QFileDialog.getSaveFileName(self, "文件保存", "/", "图片文件 (*.png);;(*.jpeg)")
#         print(fileName2)  # 打印保存文件的全部路径（包括文件名和后缀名）
#
#
# if __name__ == "__main__":
#     import sys
#
#     app = QtWidgets.QApplication(sys.argv)
#     myshow = MyWindow()
#     myshow.show()
#     sys.exit(app.exec_())
# import os
#
#
# from utils import io_util
#
# path=r'F:\生活\NE 音乐\下载'
# print(io_util.clean_empty_dir(path))

# # io_util.safe_del_files(files)

# from win10toast import ToastNotifier
# toaster = ToastNotifier()
# toaster.show_toast(u'标题', u'收到一个通知')
#
# print(int('04'))

# l1=["a", "b"]
# l2=["a", "b"]
# print(l1==l2)
#
#
# l1=["a", "b"]
# l2=["a", "c"]
# print(l1==l2)

def get_time_detail(secs):
    day = (secs % (3600 * 24 * 354)) // (3600 * 24)
    hour = (secs % (3600 * 24)) // (3600)
    min = (secs % 3600) // 60
    sec = secs % 60
    s = ''
    if day != 0:
        s = s + str(day) + '天'

    if hour != 0:
        s = s + str(hour) + '小时'

    if min != 0:
        s = s + str(min) + '分'

    if sec != 0:
        s = s + str(sec) + '秒'
    return day, hour, min, sec,s
#
# def a(X):
#     T = X //(60 * 60 * 24)
#     S = X %(60 * 60 * 24)//(60 * 60)
#     F = X %(60 * 60)// 60
#     M = X % 60
#     return T,S,F,M
#
# print(get_time_detail(51840000))
# a=[]
# print(a[:])
import time

# t=int(time.time())
# time.sleep(3)
# t2=int(time.time())
print(get_time_detail(10006))