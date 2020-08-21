import sqlite3

# 连接到数据库文件，如果文件不存在则创建
conn = sqlite3.connect('data.db')
# 创建游标
cursor = conn.cursor()
# # 执行一条语句，创建user表，如果表存在则报错。
# cursor.execute('create table home(id int(10) primary key,name varchar(20))')

# 新增数据
# for i in range(5):
#     cursor.execute('insert into home (id,name) values ({}, "张三")'.format(str(i)))

# # 查询
# # cursor.execute('select id,name from home where name="张三"')
# cursor.execute('select * from home where id>?',(1,))  #元组中的逗号不能省略，等价于id>1
# result=cursor.fetchall()
# print(result)
#
# # 修改
# cursor.execute('update home set name=? where id=?',("李四",0))

# 删除

cursor.execute('delete from home where id=4')

# 关闭
cursor.close()
# 提交事务
conn.commit()
conn.close()
