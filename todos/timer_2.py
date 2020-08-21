# -*- coding: utf-8 -*-

"""
用来实现倒计时任务管理的小工具
@author TimiKays
@version 2.0
@last edit :
@content:
    1、任务按倒计时排序
    2、凸显正在进行的任务
    3、尝试解决打包后不弹出通知的bug
    4、增加显示列：最近完成时间。把计时的算法改为根据当前时间和最近开始时间计算。
"""

import sqlite3

import os
import sys
import time
from functools import partial

from PyQt5 import QtGui
from win10toast import ToastNotifier
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import (QWidget, QLabel,
                             QLineEdit, QApplication, QPushButton, QMainWindow,QTableView, QVBoxLayout,
                             QHeaderView, QHBoxLayout, QAction, QAbstractItemView, QMessageBox,
                             QTableWidget, QTableWidgetItem)



# ------------------------------------------计时的子线程---------------------------------------------
class TimeTask(QThread):
    # 使用信号和UI主线程通讯，参数是发送信号时附带参数的数据类型，可以是str、int、list等
    timeSignal = pyqtSignal(int)

    # 带参数示例
    def __init__(self, parent=None):
        super(TimeTask, self).__init__(parent)

    def run(self):
        while (True):
            self.sleep(1)
            self.timeSignal.emit(1)


# -------------------------------------------创建数据库，表-----------------------------------------------
def create_table():
    '''参数：表名，字典，创建表的sql，插入数据的sql'''
    # 连接到数据库文件，如果文件不存在则创建
    conn = sqlite3.connect(db_path)
    # 创建游标
    cursor = conn.cursor()

    # #  删除表
    # cursor.execute('DROP TABLE IF EXISTS {}'.format(table))
    try:
        #  创建表、字段
        create_sql = '''
                create table tasks (id INTEGER primary key AUTOINCREMENT,
                        name text(50) NOT NULL,
                        totaltime INTEGER(20) NOT NULL,
                        resttime INTEGER(20) NOT NULL,
                        laststart INTEGER(30) DEFAULT NULL,
                        lastpause INTEGER(30) DEFAULT NULL,
                        lastcomplete INTEGER(30) DEFAULT NULL,
                        completecount INTEGER(10) DEFAULT 0,
                        status INTEGER(2) DEFAULT 0)
                '''
        cursor.execute(create_sql)
        print('成功创建表tasks')
    except(Exception) as e:
        print('表已存在', e)

    cursor.close()
    conn.commit()
    conn.close()


# -----------------------------------------插入数据到数据库----------------------------------------------
def insert_data(data):
    '''参数：表名，字典，创建表的sql，插入数据的sql'''
    # 连接到数据库文件，如果文件不存在则创建
    conn = sqlite3.connect(db_path)
    # 创建游标
    cursor = conn.cursor()
    cursor.execute(
        'insert into tasks(name,totaltime,resttime,laststart,lastpause,lastcomplete,completecount,status) values (?,?,?,?,?,?,?,?)',
        data)
    cursor.close()
    conn.commit()
    conn.close()


# -------------------------------------更新数据库----------------------------------------------
def update_data(update_sql):
    '''更新数据的sql'''
    # 连接到数据库文件，如果文件不存在则创建
    conn = sqlite3.connect(db_path)
    # 创建游标
    cursor = conn.cursor()
    # sql = 'update tasks set {} ={} where id={}'.format(key, value, id)
    print(update_sql)
    try:
        cursor.execute(update_sql)
    except(Exception) as e:
        print(e)

    cursor.close()
    conn.commit()
    conn.close()

# ----------------------------------------删除数据-----------------------------------
def delete_data(id):
    # 连接到数据库文件，如果文件不存在则创建
    conn = sqlite3.connect(db_path)
    # 创建游标
    cursor = conn.cursor()
    sql = 'delete from tasks where id={}'.format(id)
    print(sql)
    try:
        cursor.execute(sql)
    except(Exception) as e:
        print(e)

    cursor.close()
    conn.commit()
    conn.close()


