from numpy import loadtxt
import numpy as np
file = open('data.csv', 'rb')
data = np.genfromtxt(file,dtype=None,delimiter = ",",autostrip = True, encoding='GBK')
# autostrip = True 删除所有多余空格
blank = np.where(data=='') #查找空缺位置
data[blank] = -1   #进行填充
print(data)