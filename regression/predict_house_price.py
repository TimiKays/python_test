#需要的包
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn import datasets, linear_model

def get_data(file_name):
    data=pd.read_csv(file_name)  #读入到数据帧
    x_parameter=[]
    y_parameter=[]
    for single_square_feet,single_price_value in zip(data['square_feet'],data['price']):
        x_parameter.append([float(single_square_feet)]) #这里要转换成多个数组
        y_parameter.append(float(single_price_value))

    return x_parameter,y_parameter

def linear_model_main(x_parameter,y_parameter,predict_x):
    # 创建线性回归对象
    regr=linear_model.LinearRegression()
    # 训练模型
    regr.fit(x_parameter,y_parameter)
    # 查看拟合直线
    show_linear_line(x_parameters,y_paramaters,regr)
    # 预测值
    predict_y=regr.predict(predict_x)
    predictions={}
    # 截距
    predictions['a']=regr.intercept_
    # 系数
    predictions['b'] = regr.coef_
    # 预测值
    predictions['predicted_y'] = predict_y
    return predictions

def show_linear_line(x_parameters,y_paramaters,regr):
    plt.scatter(x_parameters,y_paramaters,color='blue')
    plt.plot(x_parameters,regr.predict(x_parameters),color='red',linewidth=4)
    # plt.xticks(())
    # plt.yticks(())
    plt.savefig('predict_house_price.png')

if __name__ == '__main__':
    x_parameters,y_paramaters=get_data('input_data.csv')
    print(x_parameters,y_paramaters)
    predictvalue=700
    predictvalue = np.array(predictvalue).reshape(1,-1)
    result=linear_model_main(x_parameters,y_paramaters,predictvalue)
    print(result)