# ---------------------------------------计算秒时间-------------------------------------
def get_time_detail(secs):

    day=(secs%(3600*24*354))//(3600*24)
    hour=(secs%(3600*24))//(3600)
    min=(secs%3600)//60
    sec=secs%60
    s = ''
    if day != 0:
        s = s +str(day) + '天'

    if hour != 0:
        s = s + str(hour) + '小时'

    if min!= 0:
        s = s + str(min) + '分'


    s = s + str(sec) + '秒'
    return day,hour,min,sec,s

# -----------------------------------------设置行颜色-----------------------------------------
def setColortoRow(table, rowIndex, bgcolor,ftcolor):


    counts=table.columnCount()-1
    for j in range(counts):
        if bgcolor != 0:
            table.item(rowIndex, j).setBackground(bgcolor)
        else:
            table.item(rowIndex, j).setBackground(QtGui.QColor(255, 255, 255))

        if ftcolor !=0:
            table.item(rowIndex, j).setForeground(ftcolor)
        else:
            table.item(rowIndex, j).setForeground(QtGui.QColor(0, 0, 0))


#  -------------------------------------------子窗口---------------------------------------------
class Child(QWidget):
    # 信号，返回0表示不用操作，返回1表示需要备份表格正在运行的数据并重新从数据库获取数据
    my_singnal = pyqtSignal(int)

    def __init__(self,data,id):
        super().__init__()
        self.data=data
        self.id=id
        self.single_data=data[id]

        self.setGeometry(400, 550, 450, 270)
        self.setWindowTitle('我是子窗口')

        #让子窗口置顶
        # self.setWindowFlags(
        #     Qt.WindowCloseButtonHint | Qt.MSWindowsFixedSizeDialogHint | Qt.Tool)
        self.setWindowModality(Qt.ApplicationModal)

        # 任务名称
        self.hint1 = QLabel(self, text='任务名称')
        self.hint1.adjustSize()
        self.et_name = QLineEdit(self, text='任务一')
        self.et_name.setMaximumWidth(280)
        self.et_name.setFocus()
        self.et_name.selectAll()

        # 总时长
        self.hint2 = QLabel(self, text='总时长')
        self.hint2.adjustSize()
        # 输入天数
        self.et_day = QLineEdit(self)
        self.et_day.setValidator(QIntValidator(0, 1000))
        self.et_day.setText('0')
        self.day = QLabel(self, text='天')
        self.day.adjustSize()
        # 输入小时数
        self.et_hour = QLineEdit(self)
        self.et_hour.setValidator(QIntValidator(0, 1000))
        self.et_hour.setText('0')
        self.hour = QLabel(self, text='小时')
        self.hour.adjustSize()
        # 输入分数
        self.et_min = QLineEdit(self)
        self.et_min.setValidator(QIntValidator(0, 1000))
        self.et_min.setText('0')
        self.min = QLabel(self, text='分')
        self.min.adjustSize()
        # 输入秒数
        self.et_sec = QLineEdit(self)
        self.et_sec.setValidator(QIntValidator(0, 1000))
        self.et_sec.setText('0')
        self.sec = QLabel(self, text='秒')
        self.sec.adjustSize()



        # 剩余时长
        self.hint3 = QLabel(self, text='剩余时长')
        self.hint3.adjustSize()
        # 输入天数
        self.et_day2 = QLineEdit(self)
        self.et_day2.setValidator(QIntValidator(0, 1000))
        self.et_day2.setText('0')
        self.day2 = QLabel(self, text='天')
        self.day2.adjustSize()
        # 输入小时数
        self.et_hour2 = QLineEdit(self)
        self.et_hour2.setValidator(QIntValidator(0, 1000))
        self.et_hour2.setText('0')
        self.hour2 = QLabel(self, text='小时')
        self.hour2.adjustSize()
        # 输入分数
        self.et_min2 = QLineEdit(self)
        self.et_min2.setValidator(QIntValidator(0, 1000))
        self.et_min2.setText('0')
        self.min2 = QLabel(self, text='分')
        self.min2.adjustSize()
        # 输入秒数
        self.et_sec2 = QLineEdit(self)
        self.et_sec2.setValidator(QIntValidator(0, 1000))
        self.et_sec2.setText('0')
        self.sec2 = QLabel(self, text='秒')
        self.sec2.adjustSize()

        # 删除按钮
        self.bt_del = QPushButton('删除', self)
        self.bt_del.clicked.connect(self.button_delete)
        # 确定按钮
        self.bt_commit = QPushButton('确定', self)
        self.bt_commit.clicked.connect(self.button_commit)

        # 填入数据
        if self.single_data!=[]:
            self.name=self.single_data[1]
            self.total_time=self.single_data[2]
            self.rest_time=self.single_data[3]
            self.et_name.setText(self.name)
            total=get_time_detail(self.total_time)
            print(total)
            self.et_day.setText(str(total[0]))
            self.et_hour.setText(str(total[1]))
            self.et_min.setText(str(total[2]))
            self.et_sec.setText(str(total[3]))

            rest=get_time_detail(self.rest_time)
            print(rest)
            self.et_day2.setText(str(rest[0]))
            self.et_hour2.setText(str(rest[1]))
            self.et_min2.setText(str(rest[2]))
            self.et_sec2.setText(str(rest[3]))
        else:
            # 关联更改
            self.et_day.textChanged.connect(self.day_changed)
            self.et_hour.textChanged.connect(self.hour_changed)
            self.et_min.textChanged.connect(self.min_changed)
            self.et_sec.textChanged.connect(self.sec_changed)
            #隐藏删除按钮
            self.bt_del.setVisible(False)

        # 厢式布局/框布局
        # 水平盒子1，装按钮
        h_box1 = QHBoxLayout()
        h_box1.addWidget(self.hint2)
        h_box1.addStretch(1)
        h_box2 = QHBoxLayout()
        h_box2.addWidget(self.et_day)
        h_box2.addWidget(self.day)
        h_box2.addSpacing(20)
        h_box2.addWidget(self.et_hour)
        h_box2.addWidget(self.hour)
        h_box2.addSpacing(20)
        h_box2.addWidget(self.et_min)
        h_box2.addWidget(self.min)
        h_box2.addSpacing(20)
        h_box2.addWidget(self.et_sec)
        h_box2.addWidget(self.sec)
        h_box3 = QHBoxLayout()
        h_box3.addWidget(self.et_day2)
        h_box3.addWidget(self.day2)
        h_box3.addSpacing(20)
        h_box3.addWidget(self.et_hour2)
        h_box3.addWidget(self.hour2)
        h_box3.addSpacing(20)
        h_box3.addWidget(self.et_min2)
        h_box3.addWidget(self.min2)
        h_box3.addSpacing(20)
        h_box3.addWidget(self.et_sec2)
        h_box3.addWidget(self.sec2)
        h_box4 = QHBoxLayout()
        h_box4.addStretch(1)
        h_box4.addWidget(self.bt_del)
        h_box4.addWidget(self.bt_commit)


        # 垂直盒子
        v_box = QVBoxLayout()
        v_box.addWidget(self.hint1)
        v_box.addWidget(self.et_name)
        v_box.addSpacing(20)
        v_box.addLayout(h_box1)
        v_box.addLayout(h_box2)
        v_box.addSpacing(20)
        v_box.addWidget(self.hint3)
        v_box.addLayout(h_box3)
        v_box.addStretch(1)
        v_box.addLayout(h_box4)
        v_box.setContentsMargins(20, 20, 20, 20)

        # 设置布局
        self.setLayout(v_box)

    def button_commit(self):
        name = self.et_name.text()
        if (name == ''):
            QMessageBox.information(self,
                                    "提交失败",
                                    "任务名称不能为空",
                                    QMessageBox.Ok,
                                    QMessageBox.Ok)
            # 如果要处理消息框返回值才要创建echo方法
            # self.echo(reply)
            return

        days = '0' if self.et_day.text() == '' else self.et_day.text()
        hours = '0' if self.et_hour.text() == '' else self.et_hour.text()
        mins = '0' if self.et_min.text() == '' else self.et_min.text()
        secs = '0' if self.et_sec.text() == '' else self.et_sec.text()
        total_time = int(secs) + int(mins) * 60 + int(hours) * 3600 + int(days) * 3600 * 24
        if (total_time == 0):
            QMessageBox.information(self, "提交失败",
                                    "总时长不能为空",
                                    QMessageBox.Ok,
                                    QMessageBox.Ok)
            return
        days2 = '0' if self.et_day2.text() == '' else self.et_day2.text()
        hours2 = '0' if self.et_hour2.text() == '' else self.et_hour2.text()
        mins2 = '0' if self.et_min2.text() == '' else self.et_min2.text()
        secs2 = '0' if self.et_sec2.text() == '' else self.et_sec2.text()
        rest_time = int(secs2) + int(mins2) * 60 + int(hours2) * 3600 + int(days2) * 3600 * 24
        if (rest_time == 0):
            QMessageBox.information(self, "提交失败",
                                    "剩余时长不能为空",
                                    QMessageBox.Ok,
                                    QMessageBox.Ok)
            return
        elif (rest_time >total_time):
            QMessageBox.information(self, "提交失败",
                                    "剩余时长不能大于总时长",
                                    QMessageBox.Ok,
                                    QMessageBox.Ok)
            return



        data = self.single_data[:]
        # 如果为空，则新建数据
        if data==[]:
            data.append(name)
            data.append(total_time)
            data.append(rest_time)
            data.append('null')
            data.append('null')
            data.append('null')
            data.append(0)
            data.append(0)
            # 更新全局数据变量
            self.data.append(data)
            # 更新数据库
            insert_data(data)
            self.my_singnal.emit(1)
        # 如果不为空，
        else:
            # 把新数据修改到列表副本中
            data[1]=name
            data[2]=total_time
            data[3]=rest_time
            # 如果列表副本等于列表，就不需要任何操作
            if data==self.single_data:
                self.my_singnal.emit(0)
            else:
                #如果不等于，更新数据库，返回信号2，更新数据
                sql = 'update tasks set name ="{}",totaltime={},resttime={} where id={}'.format(data[1],data[2],data[3],data[0])
                update_data(sql)
                self.data[self.id]=data
                self.my_singnal.emit(2)


        self.close()


    def day_changed(self, text):
        self.et_day2.setText(text)

    def hour_changed(self, text):
        self.et_hour2.setText(text)

    def min_changed(self, text):
        self.et_min2.setText(text)

    def sec_changed(self, text):
        self.et_sec2.setText(text)

    def closeEvent(self, event):
        pass

    def button_delete(self):
        # 删除确定框
        # 确认个鬼
        print('删除')

        # 删除数据库
        delete_data(self.data[self.id][0])
        # 删除数据变量
        self.data.pop(self.id)
        self.my_singnal.emit(2)
        self.close()

    # 键盘
    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Return:
            print('enter')
            self.button_commit()


