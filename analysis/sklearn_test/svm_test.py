# -*- coding: utf-8 -*-

import time
import matplotlib.pyplot as plt
import numpy as np
from sklearn.svm import SVC
import joblib
import os
from PIL import Image
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.datasets import load_digits

def load_model():
    # 加载模型
    clf = joblib.load('digits_svm.pkl')
    # Ypred = clf.predict(Xtest);
    # print(clf.score(Xtest, Ytest))
    return clf


def train_dataset():
    # 加载数据集，生成对象
    print('开始数据导入...')

    digits = load_digits()
    print('完成数据导入!')

    # 显示前10个图像
    images_and_labels = list(zip(digits.images, digits.target))
    plt.figure(figsize=(8, 6))
    for index, (image, label) in enumerate(images_and_labels[:10]):
        plt.subplot(2, 5, index + 1)
        plt.axis('off')
        plt.imshow(image, cmap='Greys_r', interpolation='nearest')
        plt.title('Digit:{}'.format(label), fontsize=20)
    plt.savefig('数据集前10个.png')

    # 分为训练集和测试集，并进行训练
    print('开始训练...')

    Xtrain, Xtest, Ytrain, Ytest = train_test_split(digits.data, digits.target, test_size=0.20, random_state=2)
    clf = SVC(gamma=0.001, C=100., probability=True)
    clf.fit(Xtrain, Ytrain)
    print('完成训练!')

    print('开始预测...')
    # 进行训练并评估模型准确度--- 0.9777777777777777
    Ypred = clf.predict(Xtest);
    print(accuracy_score(Ytest, Ypred))
    print(clf.score(Xtest, Ytest))
    print('完成预测!')

    # 预测某张图片的可能性
    # np.set_printoptions(suppress=True)   #设置输出的小数不为科学计数法
    # plt.show()
    prob = clf.predict_proba(Xtest[6].reshape(1, -1))
    print(prob)

    print('开始输出图片...')
    # 真实值和预测值对比
    fig, axes = plt.subplots(4, 4, figsize=(8, 8))
    fig.subplots_adjust(hspace=0.1, wspace=0.1)
    for i, ax in enumerate(axes.flat):
        ax.imshow(Xtest[i].reshape(8, 8), cmap=plt.cm.gray_r, interpolation='nearest')
        ax.text(0.05, 0.05, str(Ypred[i]), fontsize=32, transform=ax.transAxes,
                color='green' if Ypred[i] == Ytest[i] else 'red')
        ax.text(0.8, 0.05, str(Ytest[i]), fontsize=32, transform=ax.transAxes,
                color='black')
        ax.set_xticks([])
        ax.set_yticks([])
    plt.savefig('手写数字识别结果对比.png')
    print('完成输出图片!')
    return clf

def get_all_file(path,files,names):
    # 加载所有图片
    for f in os.listdir(path):
        if os.path.isdir(path + '/' + f):
            get_all_file(path + '/' +f,files,names)
        else:
            try:
                imf=open(path + '/' + f,'rb')
                im=Image.open(imf)
                if 'test' in path:
                    # 原来的测试图片对象，方便后面移动
                    orig.append(im)
                im=im.convert('L')
                im=im.resize((8,8),Image.ANTIALIAS)
                tmp=np.array(im)
                vec=tmp.ravel()
                files.append(vec)
                names.append(path.split('/')[-1])

            except(Exception) as e:
                print('无法用image打开：' + path + '/' + f)
                print(e)
            finally:
                imf.close()


def train_for_file():
    print('开始训练...')
    Xtrain, Xtest, Ytrain, Ytest = train_test_split(train_pics, train_labels, test_size=0.20, random_state=2)
    clf = SVC(gamma=0.001, C=100., probability=True)
    clf.fit(Xtrain, Ytrain)
    print('完成训练!')

    print('开始预测...')
    # 进行训练并评估模型准确度--- 0.9777777777777777
    Ypred = clf.predict(Xtest);
    print(accuracy_score(Ytest, Ypred))
    print(clf.score(Xtest, Ytest))
    print('完成预测!')
    return clf



def test(clf):
    # 识别图片，并把图片存到对应的文件夹中
    results=clf.predict(test_pics)
    for i in range(len(results)):
        path='handwrite_digits/results/'+results[i]
        if not os.path.exists(path):
            os.makedirs(path)
        # im=Image.fromarray(test_pics[i].reshape(8,8))
        # print(test_pics[i].reshape(8,8))
        im=orig[i]
        im.save(path+'/{}.png'.format(time.time()),"PNG")




def save_model(clf):
    # 保存模型
    joblib.dump(clf, 'digits_svm.pkl')





if __name__ == '__main__':
    start = time.time()
    # 读取模型
    clf=load_model()

    # 使用数据集训练模型——无法用真实图片测试
    # clf=train_dataset()

    # 使用其他图片训练模型
    # train_pics=[]
    # train_labels=[]
    # get_all_file('handwrite_digits/train',train_pics,train_labels)
    # clf=train_for_file()

    # 测试模型
    test_pics = []
    orig=[]
    test_labels = []
    get_all_file('handwrite_digits/test', test_pics, test_labels)
    test(clf)

    # 保存模型
    save_model(clf)
    print('程序历时：{:.2f}'.format(time.time() - start))