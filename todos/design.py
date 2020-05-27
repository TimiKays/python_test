'''
任务表设计：
    名称
    总时长
    剩余时长
    最近开始时间
    最近完成时间
    总完成次数
    create table tasks (0 id INTEGER primary key AUTOINCREMENT,
                        1  name text(50) NOT NULL,
                        2  totaltime INTEGER(20) NOT NULL,
                        3  resttime INTEGER(20) NOT NULL,
                        4  laststart INTEGER(30) DEFAULT NULL,
                        5  lastpause INTEGER(30) DEFAULT NULL,
                        6  lastcomplete INTEGER(30) DEFAULT NULL,
                        7  completecount INTEGER(10) DEFAULT 0,
                        8  status INTEGER(2) DEFAULT 0)

代码结构：
    主窗口
        创建控件与布局
            按钮点击事件
                add_buttonClicked
                    接收：无
                    操作：弹出小窗口，
                          用 get_data 接收信号
                    返回：无
                reset_buttonClicked
                    ？？？
        调用 create_table
        调用 get_data
        设置表格

        方法：
            table_double_clicked 双击表格
                接收：index
                操作：开启TimeTask线程，传递 self.data,row_id
                      用thread_back 接收信号
                返回：无

            thread_back
                接收：id
                操作：得到self.data对应id的剩余时间，更新单元格
                返回：无
            get_data
                接收：无
                操作：查询数据库，数据保存到self.data
                    调用 fill_table
                返回：无
            fill_table
                接收：无
                操作：清空表格保留表头
                      写入self.data到表格
                返回：无
            closeEvent 窗口关闭
                解决主窗口关闭时子窗口仍显示的问题

    子窗口 Child
        定义信号 my_singnal(str)
        创建控件与布局

        按钮点击事件
            button_commit
                判断表单合法性
                调用insert_data
                关闭窗口
            button_delete
                ？
        输入框修改事件
            同步修改剩余时间
        窗口关闭事件 closeEvent
            发送信号：'1'
        键盘事件
            按回车调用button_commit

    子线程 TimeTask
        接收 list,id
        更改list中id个数据的resttime字段，每秒-1
        发送信号 timeSignal(id)

    方法
        create_table
            接收 无
            返回 无
        insert_data
            接收 list
            返回 无

'''

