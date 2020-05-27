

# 传入列表元素为字典的数据，存入数据库
import pymysql




def save_data(table,dic,create_sql,insert_sql):
    '''@:arg 表名:str，数据：dic  ,sql_content:创建表的字段内容  '''
    # 打开数据库连接,参数1:主机名或IP；参数2：用户名；参数3：密码；参数4：数据库名称。
    # 额外设置字符集，可防止插入中文出错
    db = pymysql.connect('localhost', 'root', '19911012', 'learn_mysql', charset='utf8')
    # 使用 cursor()方法创建一个游标对象 cursor
    cursor = db.cursor()
    print('成功连接数据库')

    # # 创建表
    cursor.execute('DROP TABLE IF EXISTS {}'.format(table))
    # 参考
    # create_sql = '''
    # CREATE TABLE files(id int(8) NOT NULL AUTO_INCREMENT,
    #     file varchar(150) NOT NULL,
    #     md5 varchar(32) NOT NULL,
    #     size decimal(20) DEFAULT NULL,
    #     dir varchar(100) NOT NULL,
    #     filename varchar(50) NOT NULL,
    #     type varchar(10) NOT NULL,
    #     PRIMARY KEY (id))ENGINE=MyISAM AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
    # '''
    cursor.execute(create_sql)
    print('成功创建表{}'.format(table))

    # 存入数据
    # 把列表中的字典的值转成元组，执行多条语句
    new_list=[]
    for i in range(len(dic)):
        tu=tuple(dic[i].values())
        new_list.append(tu)
    # print(new_list)

    # try:
    # 参考
    # insert_sql='insert into files(file,md5,size,dir,filename,type) values (%s,%s,%s,%s,%s,%s)'
    cursor.executemany(insert_sql,new_list)
    db.commit()
    print('成功写入数据库')
    # except(Exception) as e:
    #     # 发生错误时回滚
    #     print(e)
    #     db.rollback()
    #     print('写入数据错误，已回滚')

    # 关闭连接
    db.close()
    print('成功关闭数据库')

def get_repeated():
    '''@:arg 表名:str，数据：dic  ,sql_content:创建表的字段内容  '''
    # 打开数据库连接,参数1:主机名或IP；参数2：用户名；参数3：密码；参数4：数据库名称。
    # 额外设置字符集，可防止插入中文出错
    db = pymysql.connect('localhost', 'root', '19911012', 'learn_mysql', charset='utf8')
    # 使用 cursor()方法创建一个游标对象 cursor
    cursor = db.cursor()
    print('成功连接数据库')

    # 查出重复的项
    sql='select filename,dir,size,md5,file from files where md5 in ( select md5 from files  group by md5  having count(md5) > 1) order by md5 asc,filename desc,dir asc  '
    cursor.execute(sql)
    repeated=cursor.fetchall()


    # 关闭连接
    db.close()
    print('成功关闭数据库')
    return repeated