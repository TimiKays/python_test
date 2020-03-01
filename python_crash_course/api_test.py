import requests
import pygal
from pygal.style import LightColorizedStyle as LCS, LightenStyle as LS

"""下载api_github.json，获取github上的项目概况"""

url = 'https://api.github.com/search/repositories?q=language:python&sort=stars'
r = requests.get(url)
print(r.status_code)
if r.status_code == 200:

    # 无法存储，这一段存储的代码无法运行，文件没写入
    # try:
    #     with open('output\\api_github.json','w') as file:
    #         file.write(r.text)
    # except UnicodeEncodeError:
    #     print('编码错误')

    # 转换成一个python字典
    response_dict = r.json()
    print('total_count:', response_dict['total_count'])

    # 获取字典中建为Items的值，存储为一个列表items
    items = response_dict['items']
    print('items_get:', len(items))

    # 从Items列表中获取第一个元素，即一个字典，一个仓库，存储为item
    names,plot_dicts = [],[]  # 用来存储名称和星星的字典的列表
    for item in items:
        # print('Keys_count:',len(item))
        # print('\n')
        names.append(item['name'])
        if item['description']:
            plot_dict = {
                'value': item['stargazers_count'],
                'label': item['description'] , #很奇怪，label后面加个空格就不报错了
                'xlink':item['html_url']
            }
        else:
            plot_dict = {
                'value': item['stargazers_count'],
                'label': 'no_description',
                'xlink':item['html_url']
            }

        plot_dicts.append(plot_dict)
    print(plot_dicts)
        # 打印信息
        # for key in sorted(item.keys()):
        #     if key in ['name','stargazers_count','html_url','created_at','updated_at','description']:
        #         print(key,': ',item[key])
        #     elif key == 'owner':
        #         print(key, ': ', item[key]['login'])

    # 可视化
    my_style = LS('#333366', base_style=LCS)
    # 方式一，通过实参的方式设置隐藏图例
    # chart=pygal.Bar(style=my_style,x_label_rotation=45,show_legend=False)

    # 方式二，通过配置文件传给Bar()来绘制条形图
    my_config = pygal.Config()
    my_config.x_label_rotation = 45  # 旋转45度
    my_config.show_legend = False  # 不显示图例
    my_config.title_font_size = 24
    my_config.label_font_size = 14
    my_config.major_label_font_size = 18  # 设置主标签字体大小，但是图表中没有变化
    my_config.truncate_label = 15  # 把较长的项目名缩短为15个字符
    my_config.show_y_guides = False  # 不显示水平线
    my_config.width = 1000

    chart = pygal.Bar(my_config, style=my_style)
    chart.title = 'Most-Starred Python Projects of Github'
    chart.x_labels = names
    # 传递一个字典，用于自定义工具提示
    chart.add('', plot_dicts)
    chart.render_to_file('output\\pyprojects_of_github2.svg')
