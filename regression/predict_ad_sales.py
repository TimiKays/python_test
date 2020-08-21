import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

data = pd.read_csv('Advertising.csv')
print(data.head())

# 0、使用散点图可视化特征与响应之间的关系
# 选择三个为特征，salse作为观测值。这里会生成三幅图，size表示整歌图放大的倍数，aspect应该是长宽比。
# kind='reg'，表示会添加一条最佳拟合直线和95%的置信带。
# 通过图片可以看出，TV特征和销量有比较强的线性关系，而radio弱一些，newspaper更弱。
# sns.pairplot(data,x_vars=['TV','radio','newspaper'],y_vars='sales',size=7,aspect=0.8,kind='reg')
# plt.savefig('predict_ad_sales1_散点图.png')

# 1、使用Pandas构建x（特征向量）和y(标签列)
# scikit-learn要求X是一个特征矩阵，y是一个NumPy向量。pandas构建在NumPy之上。因此，X可以是pandas的DataFrame，y可以是pandas的Series，scikit-learn可以理解这种结构。
# 创建特征列表：
feature_cols = ['TV', 'radio', 'newspaper']
# 构建特征向量 x
# 使用列表选择原始DataFrame的子集
x = data[feature_cols]
# 等价于： X = data[['TV', 'Radio', 'Newspaper']]
# 输出前5项数据，检查X类型及维度：
print(x.head())
print(type(x))
print(x.shape)
# 构建标签列 y
y = data['sales']
# 等价于y=data.sales
print(y)

# 2、构建训练集与测试集
from sklearn.model_selection import train_test_split

# random_state 伪随机数生成器。默认训练集为0.75，测试集为0.25
x_train, x_test, y_train, y_test = train_test_split(x, y, random_state=0)
print(x_train.shape)
print(x_test.shape)

# 3、sklearn的线性回归
from sklearn.linear_model import LinearRegression

linreg = LinearRegression()
linreg.fit(x_train, y_train)
print(linreg)
print(linreg.intercept_)
print(linreg.coef_)
# 把特征名称（自变量）与系数对应
zip(feature_cols, linreg.coef_)
# 线性回归结果如下：
# y=2.877 + 0.047*tv + 0.179*radio + 0.004*newspaper

# 4、预测
# 通过回归模型预测数据
y_pred = linreg.predict(x_test)
print(y_pred)
print(type(y_pred))

# 5、均方根误差 RMSE
import numpy as np
from sklearn import metrics
print(type(y_pred), type(y_test))
print(len(y_pred), len(y_test))
print(y_pred.shape, y_test.shape)
# 求出方差和的平均数，并开方
sum_mean = 0
for i in range(len(y_pred)):
    sum_mean += (y_pred[i] - y_test.values[i]) ** 2
sum_erro = np.sqrt(sum_mean / 50)
print("RMSE by hand:", sum_erro)  # 1.4

# 绘制 ROC 曲线 （受试者工作特征曲线），用来对比预测值与真实值
import matplotlib.pyplot as plt
plt.figure()
plt.plot(range(len(y_pred)),y_pred,'b',label="predict")
plt.plot(range(len(y_pred)),y_test,'r',label="test")
plt.legend(loc="upper right")                                      #显示图中的标签
plt.xlabel("the number of sales")                                   #横坐标轴
plt.ylabel('value of sales')                                        #纵坐标轴
plt.savefig('predict_ad_sales2_ROC曲线.png')                       #显示结果

