import matplotlib.pyplot as plt
import numpy as np


size = 4

x = np.arange(size)

# 有a/b/c三种类型的数据，n设置为3
total_width, n = 0.6, 3
# 每种类型的柱状图宽度
width = total_width / n

list1 = [7480.676460000029, 8212.991640000038,  10095.375999999977, 7690.761419999994]
list2 = [258018.14204000004, 257407.58638, 290447.60922, 253497.8051999999]
list3 = [388.11045999999577, 485.34275999994636, 489.0315200000259, 478.08041999999207]

# 重新设置x轴的坐标
x = x - (total_width - width) / 2
print(x)
plt.rcParams['font.serif'] = ['Times New Roman']
# 画柱状图

plt.bar(x, list1, width=width, label="FLRA", color='#0066cc')
plt.bar(x + width, list2, width=width, label="OPT-FLRA", color='#FF3E23')
plt.bar(x + 2*width, list3, width=width, label="Greedy", color='#9ACD32')
# plt.bar(x + 2*width, c, width=width, label="c")
plt.xticks(np.arange(size), (10, 20, 30, 40))
plt.ylim(10,10**7)
plt.yscale("log")
# 显示图例
# plt.figure(dpi=300,figsize=(24,24))

plt.title("N = 40,M = 20,R = 1,(32)", loc='center', fontname="Times New Roman", style='italic')
plt.legend(loc=2, prop={"family": "Times New Roman"})
plt.xlabel("Bandwidth", fontname="Times New Roman")
plt.ylabel("Execution Time(ms)", fontname="Times New Roman")
plt.savefig('plot123_2.pdf',bbox_inches='tight')
plt.savefig('plot123_2.png', dpi=500)
# 显示柱状图
plt.show()