# ------------------------------------主窗口-------------------------------------

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # 设置主窗口
        self.setGeometry(300, 300, 780, 550)
        self.setWindowTitle('倒计时')

        # # 路径，数据
        self.data = []

        tool = self.addToolBar('file')
        self.add=QAction('添加任务',self)
        self.about = QAction('关于', self)
        tool.addAction(self.add)
        tool.addAction(self.about)
        tool.actionTriggered[QAction].connect(self.toolbar_trigger)


        # 连接数据库、创建表tasks
        create_table()

        # 用tablewidget实现
        self.table = QTableWidget()
        self.get_data()
        # 只能选中一行
        # self.table.setSelectionMode(QAbstractItemView.SingleSelection)
        # 只有行选中
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        # 不可编辑
        self.table.setEditTriggers(QTableView.NoEditTriggers)
        # 水平方向标签拓展剩下的窗口部分，填满表格(最后一列决定充满剩下的界面)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setColumnWidth(0, 200)
        self.table.setColumnWidth(1, 60)
        self.table.setColumnWidth(2, 60)
        self.table.setColumnWidth(3, 100)
        # 双击事件
        self.table.doubleClicked.connect(self.table_double_clicked)
        # 可拖拽
        # self.table.setDragEnabled(True)

        # 更改行颜色
        # for r in range(self.table.rowCount()):
        #     setColortoRow(self.table,r,QtGui.QColor(255, 255, 255),QtGui.QColor(153,204,153))

        # 垂直盒子
        v_box = QVBoxLayout()
        v_box.addSpacing(5)
        v_box.addWidget(self.table)  # !!!这里改成了tablewidget
        v_box.setContentsMargins(20, 20, 20, 10)
        # v_box.addStretch(1)
        # 设置布局
        widget = QWidget()
        widget.setLayout(v_box)
        self.setCentralWidget(widget)

        # 状态栏
        self.statusBar()
        self.statusBar().showMessage('Ready')

        # 创建子线程对象
        self.th = TimeTask()
        # 将线程th的信号finishSignal和UI主线程中的槽函数button_finish进行连接
        self.th.timeSignal.connect(self.thread_back)
        # 启动子线程
        self.th.start()
        self.show()


    # 双击表格，开始或暂停
    def table_double_clicked(self, index):
        row = index.row()
        column = index.column()
        print('双击了表格：', row, column)

        # 变为运行：当状态为0时，改为1并开始
        if self.data[row][8] == 0:
            self.data[row][8] = 1

            self.data[row][4] = int(time.time())
            update_sql = 'update tasks set laststart ={},status={} where id={}'.format(self.data[row][4],
                                                                                       self.data[row][8],
                                                                                       self.data[row][0])
            update_data(update_sql)


        # 变为暂停：当状态为1时，改为0
        else:
            self.data[row][8] = 0
            # self.table.setItem(row, 3, QStandardItem('单击开始'))
            # 更新状态、剩余时间、lastpause
            update_sql = 'update tasks set lastpause ={},status={},resttime={} where id={}'.format(int(time.time()),
                                                                                                   self.data[row][8],
                                                                                                   self.data[row][3],
                                                                                                   self.data[row][0])
            update_data(update_sql)

        setColortoRow(self.table,row,QtGui.QColor(153,204,153),0)

    def backup_to_sql(self):
        # 保存一下正在运行的进度，并把状态改为0
        for id in range(len(self.data)):
            if self.data[id][8] == 1:
                update_sql = 'update tasks set resttime={} where id={}'.format(self.data[id][3],
                                                                               self.data[id][0])
                update_data(update_sql)

    def welcom_new(self, result):
        # 1新建，2修改，0无变化
        if result==1:
            self.backup_to_sql()
            # 填充表格
            self.get_data()
        elif result==2:
            #修改
            self.fill_table()


    # 单击表格，开始或暂停
    def table_clicked(self, index):
        row = index.row()
        column = index.column()
        print('单击了表格：', row, column)


    # 子线程的信号接收函数
    def thread_back(self, id):
        # 接收到信号后，如果状态为1，，如果restting>0,则restting-1
        for id in range(len(self.data)):

            if self.data[id][8] == 1:
                if self.data[id][3] > 0:
                    self.data[id][3] -= 1
                    d = get_time_detail(self.data[id][3])
                    # 更新UI
                    item = QTableWidgetItem(d[4])
                    self.table.setItem(id, 2, item)
                    setColortoRow(self.table, id, QtGui.QColor(153, 204, 153), 0)

                else:
                    self.data[id][3] = self.data[id][2]
                    self.data[id][6] = int(time.time())
                    self.data[id][7] += 1
                    self.data[id][8] = 0
                    # w完成一次以后,更新数据库，重新获取数据
                    update_sql = 'update tasks set resttime={},lastcomplete={},completecount={},status={} where id={}'.format(
                        self.data[id][3], self.data[id][6], self.data[id][7], self.data[id][8], self.data[id][0])
                    update_data(update_sql)
                    self.fill_table()
                    setColortoRow(self.table, id, 0, 0)
                    # 弹出通知
                    try:

                        toaster = ToastNotifier()
                        toaster.show_toast('Done!', self.data[id][1], threaded=True)
                        print('弹出通知')
                    except(Exception) as e:
                        print(e)


    # 用data填充表格
    def fill_table(self):

        self.table.setColumnCount(4)
        self.table.setRowCount(len(self.data))
        self.table.setHorizontalHeaderLabels(['任务名称', '总时长', '剩余时长', '控制'])
        # 设置列的模式为"Stretch"，在这种模式下列直接自适应显示，无法对列的宽度和高度进行设置
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        if len(self.data) != 0:
            for row in range(len(self.data)):

                for column in range(4):
                    # 最后一列
                    if column == 3:
                        self.bt_edit = QPushButton('编辑', self)
                        self.bt_reset = QPushButton('重置', self)
                        self.bt_del = QPushButton('删除', self)
                        self.bt_edit.adjustSize()
                        self.bt_reset.adjustSize()
                        self.bt_del.adjustSize()
                        # print(row)
                        self.bt_edit.clicked.connect(partial(self.bt_edit_clicked,row))
                        self.bt_reset.clicked.connect(partial(self.bt_reset_clicked,row))
                        self.bt_del.clicked.connect(partial(self.bt_del_clicked,row))

                        h_box = QHBoxLayout()
                        h_box.addWidget(self.bt_edit)
                        h_box.addWidget(self.bt_reset)
                        h_box.addWidget(self.bt_del)
                        bt_box = QWidget()
                        bt_box.setLayout(h_box)
                        bt_box.adjustSize()
                        h_box.setContentsMargins(0,0,0,0)

                        self.table.setCellWidget(row, 3, bt_box)

                    #第一列
                    elif column==0:
                        d = str(self.data[row][column + 1])
                        # 设置每个位置的文本值
                        item = QTableWidgetItem(d)
                    # 第二三列
                    else:
                        t=get_time_detail(self.data[row][column + 1])

                        item=QTableWidgetItem(t[4])
                    self.table.setItem(row, column, item)

            self.statusBar().showMessage('共有{}条任务'.format(len(self.data)))

        else:
            self.statusBar().showMessage('暂时还没有任务哦')



    def bt_edit_clicked(self,row):
        # print('点了编辑按钮', row)
        # if self.data[row][8]==0:

        self.child = Child(self.data,row)
        self.child.show()
        self.child.my_singnal.connect(self.welcom_new)


    def bt_reset_clicked(self,id):
        print('点了重置按钮',id)
        # 更新变量
        if self.data[id][8]==1:
            self.data[id][8]=0
        self.data[id][3]=self.data[id][2]
        # 更新表格
        d = get_time_detail(self.data[id][3])
        item = QTableWidgetItem(d[4])
        self.table.setItem(id, 2, item)
        # 更新数据库
        update_dql='update tasks set resttime={},status=0 where id={}'.format(self.data[id][3],self.data[id][0])
        update_data(update_dql)
        #表格变色
        setColortoRow(self.table, id, 0, 0)


    def bt_del_clicked(self,row):
        print('点了删除按钮', row)
        # 删除数据库
        delete_data(self.data[row][0])
        # 删除数据变量
        self.data.pop(row)
        self.fill_table()


    # 工具栏
    def toolbar_trigger(self,action):
        if action.text()=='添加任务':
            self.child = Child([[]],0)
            self.child.show()
            self.child.my_singnal.connect(self.welcom_new)
        elif action.text()=='关于':

            print('about')
            QMessageBox.about(self, "关于", "开发：TimiKays（微信号）\n设计：TimiKays\n版本号：v1.0\n技术路线：python3.7+pyqt5\n数据库路径：{}\t\n最后更新时间：2020-7-4".format(db_path))


    # 重置还是放到详情里
    def reset_all_buttonClicked(self):
        pass

    # 小窗口关闭时调用
    def get_data(self):

        # 从数据库读取数据
        # 连接到数据库文件，如果文件不存在则创建
        conn = sqlite3.connect(db_path)
        # 创建游标
        cursor = conn.cursor()

        # 查所有的项
        sql = 'select id,name,totaltime,resttime,laststart,lastpause,lastcomplete,completecount,status from tasks order by resttime asc '
        cursor.execute(sql)
        self.data = list(cursor.fetchall())
        print('数据', self.data)
        listdata = []
        for i in range(len(self.data)):
            listdata.append(list(self.data[i]))
        self.data = listdata
        cursor.close()
        conn.commit()
        conn.close()
        self.fill_table()

    # 解决主窗口关闭时子窗口仍显示的问题
    def closeEvent(self, event):
        # 保存一下正在运行的进度，并把状态改为0
        for id in range(len(self.data)):
            if self.data[id][8] == 1:
                update_sql = 'update tasks set resttime={},status=0 where id={}'.format(self.data[id][3],
                                                                                        self.data[id][0])
                update_data(update_sql)

        sys.exit(0)


if __name__ == '__main__':
    dir=r'D:\Program Files\timer'
    if not os.path.exists(dir):
        os.mkdir(dir)
    db_path = r'D:\Program Files\timer\data.db'
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
