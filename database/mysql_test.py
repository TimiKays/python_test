import pymysql

# 打开数据库连接,参数1:主机名或IP；参数2：用户名；参数3：密码；参数4：数据库名称。
# 额外设置字符集，可防止插入中文出错
db = pymysql.connect('localhost', 'root', '19911012', 'learn_mysql',charset='utf8')
# 使用 cursor()方法创建一个游标对象 cursor
cursor = db.cursor()
print('成功连接数据库')

# # 查询版本
# cursor.execute('SELECT VERSION()')
# # 使用 fetchone()方法获取单条数据
# data = cursor.fetchone()
# print(data)
#
# # 创建表
# cursor.execute('DROP TABLE IF EXISTS books')
# print('..')
# sql = '''
# CREATE TABLE books(
#     id int(8) NOT NULL AUTO_INCREMENT,
#     name varchar(50) NOT NULL,
#     category varchar(50) NOT NULL,
#     price decimal(10,2) DEFAULT NULL,
#     publish_time date DEFAULT NULL,
#     PRIMARY KEY (id)
# )ENGINE=MyISAM AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
# '''
# cursor.execute(sql)

# 执行多条语句
li=[('第一本书','普通','1.1','2020-6-22'),
    ('第二本书','普通','2.2','2020-6-21')]
try:
    cursor.executemany('insert into books(name,category,price,publish_time) values (%s,%s,%s,%s)',li)
    db.commit()
except(Exception) as e:
    # 发生错误时回滚
    print(e)
    print('写入数据错误，正在回滚...')
    db.rollback()

# 关闭连接
db.close()
print('成功关闭数据库')
