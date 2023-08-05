# 导入库
import matplotlib.pyplot as plt
import numpy as np

# #设定画布。dpi越大图越清晰，绘图时间越久
# fig = plt.figure(figsize=(5, 4), dpi=300)
# 导入数据


x = [7, 14, 20, 28, 30.95, 30.96, 31.7, 38, 45, 52, 59]
aa = 30.96  # 选中出价
bb = 40.15  # 心里出价
y = []
for i in x:
    if i < aa:
        y.append(aa-bb)
    else:
        y.append(0)
# 绘图命令

plt.title("N = 10,M = 5,R = 1", loc='center', fontname="Times New Roman", style='italic')
plt.legend(loc=2, frameon=False,prop={"family": "Times New Roman"})
plt.xlabel("Bid of User 1(Lose)", fontname="Times New Roman")

plt.ylabel("Utility of User 1(Lose)", fontname="Times New Roman")
plt.scatter(x, y, marker='*', c='g')
plt.plot(x, y, lw=1, ls='--', c='g', alpha=1)
plt.ylim(-12, 3)
plt.plot()
# 保存图片
plt.savefig('plot123_2.pdf',bbox_inches='tight')
plt.savefig('plot123_2.png', dpi=1000)
# show出图形
plt.show()

