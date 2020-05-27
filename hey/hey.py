# -*- coding: utf-8 -*-
import json
# import jieba
from sentence import Sentence


def get_sentence():
    while True:
        a = input('你：')
        if a == 'q':
            break
        s=Sentence(a)
        print(s.reply)


'''机器人输出'''
def robot_say(s):
    print('{}：{}'.format(robot['name'],s))

'''记忆'''
def write_to_history(s):
    with open('history.json','w',encoding='utf-8') as f:
        json.dump(s,f,ensure_ascii=False,sort_keys=True, indent=4)


'''初始化机器人'''
def init_robot():

    #读取机器人配置
    with open('robot.json','w',encoding='utf-8') as f:
        json.dump(robot,f,ensure_ascii=False,sort_keys=True, indent=4)

    # 读入历史
    with open('history.json','r',encoding='utf-8') as h:
        try:
            history=json.load(h)
            print(type(history))
            robot_say('再次见到你，我很高兴（q退出）')
        except:
            robot_say('第一次见到你，我很高兴~')
            write_to_history([{'init':'True'}])


if __name__ == '__main__':
    robot = {'name': 'TIMI'}

    init_robot()
    get_sentence()

    # sentence={'zd':'','z':'','zw':'','w':'','bd':'','b':''}
    # z=['你','我','他','她']