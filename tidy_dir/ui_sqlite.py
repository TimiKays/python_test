# -*- coding: utf-8 -*-

"""
用来实现文件去重的小工具
@author TimiKays
@version 1.0
@last edit : 2020-6-30 22:29
"""
import hashlib
import os
import sys
import time
import send2trash
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QColor, QPalette
from PyQt5.QtSql import QSqlQueryModel
from PyQt5.QtWidgets import (QWidget, QLabel,
                             QLineEdit, QApplication, QPushButton, QMainWindow, QComboBox, QTableView, QVBoxLayout,
                             QHeaderView, QHBoxLayout, qApp, QAction, QAbstractItemView)
import sqlite3


class GetRepeatedThread(QThread):
    # 使用信号和UI主线程通讯，参数是发送信号时附带参数的数据类型，可以是str、int、list等
    # 用来刷新界面元素
    finishSignal = pyqtSignal(list)

    # 带参数示例
    def __init__(self, path, parent=None):
        super(GetRepeatedThread, self).__init__(parent)
        self.path = path

    def run(self):
        ''' 重写run方法'''
        files = get_file_details(self.path)
        print('文件数目：', len(files))

        # 调用方法保存数据到数据库
        create_sql = '''
        create table files(id INTEGER primary key AUTOINCREMENT,
                file text(200) NOT NULL,
                md5 text(32) NOT NULL,
                size int(20) DEFAULT NULL,
                dir text(100) NOT NULL,
                filename text(100) NOT NULL,
                type text(10) NOT NULL)
        '''
        try:
            insert_sql = 'insert into files(file,md5,size,dir,filename,type) values (?,?,?,?,?,?)'
            save_data('files', files, create_sql, insert_sql)
        except(Exception) as e:
            print(e)

        # 查出重复的
        data = get_repeated()

        # 给主线程发送信号
        self.finishSignal.emit(list(data))
        return


# 删除文件的内部类
class DelEmptyThread(QThread):
    finishSignal = pyqtSignal(str)

    # 带参数示例
    def __init__(self, path, parent=None):
        super().__init__(parent)
        self.path = path

    def run(self):
        ''' 重写run方法'''
        msg = clean_empty_dir(self.path)

        # 给主线程发送信号
        self.finishSignal.emit(msg)
        return


# 保存数据
def save_data(table, dic, create_sql, insert_sql):
    '''参数：表名，字典，创建表的sql，插入数据的sql'''
    # 连接到数据库文件，如果文件不存在则创建
    conn = sqlite3.connect('data.db')
    # 创建游标
    cursor = conn.cursor()

    #  删除表
    cursor.execute('DROP TABLE IF EXISTS {}'.format(table))
    #  创建表、字段
    cursor.execute(create_sql)
    print('成功创建表{}'.format(table))

    # 存入数据,把列表中的字典的值转成元组，执行多条语句
    new_list = []
    for i in range(len(dic)):
        tu = tuple(dic[i].values())
        new_list.append(tu)
    # print(new_list)
    cursor.executemany(insert_sql, new_list)

    cursor.close()
    conn.commit()
    conn.close()
    print('成功写入数据')


# 取出重复数据
def get_repeated():
    # 连接到数据库文件，如果文件不存在则创建
    conn = sqlite3.connect('data.db')
    # 创建游标
    cursor = conn.cursor()

    # 查出重复的项
    sql = 'select filename,dir,size,md5,file from files where md5 in ( select md5 from files  group by md5  having count(md5) > 1) order by md5 asc,filename desc,dir asc  '
    cursor.execute(sql)
    repeated = cursor.fetchall()

    cursor.close()
    conn.commit()
    conn.close()
    print('成功获取重复项')

    # 删库跑路
    try:
        os.unlink('data.db')
        # 当remove() 中的pahtname指定为目录时,相当于调用rmdir 删除目录,
        # 当remove() 中的pathname指定问文件时,相当于调用unlink 删除文件链接
        # os.remove("data.db")
    except(Exception) as e:
        print(e)
    return repeated


def clean_empty_dir(path):
    if os.path.isdir(path):
        count = 0
        empty_dirs = []
        get_all_empty_dirs(path, empty_dirs)
        emptys = len(empty_dirs)
        while emptys > 0:
            safe_del_files(empty_dirs)
            count += emptys
            empty_dirs = []
            if os.path.exists(path):
                get_all_empty_dirs(path, empty_dirs)
                emptys = len(empty_dirs)
            else:
                break
        return '已删除该路径的下的{}个空文件夹。'.format(count)
    else:
        return '该路径不是文件夹.'


