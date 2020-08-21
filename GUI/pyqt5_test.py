#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Py40 PyQt5 tutorial

This program creates a skeleton of
a classic GUI application with a menubar,
toolbar, statusbar, and a central widget.

author: Jan Bodnar
website: py40.com
last edited: January 2015
"""

import sys

from PyQt5.QtCore import Qt, QStringListModel
from PyQt5.QtWidgets import QMainWindow, QTextEdit, QAction, QApplication, QVBoxLayout, QLCDNumber, QSlider, \
    QPushButton, QListView, QMessageBox, QTableView, QHeaderView
from PyQt5.QtGui import QIcon, QStandardItemModel, QStandardItem


class Example(QMainWindow):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        # # 文本输入框，设置到中心
        # textEdit = QTextEdit()
        # self.setCentralWidget(textEdit)

        # # 定义事件, QAction可以操作菜单栏,工具栏,或自定义键盘快捷键。
        # # 我们创建一个事件和一个特定的图标和一个“退出”的标签。然后,在定义该操作的快捷键。
        # # 第三行创建一个鼠标指针悬停在该菜单项上时的提示。
        # exitAction = QAction(QIcon('cat.JPG'), 'Exit', self)
        # exitAction.setShortcut('Ctrl+Q')
        # exitAction.setStatusTip('Exit application')
        # exitAction.triggered.connect(self.close)
        #
        #状态栏
        self.statusBar()
        self.statusBar().showMessage('Ready')
        #
        # #菜单栏
        # menubar = self.menuBar()
        # fileMenu = menubar.addMenu('&File')
        # fileMenu.addAction(exitAction)
        #
        # #工具栏
        # toolbar = self.addToolBar('Exit')
        # toolbar.addAction(exitAction)

        # # 滑块改变数字
        # # 数字
        # lcd = QLCDNumber(self)
        # # 滑块
        # sld = QSlider(Qt.Horizontal, self)
        # # 布局
        # vbox = QVBoxLayout()
        # vbox.addWidget(lcd)
        # vbox.addWidget(sld)
        # self.setLayout(vbox)
        # # 连接，将滚动条的valueChanged信号连接到lcd的display插槽。
        # sld.valueChanged.connect(lcd.display)

        # # 添加按钮并关联事件
        # btn1 = QPushButton("Button 1", self)
        # btn1.move(30, 50)
        # btn2 = QPushButton("Button 2", self)
        # btn2.move(150, 50)
        # btn1.clicked.connect(self.buttonClicked)
        # btn2.clicked.connect(self.buttonClicked)

        # #下拉列表
        # combo = QComboBox(self)
        # combo.addItem("Ubuntu")
        # combo.addItem("Mandriva")

        # # 列表、对话框
        # listView = QListView()  # 创建一个listview对象
        # slm = QStringListModel();  # 创建mode
        # self.qList = ['Item 1', 'Item 2', 'Item 3', 'Item 4']  # 添加的数组数据
        # slm.setStringList(self.qList)  # 将数据设置到model
        # listView.setModel(slm)  ##绑定 listView 和 model
        # listView.clicked.connect(self.clickedlist)  # listview 的点击事件
        # self.setCentralWidget(listView)

        # 表格
        # 设置数据层次结构，4行4列
        self.model = QStandardItemModel(4, 4)
        # 设置水平方向四个头标签文本内容
        self.model.setHorizontalHeaderLabels(['标题1', '标题2', '标题3', '标题4'])
        for row in range(4):
            for column in range(4):
                item = QStandardItem('row %s,column %s' % (row, column))  #就是内容
                # 设置每个位置的文本值
                self.model.setItem(row, column, item)
            # 实例化表格视图，设置模型为自定义的模型
        self.tableView = QTableView()
        self.tableView.setModel(self.model)
        # self.tableView.setGeometry(20, 60, 500, 300)
        self.setCentralWidget(self.tableView)
        # 水平方向标签拓展剩下的窗口部分，填满表格
        self.tableView.horizontalHeader().setStretchLastSection(True)
        # 水平方向，表格大小拓展到适当的尺寸
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # 设置坐标和宽高
        self.setGeometry(300, 300, 350, 250)
        self.setWindowTitle('Main window')
        self.show()

    #实现键盘按下的事件处理器
    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.close()

    # 实现按钮点击事件处理器，并告知事件发送者
    def buttonClicked(self):
        sender = self.sender()
        self.statusBar().showMessage(sender.text() + ' was pressed')

    #列表的点击事件，弹出对话框
    def clickedlist(self, qModelIndex):
        QMessageBox.information(self, "QListView", "你选择了: " + self.qList[qModelIndex.row()])
        print("点击的是：" + str(qModelIndex.row()))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    # 进入主循环
    sys.exit(app.exec_())