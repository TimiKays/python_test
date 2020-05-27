# import input_data
# import numpy as np
#
# path = r"E:\pythonCode\TensorFlow\cifar10\cifar-10-batches-py"
# cifar10 = input_data.load_cifar10(path, one_hot=True)
# images = cifar10.images
# print("训练集图片：" + str(images.shape))
# labels = cifar10.labels
# print("训练集类别：" + str(labels.shape))
# test_images = cifar10.test.images
# print("测试集图片：" + str(test_images.shape))
# test_labels = cifar10.test.labels
# print("测试集类别：" + str(test_labels.shape))
# batch_xs, batch_ys = cifar10.next_batch(batch_size=500, shuffle=True)
# print("batch_xs shape is:" + str(batch_xs.shape))
# print("batch_ys shape is:" + str(batch_ys.shape))


# 导包
import warnings

from sklearn.preprocessing import OneHotEncoder

# warnings.filterwarning('ignore')

import pickle  # 官方提供的读取数据的模块
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt

# 读取数据的方法
def unpickle(file):
    with open(file, 'rb')as fo:
        dict = pickle.load(fo, encoding='bytes')
    return dict

# 训练数据加载
labels = []  # 存放图片的分类
X_train = []  # 存放图片的数据

for i in range(1, 6):
    # 已下载的文件路径
    data = unpickle('cifar10\cifar-10-python.tar\cifar-10-python\cifar-10-batches-py/data_batch_{}'.format(i))
    labels.append(data[b'labels'])
    X_train.append(data[b'data'])

X_train = np.array(X_train)  # 将list转换为ndarray
X_train = np.transpose(X_train.reshape(-1, 3, 32, 32), [0, 2, 3, 1]).reshape(-1, 3072)
y_train = np.array(labels).reshape(-1)
X_train = X_train.reshape(-1, 3072)

# 转换目标值概率
one_hot = OneHotEncoder()
y_train = one_hot.fit_transform(y_train.reshape(-1, 1)).toarray()

# 测试数据加载
# X_train 的第一维度为样本的数量，第二维度为RGB通道，第三维度为图片样本的宽，第四维度为图片样本的长。
# 所以需要利用transpose进行维度之间的转换，否则画出的图像将是错误的。
test = unpickle('cifar10/cifar-10-python.tar/cifar-10-python/cifar-10-batches-py/test_batch')
X_test = test[b'data']
X_test = np.transpose(X_test.reshape(-1, 3, 32, 32), [0, 2, 3, 1]).reshape(-1, 3072)
y_test = one_hot.transform(np.array(test[b'labels']).reshape(-1, 1)).toarray()
print(y_test)

# 查看图片
plt.figure(figsize=(1,1))
plt.imshow(X_test[1].reshape(32,32,3))
plt.show()

# ----------构建神经网络-----------
# 定义占位符
X = tf.placeholder(dtype=tf.float32, shape=[None, 3072])
y = tf.placeholder(dtype=tf.float32, shaoe=[None, 10])
kp = tf.placeholder(dtype=tf.float32)


# 定义变量
def gen_v(shape, std=5e-2):
    return tf.Variable(tf.truncated_normal(shape=shape, stddev=std))


def conv(input_, filter_, b):
    conv = tf.nn.conv2d(input_, filter_, strides=[1, 1, 1, 1], padding='SAME') + b  # 卷积
    conv = tf.layers.batch_normalization(conv, training=True)  # 归一化
    conv = tf.nn.relu(conv)  # 激活
    return tn.nn.max_pool(conv, [1, 3, 3, 1], [1, 2, 2, 1], 'SAME')  # 池化


# 形状改变，4维
def net_work(X, kp):
    input_ = tf.reshape(X, shape=[-1, 32, 32, 3])

    # 第一层
    filter1 = gen_v(shape=[3, 3, 3, 64])  # 定义卷积核
    b1 = gen_v(shape=[64])
    pool1 = conv(input_, filter1, b1)

    # 第二层
    filter2 = gen_v([3, 3, 64, 128])
    b2 = gen_v(shape=[128])
    pool2 = conv(pool1, filter2, b2)

    # 第三层
    filter3 = gen_v([3, 3, 128, 256])
    b3 = gen_v([256])
    pool3 = conv(pool2, filter3, b3)

    # 第一次全连接层
    dense = tf.reshape(pool3, shape=[-1, 4 * 4 * 256])
    fcl_w = gen_v(shape=[4 * 4 * 256, 1024])
    fcl_b = gen_v(shape=[1024])
    bn_fc_1 = tf.layers.batch_normalization(tf.matmul(dense, fcl_w) + fcl_b, training=True)
    relu_fu_1 = tf.nn.relu(bn_fc_1)


    # 期望 fc1.shape = [-1, 1024]

    # 抛弃
    '''
    每次选择部分的特征，类似套袋，防止过拟合
    keep_prob:每次选择的数据所占全部数据的比例
    rate:每次不选择的数据所占全部数据的比例
    '''
    dp = tf.nn.dropout(relu_fu_1, keep_prob=kp)

    # 输出层
    out_w = gen_v(shape=[1024, 10])
    out_b = gen_v(shape=[10])
    out = tf.matmul(dp, out_w) + out_b
    return out


