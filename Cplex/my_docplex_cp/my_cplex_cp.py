import copy
from math import exp

from docplex.cp.model import CpoModel
import time

def main_cplex(user_size, edge_size, res_size,bids, S, v, caps, THP_edge, bandwidth):
    # 代码开始运行
    start = time.perf_counter()

    # from read_data_from_excel import user_size, edge_size, res_size, bids, S, v, caps, THP_edge, bandwidth
    # from return_data_i_j import return_all_data
    # user_size, edge_size, res_size, \
    # bids_1, S_1, v_1, caps_1, THP_edge_1, bandwidth_1, \
    # bids, S, v, caps, THP_edge, bandwidth = return_all_data(15, 6, 1)

    # 测试
    # user_size, edge_size, res_size = 10, 5, 1  # 用户数量, edge数量, 资源类型数量
    # bids = {1: 29.0, 2: 6.0, 3: 25.0, 4: 15.0, 5: 45.0, 6: 38.0, 7: 16.0, 8: 36.0, 9: 28.0, 10: 9.0}
    # S = {(1, 1): 7.53, (1, 2): 6.0, (2, 1): 16.83, (2, 2): 1.0, (3, 1): 10.78, (3, 2): 5.0, (4, 1): 10.7, (4, 2): 9.0,
    #      (5, 1): 6.83, (5, 2): 3.0, (6, 1): 17.33, (6, 2): 9.0, (7, 1): 14.22, (7, 2): 1.0, (8, 1): 9.62, (8, 2): 5.0,
    #      (9, 1): 8.29, (9, 2): 9.0, (10, 1): 11.29, (10, 2): 9.0}
    # v = {1: 76.13, 2: 56.73, 3: 108.09, 4: 47.34, 5: 118.65, 6: 34.91, 7: 19.07, 8: 35.94, 9: 45.12, 10: 360.09}
    # caps = {(1, 1): 32.0, (2, 1): 32.0, (3, 1): 32.0, (4, 1): 32.0, (5, 1): 32.0}
    # THP_edge = {1: 30.0, 2: 30.0, 3: 30.0, 4: 30.0, 5: 30.0}
    # bandwidth = {(1, 1): 0, (1, 2): 7.6, (1, 3): 0, (1, 4): 11.7, (1, 5): 0, (2, 1): 8.6, (2, 2): 0, (2, 3): 0,
    #              (2, 4): 0, (2, 5): 0, (3, 1): 7.5, (3, 2): 1.7, (3, 3): 7.8, (3, 4): 0, (3, 5): 11.3, (4, 1): 0,
    #              (4, 2): 4.8, (4, 3): 0, (4, 4): 11.8, (4, 5): 0, (5, 1): 0, (5, 2): 3.0, (5, 3): 0, (5, 4): 9.4,
    #              (5, 5): 0, (6, 1): 0, (6, 2): 8.6, (6, 3): 11.0, (6, 4): 1.6, (6, 5): 11.4, (7, 1): 13.6, (7, 2): 0,
    #              (7, 3): 0.6, (7, 4): 0, (7, 5): 4.1, (8, 1): 0, (8, 2): 8.1, (8, 3): 0, (8, 4): 12.2, (8, 5): 0,
    #              (9, 1): 0, (9, 2): 17.1, (9, 3): 0, (9, 4): 12.8, (9, 5): 1.1, (10, 1): 0, (10, 2): 0, (10, 3): 16.8,
    #              (10, 4): 0, (10, 5): 16.7}
    bids_copy = copy.deepcopy(bids)

    # 写死的小例子, 用于测试 (规模小)
    # user_size, edge_size, res_size = 3, 2, 2  # 用户数量, edge数量, 资源类型数量
    # bids = {1: 300, 2: 300, 3: 300}  # 用户报价
    # S = {(1, 1): 3, (1, 2): 1, (1, 3): 1,  # 用户资源需求(N x R+1)最后一列是带宽需求 第一列是内存需求也就是数据大小
    #      (2, 1): 2, (2, 2): 1, (2, 3): 2,
    #      (3, 1): 2, (3, 2): 4, (3, 3): 3}
    # v = {1: 700, 2: 300, 3: 500}
    # caps = {(1, 1): 5, (1, 2): 50,  # 边缘服务器资源容量(M x R)
    #         (2, 1): 5, (2, 2): 50}
    # THP_edge = {1: 20, 2: 30}  # 边缘服务器的处理转发速率
    # bandwidth = {(1, 1): 1, (1, 2): 1,  # 部署矩阵(N x M)信号强度矩形
    #              (2, 1): 2, (2, 2): 2,
    #              (3, 1): 3, (3, 2): 3}
    # bids_copy = copy.deepcopy(bids)

    THP_cloud = 500  # 云端处理速度
    k1 = 100000  # k1 k2 k3 是关于e函数的三个常数
    k2 = 0.00007  # 多加0会变平缓但也会导致单个用户的增益变小，使得该用户选不上
    k3 = 100000
    a = 0.1  # 边缘的单位带宽成本
    b = 0.1  # 模型单位计算成本
    r = 0.1  # 模型单位存储成本
    a1 = 0.01  # 云端的单位带宽成本
    a2 = 0.05  # 用户单位收集数据成本
    b2 = 0.05  # 用户单位计算成本
    m = 5  # 模型大小
    delta_l = 5  # 本地训练轮数
    delta_g = 10  # 全局训练轮数

    # 定义一些用于计算的全局变量！
    set_I = range(1, user_size + 1)
    set_J, set_K = range(1, edge_size + 1), range(1, res_size + 1)

    def opt_alloc():
        # 创建模型
        mode = CpoModel()

        # 定义决策变量x_ij
        x_vars = {(i, j): mode.binary_var(name="x_{0}_{1}".format(i, j))
                  for i in set_I for j in set_J}  # (N x M)

        # 添加约束条件
        # 1.用户的带宽需求≤用户与其能探测到的边缘节点之间的传输速度(带宽需求是用户需求向量的最后一个)
        for j in set_J:
            for i in set_I:
                mode.add(S[i, res_size + 1] * x_vars[i, j] <= bandwidth[i, j])
        # 2.边缘服务器接收到的带宽总和≤边缘服务器的处理转发速度：(边缘服务器的处理转发速度在它的资源容量向量的最后一个)
        for j in set_J:
            mode.add(mode.sum(S[i, res_size + 1] * x_vars[i, j] for i in set_I) <= THP_edge[j])
        # 3.边缘服务器分配出去的资源总和≤它的最大资源容量
        for j in set_J:
            for k in set_K:
                mode.add(mode.sum(S[i, k] * x_vars[i, j] for i in set_I) <= caps[j, k])
        # 4.对于云端来说，所有边缘节点选择的用户的带宽总和≤云端的处理速度(因为用户的带宽≤边缘的转发速率，所有边缘的转发速率之和≤云端的处理速度)
        mode.add(mode.sum(S[i, res_size + 1] * x_vars[i, j] for j in set_J for i in set_I) <= THP_cloud)
        # 5.一个用户在一个边缘服务器最多只能被分配一次
        for i in set_I:
            mode.add(mode.sum(x_vars[i, j] for j in set_J) <= 1)

        # 定义目标函数
        # fai - 全局轮数*边缘成本(带宽,计算,存储) - 全局轮数*云端成本(带宽) - 用户成本(收集数据(本地数据大小*a2), 计算) - 用户报价
        objective = k1 - k3 * mode.exponent(
            (-k2) * mode.sum(x_vars[i, j] * v[i] for j in set_J for i in set_I)) - delta_g * mode.sum(
            x_vars[i, j] * (S[i, res_size + 1] * a + m * b + m * r) for i in set_I for j in set_J) - delta_g * mode.sum(
            x_vars[i, j] * S[i, res_size + 1] * a1 for i in set_I for j in set_J) - mode.sum(
            x_vars[i, j] * S[i, 1] * (a2 + delta_l * delta_g * m * b2) for i in set_I for j in set_J) - mode.sum(
            x_vars[i, j] * bids[i] for i in set_I for j in set_J)
        # 最大化目标
        mode.add(mode.maximize(objective))

        win = set()
        edge_result = []
        # 求解模型
        # msol = mode.solve()
        msol = mode.solve(TimeLimit=10)  # 时间限制 单位为秒 如不限制 数据一多 跑个没完
        print("------------------")
        for i in set_I:
            for j in set_J:
                if msol[x_vars[i, j]] == 1:
                    win.add(i - 1)  # 最小用户为0
                    edge_result.append(j - 1)  # 最小边缘为0
                    # print('user{0} edge{1} 为'.format(i, j), msol[x_vars[i, j]])
        # print('胜者(从0开始) =', win)
        # print('边缘(从0开始) =', edge_result)
        # print("------------------e^vi-边缘成本-云成本-报价")
        # # print('vi 总和', sum(msol[x_vars[i, j]] * v[i] for j in set_J for i in set_I))
        # print('e函数', k1 - k3 * exp((-k2) * sum(msol[x_vars[i, j]] * v[i] for j in set_J for i in set_I)))
        # print('边缘节点的带宽成本',
        #       delta_g * sum(msol[x_vars[i, j]] * (S[i, res_size + 1] * a + m * b + m * r) for i in set_I for j in set_J))
        # print('云的带宽成本', delta_g * sum(msol[x_vars[i, j]] * S[i, res_size + 1] * a1 for i in set_I for j in set_J))
        # print('用户成本', sum(msol[x_vars[i, j]] * S[i, 1] * (a2 + delta_l * delta_g * m * b2) for i in set_I for j in set_J))
        # print('用户报价', sum(msol[x_vars[i, j]] * bids[i] for i in set_I for j in set_J))
        return win, edge_result, msol

    # 运行分配 接收两个值
    win, edge_result, msol = opt_alloc()
    social_welfare = msol.get_objective_value()
    # 初始化支付列表
    pi = []

    # VCG支付
    for i in win:
        bids = copy.deepcopy(bids_copy)
        # 把当前用户排除（改变用户i+1的报价 因为win中的用户下标比bids字典中的用户key值要小1 故而i+1）
        bids[i + 1] = k1
        # 不存在当前用户时，其他人的收益
        social_welfare_except_i = opt_alloc()[2].get_objective_value()
        # 反向拍卖的支付计算 = 最优 - 排除当前用户后的最优 + 当前用户报价
        pi.append(social_welfare - social_welfare_except_i + bids_copy[i + 1])

    # 计算资源利用率  1.edge总资源  2.win消耗的资源
    liyonglv = []

    for k in range(res_size):
        temp = 0
        temp1 = 0
        for j in range(edge_size):
            temp += caps[j + 1, k + 1]
        for i in win:
            temp1 += S[i + 1, k + 1]
        liyonglv.append(temp1 / temp)
    # 计算带宽利用率
    temp = 0
    for j in range(edge_size):
        temp += THP_edge[j + 1]
    temp1 = 0
    for i in win:
        temp1 += S[i + 1, res_size + 1]
    liyonglv.append(temp1 / temp)

    print('胜者(从0开始)')
    print(win)
    print('对应分配边缘')
    print(edge_result)
    print('社会福利')
    print(social_welfare)
    print('资源利用率')  # 分配资源/所有资源
    for i in range(len(liyonglv)):
        print('第', i, '种资源', '利用率为', liyonglv[i])
    print('支付为：')
    print(pi)
    # http://ibmdecisionoptimization.github.io/docplex-doc/cp/index.html
    # 搜索 CpoModelSolution
    # 有相关操作
    # print(msol.solution)
    # print(msol.get_objective_value())

    # 代码结束运行
    end = time.perf_counter()
    # 计算运行时间，单位为秒
    print('运行时间为：{}秒'.format(end - start))
    # 返回社会福利 资源利用率，总支付，运行时间
    return social_welfare, liyonglv, sum(pi), end - start
