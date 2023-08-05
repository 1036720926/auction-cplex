import matplotlib.pyplot as plt
import numpy as np


size = 4

x = np.arange(size)

# 有a/b/c三种类型的数据，n设置为3
total_width, n = 0.6, 3
# 每种类型的柱状图宽度
width = total_width / n

list1 = [12968.166067583365, 13467.618527851713, 13562.189805609776, 13210.30589589816]
list2 = [13312.285999999998, 13606.159999999998, 13590.874, 13210.314000000002]
list3 = [10661.826117492787, 11829.381622700737, 11832.242368724175, 11683.006184416536]

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
plt.ylim(0,20000)
# 显示图例
# plt.figure(dpi=300,figsize=(24,24))

plt.title("N = 40,M = 20,R = 1,(32)", loc='center', fontname="Times New Roman", style='italic')
plt.legend(loc=2, prop={"family": "Times New Roman"})
plt.xlabel("Bandwidth", fontname="Times New Roman")
plt.ylabel("Social Welfare", fontname="Times New Roman")
plt.savefig('plot123_2.pdf',bbox_inches='tight')
plt.savefig('plot123_2.png', dpi=1000)
# 显示柱状图
plt.show()
