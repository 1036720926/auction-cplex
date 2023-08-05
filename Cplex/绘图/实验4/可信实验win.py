# 导入库
import matplotlib.pyplot as plt
import numpy as np

# #设定画布。dpi越大图越清晰，绘图时间越久
# fig = plt.figure(figsize=(5, 4), dpi=300)
# 导入数据

x = [7, 14, 20, 28, 31.13, 31.14, 33, 38, 45, 52, 59]
aa = 31.14  # 支付
bb = 17.67  # 心里出价
y = []
for i in x:
    if i < aa:
        y.append(aa - bb)
    else:
        y.append(0)
# 绘图命令

plt.title("N = 10,M = 5,R = 1", loc='center', fontname="Times New Roman", style='italic')
plt.legend(loc=2, frameon=False,prop={"family": "Times New Roman"})
plt.xlabel("Bid of User 4(Win)", fontname="Times New Roman")
plt.ylabel("Utility of User 4(Win)", fontname="Times New Roman")
plt.scatter(x, y, marker='*', c='r')
plt.plot(x, y, lw=1, ls='--', c='r', alpha=1)
plt.ylim(-5,20)
plt.plot()
# 保存图片
plt.savefig('plot123_2.pdf',bbox_inches='tight')
plt.savefig('plot123_2.png', dpi=1000)
# show出图形
plt.show()

