'''
项目：文件去重
1、得到指定目录下全部文件的路径、文件名，对应的Md5值、文件大小、文件类型
2、
    列出相同文件：即MD5值相同的文件，并给出按钮跳转到文件所在目录
    列出可能相同文件，即文件大小相同且文件类型相同
    列出同名文件
Python 获取文件的MD5值

'''
import os
import string
import hashlib
from utils import io_util as u
import pymysql
from utils import db_util


if __name__ == '__main__':
    path=r'F:\生活\NE 音乐\下载'
    files = u.get_file_details(path)
    print('文件数目：',len(files))

    # 调用方法保存数据
    create_sql = '''
    CREATE TABLE files(id int(8) NOT NULL AUTO_INCREMENT,
        file varchar(150) NOT NULL,
        md5 varchar(32) NOT NULL,
        size decimal(20) DEFAULT NULL,
        dir varchar(100) NOT NULL,
        filename varchar(50) NOT NULL,
        type varchar(10) NOT NULL,
        PRIMARY KEY (id))ENGINE=MyISAM AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
    '''
    insert_sql = 'insert into files(file,md5,size,dir,filename,type) values (%s,%s,%s,%s,%s,%s)'
    db_util.save_data('files',files,create_sql,insert_sql)

    #查出重复的
    repeated=db_util.get_repeated()



    # go=input('是否打开？（y/n）')
    # if go=='y':
    #     os.system('explorer.exe /n,{}'.format(paths[1]))

