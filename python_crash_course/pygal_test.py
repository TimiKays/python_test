from random import randint
import pygal

class Die():
    def __init__(self,num_sides=6):
        """设置骰子的面数"""
        self.num_sides=num_sides
    def roll(self):
        """扔色子"""
        return randint(1,self.num_sides)


if __name__=='__main__':
    die=Die()

    # 掷一个骰子1000次，并把结果存储到列表中
    # results=[]
    # for i in range(1000):
    #     one_shot=die.roll()
    #     results.append(one_shot)
    # print(results)
    # # 分析结果
    # times=[]
    # for t in range(1,die.num_sides+1):
    #     times.append(results.count(t))
    # print(times)
    # # 对结果可视化
    # hist=pygal.Bar()
    # hist.title="Results of rolling one D6 1000 times."
    # hist.x_labels=['1','2','3','4','5','6']
    # hist.x_titile="Result"
    # hist.y_title="Frequency of Result"
    # hist.add('D6',times)
    # hist.render_to_file('die_visual.svg') #保存

    # 掷两个骰子1000次，并把结果相加存储到列表中
    # die2=Die()
    # results=[]
    # for i in range(1000):
    #     results.append(die.roll()+die2.roll())
    # times=[]
    # for t in range(2,die.num_sides+die2.num_sides+1):
    #     times.append(results.count(t))
    # # 对结果可视化
    # hist=pygal.Bar()
    # hist.title="Results of rolling two D6 1000 times."
    # # hist.x_labels=['2','3','4','5','6','7','8','9','10','11','12']
    # # 改成列表解析
    # hist.x_labels=[str(num) for num in range(2,die.num_sides+die2.num_sides+1)]
    # hist.x_titile="Result"
    # hist.y_title="Frequency of Result"
    # hist.add('D6+D6',times)
    # hist.render_to_file('die_visual2.svg') #保存

    # 掷两个骰子1000次，并把结果相乘存储到列表中
    die2=Die()
    results=[]
    for i in range(1000):
        results.append(die.roll()*die2.roll())
    times=[]
    for t in range(1,die.num_sides*die2.num_sides+1):
        times.append(results.count(t))
    # 对结果可视化
    hist=pygal.Bar()
    hist.title="Results of rolling two D6 1000 times."
    # 改成列表解析
    hist.x_labels=[str(num) for num in range(1,die.num_sides*die2.num_sides+1)]
    hist.x_titile="Result"
    hist.y_title="Frequency of Result"
    hist.add('乘积',times)
    hist.render_to_file('output\\die_visual3.svg') #保存