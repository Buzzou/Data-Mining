import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import random as rd
from collections import defaultdict
import matplotlib.cm as cm

dataset = pd.read_csv('Mall_Customers.csv')
X = dataset.iloc[:, [3, 4]].values

K = 5
m = 200

# step 1：随机确定初始质心
Centroids = np.array([]).reshape(2, 0)

for i in range(K):
    rand = rd.randint(0, m - 1)
    Centroids = np.c_[Centroids, X[rand]]  # 质心矩阵

# step2：迭代至收敛
num_iter = 100
Output = defaultdict()
Output = {}  # 输出
for n in range(num_iter):
    # step 2.a
    EuclidianDistance = np.array([]).reshape(m, 0)
    for k in range(K):
        tempDist = np.sum((X - Centroids[:, k]) ** 2, axis=1)
        EuclidianDistance = np.c_[EuclidianDistance, tempDist]  # 距离矩阵

    C = np.argmin(EuclidianDistance, axis=1) + 1  # 最小距离，存储列号
    # step 2.b
    Y = {}  # 每次循环临时结果
    for k in range(K):
        Y[k + 1] = np.array([]).reshape(2, 0)
    for i in range(m):
        Y[C[i]] = np.c_[Y[C[i]], X[i]]

    for k in range(K):
        Y[k + 1] = Y[k + 1].T

    for k in range(K):
        Centroids[:, k] = np.mean(Y[k + 1], axis=0)  # 更新质心

    Output = Y

# 可视化原数据
plt.scatter(X[:, 0], X[:, 1], c='black', label='unclustered data')
plt.xlabel('Income')
plt.ylabel('Number of transactions')
plt.legend()
plt.title('Plot of data points')
plt.show()

# 可视化聚类数据
color = ['red', 'blue', 'green', 'cyan', 'magenta']
labels = ['cluster1', 'cluster2', 'cluster3', 'cluster4', 'cluster5']
for k in range(K):
    plt.scatter(Output[k + 1][:, 0], Output[k + 1][:, 1], c=color[k], label=labels[k])
plt.scatter(Centroids[0, :], Centroids[1, :], s=300, c='yellow', label='Centroids')
plt.xlabel('Income')
plt.ylabel('Number of transactions')
plt.legend()
plt.show()
