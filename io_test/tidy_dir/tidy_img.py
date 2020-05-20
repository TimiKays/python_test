# -*- coding: utf-8 -*-

# 程序边界：，。
# 输入：
#   存放照片的根目录
# 算法：
#   修改图片大小：
#       设置最大宽度1000，最大高度700，如果图片分辨率超过任意一个，就等比例缩小
# 输出：
#     保存图片
#       目录名称
#           有年月信息的，生成前缀：初始日期，并在after中根据年份生成目录
#           没有年月信息的，把目录名称生成前缀，并在after中生成目录
#       文件名称
#           有中文的，前缀_原文件名
#           没中文的，
#               如果有准确日期，把前缀改为准确日期，
#               前缀+序号，如2019-01-01(1).jpg
#       保存错误
#           如果保存为JPG错误，就保存为png，再错误就打印错误信息并跳过。
#


import os
from PIL import Image
import re


def resize_img(im):
    goal_width = 1000
    goal_height = 1000
    w,h=im.size
    if w>goal_width:
        new_w=goal_width
        new_h=int(h/(w/goal_width))
        im=im.resize((new_w,new_h),Image.ANTIALIAS )

    if h>goal_height:
        new_h=goal_height
        new_w=int(w/(h/goal_height))
        im=im.resize((new_w,new_h),Image.ANTIALIAS)
    return im


def save_img(im, yearpath,f,date):
    '''保存图片到指定位置，并降低图片质量'''

    # 从文件名中获取日期，没获取到就用默认日期
    m = re.search(r'20\d{2}\-?[01]\d\-?[0123]\d', f)
    if (m):
        date = m.group(0)
        if '-' not in date:
            date = date[:4] + '-' + date[4:6] + '-' + date[-2:]
    file_save_name = yearpath + '/' + date  #F:/生活/待备份照片/after/2013/2013-10-00
    # 如果有中文，就用
    if re.search(r'[\u4e00-\u9fa5]+',f):
        file_save_name=file_save_name + '_' +f
        try:
            im.save(file_save_name)
        except(Exception) as e:
            print('保存中文图片错误：',e)
    else:
        # 防止重名，在后面加上(i)
        i=0
        file_save_name=file_save_name+'.jpg'
        while True:
            if not os.path.exists(file_save_name):
                try:
                    im.save(file_save_name,'JPEG')
                    # ,quality=90 质量降低，暂时不用。
                    break
                except(Exception) as e:
                    # 如果报错，删除原来的jpg文件，重新生成Png文件
                    # print('文件保存为jpg错误:','旧文件名是',f,'新文件名是',file_save_name)

                    try:
                        os.remove(file_save_name)
                        im.save(file_save_name[:-3]+'png',"PNG",quality=80)
                        print('然而保存为png成功')
                        break
                    except:
                        print('序号图片保存为jpg和png错误:', e)
                        print('--------------------')

            i+=1
            file_save_name=yearpath + '/' + date+'({}).jpg'.format(i)




def get_allpic(path):
    '''遍历路径下的所有文件和文件夹'''
    # 从文件夹生成日期，并创建年份的文件夹
    pathname, filename = os.path.split(path)
    print(filename, '文件夹：')

    date=''
    global root
    # 在文件夹中找日期名
    match = re.match(r'^\d{4}[\u4e00-\u9fa5]\d{2}[\u4e00-\u9fa5]', filename)
    if match:
        date_str=match.group(0)
        date=date_str[:4]+'-'+date_str[5:7]+'-00'
        # 取年份用来生成文件夹
        year=date_str[:4]
        yearpath=root+'/after/'+year
    else:
        yearpath=root + '/after/'+filename
    if filename!= root.split('/')[-1] and not os.path.exists(yearpath):
        date=filename
        os.mkdir(yearpath)

    # 遍历文件夹和文件
    for f in os.listdir(path):
        if os.path.isdir(path + '/' + f):
            # 如果是文件夹，就递归
            if f == 'after':
                continue
            get_allpic(path + '/' + f)
        else:
            # 如果是图片文件，就打开图片，处理图片，重命名保存
            if((f.split('.')[-1] )in 'JPG,jpg,JPEG,png,PNG,gif'):
                try:
                    imf=open(path + '/' + f,'rb')
                    im = Image.open(imf)
                    im = resize_img(im)
                    save_img(im, yearpath,f,date)

                except(Exception) as e:
                    print('无法用image打开：'+path + '/' + f)
                    print(e)
                finally:
                    imf.close()

            else:
                # 如果是处理不了的文件，移到 F:/生活/待备份照片/after/others
                global others_path
                os.rename(path + '/' + f,others_path+'/'+f)

if __name__ == '__main__':
    root='F:/生活/待备份照片'
    # 创建目标文件夹：after和others
    others_path = root + '/' + 'after/others'
    if not os.path.exists(others_path):
        os.makedirs(others_path)

    get_allpic(root)


