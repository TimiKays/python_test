#python之禅
# import this


#第三章 列表
# friends=['狗','猫','鸟']
# print('---欢迎以下朋友共进晚餐---')
# print(friends)
# print('---'+friends[0]+'无法赴约---')
# friends[0]='蝙蝠'
# print('---经修改，欢迎以下朋友共进晚餐---')
# print(friends)
# print('---有新桌子---')
# friends.insert(0,'鼠')
# friends.insert(2,'蛇')
# friends.append('虎')
# for friend in friends:
# 	print('哈喽，'+friend+'，有空来吃饭吗？')
# print('---新桌子不来了，只能留2个---')
# for de in range(4):
# 	print(friends.pop()+'，别来了。')
# for at in range(len(friends)):
# 	print(friends[at]+',仍然可以来')
# print('---假装聚会完了---')
# del friends[0]
# del friends[0]
# print(friends)

# 10-3到10-5
# name=input('请输入你的名字(输入quit退出)：')
# with open('names.txt','a') as file:
# 	while name!='quit':
# 		print('欢迎你，'+name)
# 		file.write(name+'\n')
# 		reason=input('为什么喜欢编程？')
# 		if reason=='quit':
# 			# 这里会直接结束到bye
# 			break
# 		file.write(' '+reason+'\n'+'\n')
# 		print('好了，下一个~')
# 		name=input('请输入你的名字(输入quit退出)：')
# 	print('bye~')

# 13-3 平铺的星星
import pygame
import sys
from random import randint

pygame.init()
# 设置窗口和图片以及他们的rect
screen=pygame.display.set_mode((1000,800))
pygame.display.set_caption('星星')
screen_rect=screen.get_rect()
star_img=pygame.image.load('pic/star_16.png')
star_rect=star_img.get_rect()

# 计算每行每列星星的数量
# 这里如果-1，右边就会至少留一个星星宽度的边距，如果没有-1，就不一定有这个边距。
count_star_x=int(screen_rect.width/2/star_rect.width)
count_star_y=int(screen_rect.height/2/star_rect.height)

# 嵌套循环把星星全部显示出来
for no_star_y in range(count_star_y):
    for no_star_x in range(count_star_x):
        # 让星星随机分布
        star_rect.x=star_rect.width+no_star_x*star_rect.width*2+randint(-20,20)
        star_rect.y=star_rect.height+no_star_y*star_rect.height*2+randint(-20,20)
        screen.blit(star_img,star_rect)

# 更新屏幕
while  True:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
                sys.exit()
    pygame.display.update()
