import matplotlib.pyplot as plt
from random import choice


def show_plot():
    """绘制折线图"""
    # 矫正图形
    input_values = [1, 2, 3, 4, 5]
    squares = [1, 4, 9, 16, 25]
    # 生成折线图
    plt.plot(input_values, squares, linewidth=3)
    # 设置标题，横竖坐标名
    plt.title("Square", fontsize=14)
    plt.xlabel("number", fontsize=12)
    plt.ylabel("result", fontsize=12)
    # 设置刻度大小
    plt.tick_params(axis='both', labelsize=12)

    plt.show()


def show_scatter():
    """绘制散点图"""
    # x_values=[1,2,3,4,5]
    x_values = list(range(1, 1001))
    # y_values=[1,4,9,16,25]
    y_values = [x ** 2 for x in x_values]
    # 指定颜色
    # plt.scatter(x_values, y_values,c=(0.9,0.6,0.8),s=1)
    # 渐变
    plt.scatter(x_values, y_values, c=y_values, cmap=plt.cm.Blues, s=1)
    # 设置标题，横竖坐标名
    plt.title("Square", fontsize=14)
    plt.xlabel("number", fontsize=12)
    plt.ylabel("result", fontsize=12)
    # 设置刻度大小
    plt.tick_params(axis='both', which='major', labelsize=12)
    # 可以显示，也可以直接保存
    # plt.show()
    plt.savefig('图2.png', box_inches='tight')


class RandomWalk():
    """随机漫步的类"""

    def __init__(self, num_points=5000):
        self.num_points = num_points
        self.x_values = [0]
        self.y_values = [0]

    def fill_walk(self):
        """随机漫步的方法"""
        while len(self.x_values) < self.num_points:
            # 计算横方向走的距离
            x_direction = choice([1, -1])
            x_distance = choice([0, 1, 2, 3, 4])
            x_step = x_direction * x_distance
            # 计算纵方向走的距离
            y_direction = choice([1, -1])
            y_distance = choice([0, 1, 2, 3, 4])
            y_step = y_direction * y_distance
            # 不允许原地踏步
            if x_step == 0 and y_step == 0:
                continue
            # 计算新坐标并追加到坐标列表里
            next_x = self.x_values[-1] + x_step
            next_y = self.y_values[-1] + y_step
            self.x_values.append(next_x)
            self.y_values.append(next_y)

			
def show_barh(li_y, li_width, y_label, title):
#使用见爬取淘宝商品案例
    # 中文的字体路径
    font = matplotlib.font_manager.FontProperties(fname='./data/SourceHanSans-Normal.otf')

    # 尺寸
    plt.figure(figsize=(8, 8))
    plt.barh(
        li_y,
        li_width,
        # color='blue',  #颜色
        # facecolor='tan',
        # edgecolor='red',  # 边缘颜色
        height=0.8,  # 高度
        tick_label=y_label,  # y轴标签
        align='center',  # 对齐
        # alpha=0.4, #透明度
    )
    # plt.yticks(index, list(df_top30_sale.word), fontproperties=font)  # y轴标签
    plt.yticks(fontproperties=font)

    # 前边设置的x、y值其实就代表了不同柱子在图形中的位置（坐标），通过for循环找到每一个x、y值的相应坐标——a、b，再使用plt.text在对应位置添文字说明来生成相应的数字标签，而for循环也保证了每一个柱子都有标签。
    # '%.0f' % b,代表标注的文字，即每个柱子对应的y值，其中0表示不显示小数后面的数值，1就表示显示小数后面一位，以此类推；
    # ha='center', va= 'bottom'代表horizontalalignment（水平对齐）、verticalalignment（垂直对齐）的方式，
    # fontsize则是文字大小。条形图、折线图也是如此设置，饼图则在pie命令中有数据标签的对应参数。对于累积柱状图、双轴柱状图则需要用两个for循环，同时通过a与b的不同加减来设置数据标签位置。
    for x, y in zip(li_width, li_y):
        plt.text(x + 0.5, y, "%.0f" % x, ha='left', va='center', fontsize=8)  # 添加数据标签
    # 标题
    plt.title(title, fontproperties=font)
    # 横轴纵轴标题
    plt.xlabel('Sales', fontsize=10)
    plt.ylabel('Words', fontsize=10)
    # 横坐标纵坐标的范围，弄高一点图形整个下移了，不弄了
    # plt.axis([0, 900000, 0, 31])
    # 去除边框
    ax=plt.subplot()
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    # ax.spines['bottom'].set_visible(False)
    # ax.spines['left'].set_visible(False)
    plt.show()

	
if __name__ == '__main__':
    # 折线图和散点图
    # show_plot()
    # show_scatter()

    # 多次随机漫步
    # while True:
    #     rw = RandomWalk()
    #     rw.fill_walk()
    #     # 设置窗口尺寸，以英寸为单位
    #     plt.figure(figsize=(10,6))
    #     #根据点数生成一个列表
    #     point_nums=list(range(rw.num_points));
    #     # 绘制。根据先后顺序渐变。s表示点的大小
    #     plt.scatter(rw.x_values, rw.y_values,c=point_nums,cmap=plt.cm.Blues, s=1)
    #     # 突出起点和终点
    #     plt.scatter(0, 0, c='green',s=20)
    #     plt.scatter(rw.x_values[-1], rw.y_values[-1], c='green',s=20)
    #     # 隐藏坐标轴
    #     plt.axes().get_xaxis().set_visible(False)
    #     plt.axes().get_yaxis().set_visible(False)
    #     plt.show()
    #     wan = input('还玩么？（y/n）')
    #     if wan == 'n':
    #         break

    # 模拟花粉运动，用折线图画
    rw_f = RandomWalk()
    rw_f.fill_walk()
    plt.plot(rw_f.x_values, rw_f.y_values)
    plt.show()