def safe_del_files(file_list):
    for filename in file_list:
        send2trash.send2trash(filename)
        # res = shell.SHFileOperation((0, shellcon.FO_DELETE, filename, None,
        #                              shellcon.FOF_SILENT | shellcon.FOF_ALLOWUNDO | shellcon.FOF_NOCONFIRMATION, None,
        #                              None))  # 删除文件到回收站
        # if not res[1]:
        #     os.system('del ' + filename)
        print('已删除到回收站：', filename)


def get_all_empty_dirs(path, list):
    # 遍历文件夹和文件
    contains = os.listdir(path)
    if len(contains) == 0:
        list.append(path)
    for f in contains:
        full_f = os.path.join(path, f)
        # 对所有的文件夹递归
        if os.path.isdir(full_f):
            get_all_empty_dirs(full_f, list)


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


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # 设置主窗口
        self.setGeometry(300, 300, 780, 550)
        self.setWindowTitle('文件去重')

        # 路径，数据
        self.path = ''
        self.data = []

        # 标签
        self.label_input = QLabel(self, text='请输入要去重的文件夹地址')

        self.label_input.adjustSize()

        # 标签
        self.label_guide = QLabel(self, text='双击文件名可打开文件，双击目录可打开文件夹')
        self.label_guide.adjustSize()

        # 单行文本框，输入文件夹地址
        self.et_path = QLineEdit(self)
        self.et_path.setText(r'F:\生活\NE 音乐')

        # 按钮
        self.commit = QPushButton("确定", self)
        self.commit.clicked.connect(self.buttonClicked)

        # 表格
        # 用成员变量传递值
        print('接收到的data', self.data)
        # 设置数据层次结构，行数，4列
        self.model = QStandardItemModel(len(self.data), 4)
        self.model.setHorizontalHeaderLabels(['文件名', '所在目录', '大小', 'md5值'])
        self.fill_table()

        # 实例化表格视图，设置模型为自定义的模型
        self.tableView = QTableView()
        self.tableView.setModel(self.model)
        # 设置只能选中一行
        # self.tableView.setSelectionMode(QAbstractItemView.SingleSelection)
        # 设置只有行选中
        self.tableView.setSelectionBehavior(QAbstractItemView.SelectRows)

        # # 水平方向，表格大小拓展到适当的尺寸(所有列自动拉伸，充满界面)
        # self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # 不可编辑
        self.tableView.setEditTriggers(QTableView.NoEditTriggers)

        self.tableView.setColumnWidth(0, 200)
        self.tableView.setColumnWidth(1, 200)
        self.tableView.setColumnWidth(2, 60)
        self.tableView.setColumnWidth(3, 100)
        # # 水平方向标签拓展剩下的窗口部分，填满表格(最后一列决定充满剩下的界面)
        self.tableView.horizontalHeader().setStretchLastSection(True)
        self.tableView.doubleClicked.connect(self.view_file)

        # 厢式布局/框布局
        # 水平盒子1，装标签
        h_box1 = QHBoxLayout()
        h_box1.addWidget(self.label_input)
        h_box1.addStretch(1)
        # 水平盒子2，装文本输入框和按钮
        h_box2 = QHBoxLayout()
        h_box2.addWidget(self.et_path)
        h_box2.addWidget(self.commit)
        # 垂直盒子
        v_box = QVBoxLayout()
        v_box.addLayout(h_box1)
        v_box.addLayout(h_box2)
        v_box.addSpacing(5)
        v_box.addWidget(self.label_guide)
        v_box.addWidget(self.tableView)
        v_box.setContentsMargins(20, 20, 20, 10)
        # v_box.addStretch(1)
        # 设置布局
        widget = QWidget()
        widget.setLayout(v_box)
        self.setCentralWidget(widget)
        # self.setLayout(v_box)
        # self.setCentralWidget(widget)
        # self.setContentsMargins(10,10,10,10)

        # 状态栏
        self.statusBar()
        self.statusBar().showMessage('Ready')

        # 添加工具栏,注意：QMainWindow 才可以有菜单栏，QWidget没有，因此上面只能采用继承QMainWIndow
        tool = self.addToolBar("File")  # 这里尝试使用QmenuBar，则此时会卡死，无法完成下面appedRow操作（猜测：可能是因为本身不允许menuBar完成这种操作）

        self.act_del = QAction("删除", self)
        self.act_del_empty = QAction('清理空文件夹', self)
        tool.addAction(self.act_del)
        tool.addAction(self.act_del_empty)
        tool.actionTriggered[QAction].connect(self.processtrigger)

        self.show()

    # 浏览文件
    def view_file(self, index):
        row = index.row()
        column = index.column()
        # 双击第一列时，打开文件
        if column == 0:
            os.system('explorer.exe /n,{}'.format(self.data[row][4]))
        # 双击第二列时，打开文件夹
        elif column == 1:
            os.system('explorer.exe /n,{}'.format(self.data[row][1]))

        print(row, column)

    # 键盘
    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.close()
        elif e.key() == Qt.Key_Return:
            print('enter')
            self.buttonClicked()
        elif e.key() == Qt.Key_Delete:
            print('delete')
            self.processtrigger(self.act_del)

    # 填充表格
    def fill_table(self):
        # 清空数据保留表头
        count = self.model.rowCount()
        print('清空表格，要删除{}行'.format(count))
        for i in range(count):
            self.model.removeRow(0)
            print('\t删除了第{}行'.format(i))

        if len(self.data) != 0:
            # 设置水平方向四个头标签文本内容

            for row in range(len(self.data)):
                for column in range(4):
                    # 写入内容
                    d = str(self.data[row][column])
                    item = QStandardItem(d)
                    # 设置每个位置的文本值
                    self.model.setItem(row, column, item)

            self.statusBar().showMessage('找到{}条'.format(len(self.data)))
            self.tableView.resizeColumnsToContents()
        else:
            self.statusBar().showMessage('"{}"路径下没有重复文件'.format(self.path))

    # 工具栏操作——批量删除、清理空文件夹
    def processtrigger(self, action):
        if action.text() == "删除":
            self.set_btn(False)
            # 获取选中的行
            # 返回结果是QModelIndex类对象，里面有row和column方法获取行列索引

            indexs = self.tableView.selectionModel().selectedRows()  # 获取被选中行

            if indexs:
                # 反转
                # 创建一个空list用于存放需要删除的行号
                r_indexs = []
                for index in indexs:
                    r_indexs.append(index.row())  # 获得需要删除的行号的list
                r_indexs.sort(key=int, reverse=True)  # 用sort方法将list进行降序排列
                print(r_indexs)

                for i in r_indexs:
                    file = self.data[i][4]
                    # 删除文件（到垃圾桶）
                    send2trash.send2trash(file)
                    print('删除了：', file)
                    # 更新表格
                    self.model.removeRow(i)
                    self.data.pop(i)
                    msg = '删除了{}个重复文件'.format(len(r_indexs))
            else:
                msg = '你没有选中任何文件哦'
            self.set_btn(True)
            self.statusBar().showMessage(msg)

        if action.text() == '清理空文件夹':
            self.path = self.et_path.text()
            msg = ('正在分析"{}"下的空文件夹...  请稍等...'.format(self.path))
            self.statusBar().showMessage(msg)

            self.th2 = DelEmptyThread(self.path)
            # 将线程th的信号finishSignal和UI主线程中的槽函数button_finish进行连接
            self.th2.finishSignal.connect(self.del_finish)
            # 启动子线程
            self.th2.start()

    # 子线程删除空文件夹后的信号接收函数
    def del_finish(self, msg):
        self.set_btn(True)
        self.statusBar().showMessage(msg)

    # 设置三个按钮状态
    def set_btn(self, falg):
        self.act_del.setEnabled(falg)
        self.act_del_empty.setEnabled(falg)
        self.commit.setEnabled(falg)

    # 按钮点击效果，分析路径，更新数据库，获取重复数据，刷新表格
    def buttonClicked(self):
        self.set_btn(False)
        # 获取输入框路径
        self.path = self.et_path.text()
        msg = ('正在分析路径：{}...  请稍等...'.format(self.path))
        self.statusBar().showMessage(msg)

        if not os.path.isdir(self.path):
            self.statusBar().showMessage(r'请输入正确的路径如：E:\图片\生活，建议从地址栏复制过来')
            return

        # 创建子线程对象
        self.th = GetRepeatedThread(self.path)
        # 将线程th的信号finishSignal和UI主线程中的槽函数button_finish进行连接
        self.th.finishSignal.connect(self.button_finish)
        # 启动子线程
        self.th.start()

    def button_finish(self, data):
        print('重复个数：', len(data))
        # print(data)
        self.data = list(data)
        self.fill_table()
        self.set_btn(True)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
