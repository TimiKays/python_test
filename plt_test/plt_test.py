# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import matplotlib
import numpy as np


a=np.arange(1,50,1)
matplotlib.rcParams['font.family']='SimHei'
plt.subplot(3,3,1)
plt.plot(a)
plt.title('1-5')

plt.subplot(3,3,2)
plt.plot(a**2)
plt.title('1-5的平方')

plt.subplot(3,3,3)
plt.plot(a**3)
plt.title('1-5的立方')

plt.subplot(3,3,4)
plt.plot(1/a)
plt.title('倒数')

plt.subplot(3,3,5)
plt.plot(1/a,a**3)
plt.title('不知道是啥')

plt.subplot(3,3,6)
plt.plot(np.gradient(a**3))
plt.title('立方的梯度')
plt.show()

count=0
for i in range(21):
    for j in range(51):
        k=100-5*i-2*j
        if k>=0:
            count+=1
print(count)