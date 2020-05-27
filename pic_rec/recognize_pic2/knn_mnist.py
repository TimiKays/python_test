import torch
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split
from torch.utils.data import DataLoader
from sklearn.datasets import load_digits
from sklearn.neighbors import KNeighborsClassifier

print('...')
# 加载数据
digits =load_digits()
print('加载完成!')

# 划分训练集和测试集
Xtrain, Xtest, Ytrain, Ytest = train_test_split(digits.data, digits.target, test_size=0.20, random_state=2)

# 训练
knn=KNeighborsClassifier( ).fit(Xtrain, Ytrain)

# 预测
Ypred = knn.predict(Xtest)
print('完成预测!')

# 预测结果评估
print(classification_report(Ytest, Ypred))
print(accuracy_score(Ytest, Ypred))
print(knn.score(Xtest, Ytest))


