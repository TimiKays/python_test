# -*- coding: utf-8 -*-

'''
目的：CNN 识别图像（有标签）
技术路线： tensorflow
失败

猫1
狗2
'''
import os

from PIL import Image
import numpy as np
import tensorflow as tf
from tensorflow.python import arg_max, placeholder



# 从文档夹读取图片和标签到numpy数组中
# 标签信息在文档名中，例如1_40.jpg表示该图片的标签为1



def read_data(data_dir,test_data_dir):
    datas = []
    test_datas = []
    labels = []
    test_labels = []
    fpaths = []    #文件路径列表
    test_fpaths = []
    # 读入图片信息，并且从图片名中得到类别
    for fname in os.listdir(data_dir):
        fpath = os.path.join(data_dir, fname)
        fpaths.append(fpath)    # 向尾部添加图片路径
        image = Image.open(fpath)
        data = np.array(image) / 255.0   #生成普通矩阵，并归一化
        label = int(fname.split("(")[0])
        datas.append(data)     #数据列表
        labels.append(label)   #标签列表

    for fname in os.listdir(test_data_dir):
        fpath = os.path.join(test_data_dir, fname)
        test_fpaths.append(fpath)  # 向尾部添加
        image = Image.open(fpath)
        data = np.array(image) / 255.0
        test_datas.append(data)
        # label = int(fname.split("_")[0])
        # test_labels.append(label)
        test_labels=['cat','cat']

    # 全部转成矩阵
    datas = np.array(datas)
    test_datas = np.array(test_datas)
    labels = np.array(labels)
    test_labels = np.array(test_labels)
    # 输出矩阵维度
    print("shape of datas: {}，shape of labels: {}".format(datas.shape, labels.shape))
    return fpaths, test_fpaths, datas, labels, test_labels, test_datas

if __name__ == '__main__':
    # 数据文档夹
    data_dir = "resource"
    test_data_dir = "test"
    # 训练还是测试,true为训练
    train = False
    # 模型文档路径
    model_path = "model/image_model"

    fpaths, test_fpaths, datas, labels, test_labels, test_datas = read_data(data_dir,test_data_dir)
    # 计算有多少类图片
    num_classes = len(set(labels))
    print(num_classes)

    # 定义Placeholder，存放输入和标签

    datas_placeholder = tf.compat.v1.placeholder(tf.float32, [None, 32, 32, 3])   #那要让图片变成32*32的吗？？？
    labels_placeholder = tf.compat.v1.placeholder(tf.int32, [None])

    # 存放DropOut参数的容器，训练时为0.25，测试时为0
    # dropout是为了减少过拟合。解决方法就是在训练的时候，以一定的概率让部分神经元停止工作，这样就可以减少特征检测器（隐层节点）间的相互作用，避免过拟合情况的发生。
    dropout_placeholdr = placeholder(tf.float32)

    # 可以将placeholder理解为一种形参吧，然后不会被直接运行，只有在调用tf.run方法的时候才会被调用，这个时候需要向placeholder传递参数。
    tf.placeholder(
        dtype=float,  # 数据类型。常用的是tf.float32,tf.float64等数值类型
        shape=None,  # 数据形状。默认是None，就是一维值，也可以是多维（比如[2,3], [None, 3]表示列是3，行不定）
        name=None  # 名称
    )

    # 定义卷积层, 20个卷积核, 卷积核大小为5，用Relu激活
    conv0 = tf.layers.conv2d(datas_placeholder, 20, 5, activation=tf.nn.relu)
    # 定义max-pooling池化层，pooling窗口为2x2，步长为2x2
    pool0 = tf.layers.max_pooling2d(conv0, [2, 2], [2, 2])

    # 定义卷积层, 40个卷积核, 卷积核大小为4，用Relu激活
    conv1 = tf.layers.conv2d(pool0, 40, 4, activation=tf.nn.relu)
    # 定义max-pooling层，pooling窗口为2x2，步长为2x2
    pool1 = tf.layers.max_pooling2d(conv1, [2, 2], [2, 2])

    # 定义全连接部分（输出层）
    # 将3维特征转换为1维向量
    flatten = tf.layers.flatten(pool1)

    # 全连接层，转换为长度为100的特征向量
    fc = tf.layers.dense(flatten, 400, activation=tf.nn.relu)

    # 加上DropOut，防止过拟合
    dropout_fc = tf.layers.dropout(fc, dropout_placeholdr)

    # 未激活的输出层
    logits = tf.layers.dense(dropout_fc, num_classes)
    # 预测输出
    predicted_labels = tf.arg_max(logits, 1)

    arg_max(a, axis=None, out=None)
    # a 表示array
    # axis 表示指定的轴，默认是None，表示把array平铺，
    # out 默认为None，如果指定，那么返回的结果会插入其中

    # 利用交叉熵定义损失
    losses = tf.nn.softmax_cross_entropy_with_logits(
        labels=tf.one_hot(labels_placeholder, num_classes),
        logits=logits
    )
    # 平均损失
    mean_loss = tf.reduce_mean(losses)

    # 定义优化器，指定要优化的损失函数
    optimizer = tf.train.AdamOptimizer(learning_rate=1e-2).minimize(losses)

    # 用于保存和载入模型
    saver = tf.train.Saver()

    with tf.Session() as sess:

        if train:
            print("训练模式")
            # 如果是训练，初始化参数
            sess.run(tf.global_variables_initializer())
            # 定义输入和Label以填充容器，训练时dropout为0.25
            train_feed_dict = {
                datas_placeholder: datas,
                labels_placeholder: labels,
                dropout_placeholdr: 0.25
            }
            for step in range(136):
                _, mean_loss_val = sess.run([optimizer, mean_loss], feed_dict=train_feed_dict)

                if step % 10 == 0:
                    print("step = {}tmean loss = {}".format(step, mean_loss_val))
            saver.save(sess, model_path)
            print("训练结束，保存模型到{}".format(model_path))
        else:
            print("测试模式")
            # 如果是测试，载入参数
            saver.restore(sess, model_path)
            print("从{}载入模型".format(model_path))
            # label和名称的对照关系
            label_name_dict = {

                1: "猫",
                2: "狗"
            }
            # 定义输入和Label以填充容器，测试时dropout为0
            test_feed_dict = {
                datas_placeholder: test_datas,
                labels_placeholder: labels,
                dropout_placeholdr: 0
            }
            predicted_labels_val = sess.run(predicted_labels, feed_dict=test_feed_dict)
            # 真实label与模型预测label
            for fpath, real_label, predicted_label in zip(test_fpaths, test_labels, predicted_labels_val):
                # 将label id转换为label名
                real_label_name = label_name_dict[real_label]
                predicted_label_name = label_name_dict[predicted_label]
                print("{}t{} => {}".format(fpath, real_label_name, predicted_label_name))
