# -*- coding: utf-8 -*-

"""
用来实现文件去重的界面
"""
import os
import sys
import time

import send2trash
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QColor, QPalette
from PyQt5.QtSql import QSqlQueryModel
from PyQt5.QtWidgets import (QWidget, QLabel,
                             QLineEdit, QApplication, QPushButton, QMainWindow, QComboBox, QTableView, QVBoxLayout,
                             QHeaderView, QHBoxLayout, qApp, QAction, QAbstractItemView)

from utils import db_util, io_util


# class Widget(QWidget):
#
#     def __init__(self):
#         QWidget.__init__(self)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # 设置主窗口
        self.setGeometry(300, 300, 1000, 600)
        self.setWindowTitle('文件去重')

        # 路径，数据
        self.path=''
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

        self.tableView.setColumnWidth(0,200)
        self.tableView.setColumnWidth(1,200)
        self.tableView.setColumnWidth(2,60)
        self.tableView.setColumnWidth(3,100)
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
        v_box.addSpacing(5)
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
        self.act_del_empty=QAction('清理空文件夹',self)
        tool.addAction(self.act_del)
        tool.addAction(self.act_del_empty)
        tool.actionTriggered[QAction].connect(self.processtrigger)

        self.show()

    # 浏览文件
    def view_file(self,index):
        row=index.row()
        column=index.column()
        # 双击第一列时，打开文件
        if column==0:
            os.system('explorer.exe /n,{}'.format(self.data[row][4]))
        # 双击第二列时，打开文件夹
        elif column==1:
            os.system('explorer.exe /n,{}'.format(self.data[row][1]))

        print(row,column)


    # # 返回包含两个按钮的widget
    # def buttonForRow(self, id):
    #     widget = QWidget()
    #     # 查看
    #     viewBtn = QPushButton('查看')
    #     viewBtn.setProperty('row',id)
    #     viewBtn.setStyleSheet(''' text-align : center;
    #                               background-color : DarkSeaGreen;
    #                               height : 30px;
    #                               border-style: outset;
    #                               font : 13px; ''')
    #     viewBtn.clicked.connect( self.viewTable(id))
    #
    #     # 删除
    #     deleteBtn = QPushButton('删除')
    #     deleteBtn.setStyleSheet(''' text-align : center;
    #                                 background-color : LightCoral;
    #                                 height : 30px;
    #                                 border-style: outset;
    #                                 font : 13px; ''')
    #     hLayout = QHBoxLayout()
    #     hLayout.addWidget(viewBtn)
    #     hLayout.addWidget(deleteBtn)
    #     hLayout.setContentsMargins(5, 2, 5, 2)
    #     widget.setLayout(hLayout)
    #     return widget


    # 键盘
    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.close()
        elif e.key() == Qt.Key_Return:
            print('enter')
            self.buttonClicked()
        elif e.key()==Qt.Key_Delete:
            print('delete')
            self.processtrigger(self.act_del)

    # 填充表格
    def fill_table(self):
        #清空数据保留表头
        count=self.model.rowCount()
        print('清空表格，要删除{}行'.format(count))
        for i in range(count):
            self.model.removeRow(0)
            print('\t删除了第{}行'.format(i))

        if len(self.data) !=0:
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
            indexs = self.tableView.selectionModel().selectedRows()  # 获取被选中行
            # # 返回结果是QModelIndex类对象，里面有row和column方法获取行列索引
            # indexs = self.tableView.selectionModel().selection().indexes()
            if indexs:
                # 反转
                r_indexs = []  # 创建一个空list用于存放需要删除的行号
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

                    # del self.data[i]
                print('成功删除了{}个文件'.format(len(r_indexs)))
                self.statusBar().showMessage('成功删除了{}个文件'.format(len(r_indexs)))
                # self.buttonClicked()
        if action.text()=='清理空文件夹':
            self.path = self.et_path.text()
            msg=io_util.clean_empty_dir(self.path)
            self.statusBar().showMessage(msg)


    # 按钮点击效果，分析路径，更新数据库，获取重复数据，刷新表格
    def buttonClicked(self):
        # 获取输入框路径
        self.path = self.et_path.text()
        self.statusBar().showMessage('正在分析路径：{}'.format(self.path))
        if not os.path.isdir(self.path):
            self.statusBar().showMessage(r'请输入正确的路径如：E:\图片\生活，建议从地址栏复制过来')
            return

        # self.statusBar().showMessage(path)
        files = io_util.get_file_details(self.path)
        print('文件数目：', len(files))

        # 调用方法保存数据到数据库
        create_sql = '''
            CREATE TABLE files(id int(8) NOT NULL AUTO_INCREMENT,
                file varchar(200) NOT NULL,
                md5 varchar(32) NOT NULL,
                size int(20) DEFAULT NULL,
                dir varchar(100) NOT NULL,
                filename varchar(100) NOT NULL,
                type varchar(10) NOT NULL,
                PRIMARY KEY (id))ENGINE=MyISAM AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
            '''
        insert_sql = 'insert into files(file,md5,size,dir,filename,type) values (%s,%s,%s,%s,%s,%s)'
        db_util.save_data('files', files, create_sql, insert_sql)

        # 查出重复的
        data = db_util.get_repeated()
        print('重复个数：', len(data))
        # print(data)
        # self.fill_table(data)
        self.data = list(data)

        # self.processtrigger( QAction("更新", self))
        self.fill_table()

        # QApplication.processEvents()
        # time.sleep(1)
        # qApp.processEvents()


if __name__ == '__main__':
    # data=[['无','无','无']]
    # print('data:',data)
    # 加载界面
    app = QApplication(sys.argv)
    window = MainWindow()

    sys.exit(app.exec_())

    # 从输入框获取地址
    # path=r'F:\生活\NE 音乐\下载'
