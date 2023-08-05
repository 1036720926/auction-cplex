import matplotlib.pyplot as plt
import numpy as np


size = 4

x = np.arange(size)

# 有a/b三种类型的数据，n设置为2
total_width, n = 0.6, 2
# 每种类型的柱状图宽度
width = total_width / n

list1 = [0.254190625, 0.2567552083333333, 0.2530802083333334, 0.27583333333333326]
list2 = [0.2582197916666667, 0.2710885416666667, 0.26822083333333335, 0.26722604166666664]


# 重新设置x轴的坐标
x = x - (total_width - width) / 2
print(x)
plt.rcParams['font.serif'] = ['Times New Roman']
# 画柱状图

plt.bar(x, list1, width=width, label="FLRA", color='#0066cc')
plt.bar(x + width, list2, width=width, label="Greedy", color='#9ACD32')
# plt.bar(x + 2*width, c, width=width, label="c")
plt.xticks(np.arange(size), (100, 120, 140, 160))
# 显示图例
# plt.figure(dpi=300,figsize=(24,24))

plt.title("M = 20,R = 1,(32,30)", loc='center', fontname="Times New Roman", style='italic')
plt.legend(loc=2, prop={"family": "Times New Roman"})
plt.xlabel("Number of Users", fontname="Times New Roman")
plt.ylabel("Bandwidth Utilization", fontname="Times New Roman")
plt.ylim(0,0.5)
plt.savefig('plot123_2.pdf',bbox_inches='tight')
plt.savefig('plot123_2.png', dpi=1000)
# 显示柱状图
plt.show()
