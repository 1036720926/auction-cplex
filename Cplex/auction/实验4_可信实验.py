# 计算改变出价后的用户效用
# 10用户 5边缘 边缘参数为32，30
import copy
from math import exp
import time

# 代码开始运行
start = time.perf_counter()

# 读取数据
# from my_docplex_cp.return_data_i_j import return_all_data
#
# user_size, edge_size, res_size, \
# bids_1, S_1, v_1, caps_1, THP_edge_1, bandwidth_1, bids1, \
# S1, v1, caps1, THP_edge1, bandwidth1 = return_all_data(5, 3, 1)  # 用户 边缘 资源
# bids = copy.deepcopy(bids_1)
# S = copy.deepcopy(S_1)
# v = copy.deepcopy(v_1)
# caps = copy.deepcopy(caps_1)
# THP_edge = copy.deepcopy(THP_edge_1)
# bandwidth = copy.deepcopy(bandwidth_1)

# 小例子
# user_size, edge_size, res_size = 5, 3, 1  # 用户数量, edge数量, 资源类型数量
# bids = [66, 79, 48, 110, 44]
# S = [[1, 2], [3, 2], [3, 3], [1, 4], [2, 1]]
# v = [108, 92, 75, 20, 189]
# caps = [[5], [5], [5]]
# THP_edge = [5, 5, 5]
# bandwidth = [[3, 2, 1], [0, 2, 1], [2, 4, 1], [2, 1, 3], [1, 2, 3]]

# 临时测试
user_size, edge_size, res_size = 10, 5, 1  # 用户数量, edge数量, 资源类型数量
# bids = [33.0, 40.15, 22.0, 12.0, 17.67, 25.0, 44.0, 33.0, 28.0, 37.0]
bids = [33.0, 30.96, 22.0, 12.0, 17.67, 25.0, 44.0, 33.0, 28.0, 37.0]
S = [[12.5, 7.0], [7.12, 7.0], [13.94, 6.0], [12.29, 8.0], [8.44, 5.0], [10.89, 7.0], [13.33, 6.0], [15.58, 7.0],
     [12.35, 9.0], [6.29, 4.0]]
v = [5.68, 20.24, 26.74, 16.48, 22.34, 180.09, 53.79, 21.18, 80.08, 27.16]
caps = [[32.0], [32.0], [32.0], [32.0], [32.0]]
THP_edge = [30.0, 30.0, 30.0, 30.0, 30.0]
bandwidth = [[12.7, 11.1, 0, 0, 0.0], [0, 0, 9.5, 12.3, 0], [0, 0, 2.2, 0, 11.8], [3.5, 8.4, 5.0, 0, 15.3],
             [9.9, 14.9, 0.8, 0, 10.7], [0, 0, 14.1, 9.7, 0], [0, 2.6, 8.0, 0, 12.0], [3.4, 7.9, 9.7, 0, 10.4],
             [0.2, 5.0, 0, 0, 18.0], [16.4, 15.9, 0, 0, 2.2]]
#
bids_1 = copy.deepcopy(bids)
S_1 = copy.deepcopy(S)
v_1 = copy.deepcopy(v)
caps_1 = copy.deepcopy(caps)
THP_edge_1 = copy.deepcopy(THP_edge)
bandwidth_1 = copy.deepcopy(bandwidth)

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


# 找出当前最有用的人 输入win集合和wait集合 返回的max_i 是一个单个用户的集合（例如{4}）
def best_i(win, wait):
    win_temp = set(win)
    wait_temp = set(wait)
    max_temp = 0
    max_i = {-1}
    for i in range(len(wait)):
        if len(wait_temp) > 0:
            i_temp = {wait_temp.pop()}
        xx = value_of_win(win_temp | i_temp, bids, v, S) - value_of_win(win, bids, v, S)
        # print("当前选的人的下标i_temp为", i_temp, "增幅xx为", xx)
        if xx > max_temp:
            max_temp = xx
            max_i = i_temp
    # print("-----------用户", max_i, "这轮第一,增幅为", max_temp)

    return max_i


# print("本轮胜者为", best_i(win={0}, wait={5, 6, 3, 7, 4}))


# 用集合计算函数：fai(w) - 成本   输入win集合 返回V是一个值
def value_of_win(win, bids, v, S):
    # global k1, k2, k3, a, b, r, a1, m
    win_temp = set(win)
    sum1 = 0
    V_w = 0
    fai_w = 0
    cost = 0
    for i in range(len(win_temp)):
        temp = win_temp.pop()
        # print(temp)
        sum1 = sum1 + v[temp]
        cost += delta_g * (S[temp][res_size] * a + m * b + m * r) + delta_g * S[temp][res_size] * a1 + S[temp][0] * (
                a2 + delta_l * delta_g * m * b2) + bids[temp]
        # print('边缘成本',delta_g * (S[temp][res_size] * a + m * b + m * r))
        # print('云端成本',delta_g * S[temp][res_size] * a1)
        # print('用户成本',S[temp][0] * (a2 + delta_l * delta_g * m * b2))
        # print('出价',bids[temp])
    fai_w = k1 - k3 * exp(-k2 * sum1)
    V_w = fai_w - cost
    return V_w


# print(value_of_win({0}))


# 判断资源是否足够 以及判断边缘服务器处理转发速率是否足够 输入待分配用户 返回0或1,和 flag_edge为待分配边缘下标
def resource_0_1(user, user_conn_edge, caps, THP_edge, S):
    flag_edge = []
    sum = 0
    for j in user_conn_edge[user]:
        for k in range(res_size):
            if caps[j][k] < S[user][k] or THP_edge[j] < S[user][
                res_size]:  # 如果当前边缘的某一项资源满足不了当前用户的需求,或者 当前边缘处理转发速率不够 那就看看下一个边缘
                # flag_edge[j] = 0
                break
            else:  # 满足需求则把边缘下标放入flag_edge
                flag_edge.append(j)

    if len(flag_edge) > 0:
        return 1, flag_edge
    else:
        return 0, flag_edge


# print('资源是否够，flag_edge', resource_0_1(0))


# 分配资源 输入 当前用户 及 该用户的可分配的边缘 用户是从下标0开始的，边缘也最小从0开始
def resource_alloc(user, flag_edge, result, wait, user_conn_edge, caps, THP_edge, S):
    # 找出可分配边中入度最小的边 min_in
    flag_edge_in = edge_in(flag_edge, wait, user_conn_edge)
    min_in = min(flag_edge_in, key=flag_edge_in.get)  # min_in是user将要分配的边缘服务器
    # print('分配到边', min_in)
    # print()
    result[user] = min_in  # 将分配结果存在result中 user 最小为0 min_in 也是最小为0
    # result[user + 1] = min_in + 1  # 将分配结果存在result中
    # *******************更新边缘服务器资源***********************
    for k in range(res_size):
        caps[min_in][k] -= S[user][k]
    # 更新边缘服务器处理转发速度
    THP_edge[min_in] -= S[user][res_size]


# 当前待选边缘入度 从wait集合 和各个用户能连接到的边
# 返回flag_edge中的边缘各自对应的入度的字典 例如[2, 4, 5] 对应的 入度{2:3,4:1,5:3}
def edge_in(flag_edge, wait, user_conn_edge):
    # global wait
    wait_temp = list(wait)  # 把wait集合中的用户下标 转为临时列表 方便进行多次循环
    flag_edge_in = {}  # 字典

    for j in flag_edge:  # [2, 4, 5]
        flag_edge_in[j] = 0
        for i in wait_temp:  # 6个待选 = [1,5,7,6,8,4]
            if j in user_conn_edge[i]:
                flag_edge_in[j] += 1
    # print('flag_edge_in = ', flag_edge_in)
    return flag_edge_in


# 数据预处理
# 各个用户能连接到的边
user_conn_edge = [[] for i in range(user_size)]
for i in range(user_size):
    for j in range(edge_size):
        if bandwidth[i][j] >= S[i][res_size]:
            user_conn_edge[i].append(j)


# print("各个用户能连接到的边user_conn_edge", user_conn_edge)


def alloc(user_size, edge_size, res_size, bids, S, v, caps, THP_edge, bandwidth):
    # 创建win loss wait 集合
    win = set()
    loss = set()
    wait = set(i for i in range(user_size))
    # 创建result字典用于存储分配结果
    result = {}

    # # 数据预处理
    # # 各个用户能连接到的边
    global user_conn_edge

    # user_conn_edge = [[] for i in range(user_size)]
    # for i in range(user_size):
    #     for j in range(edge_size):
    #         if bandwidth[i][j] >= S[i][res_size]:
    #             user_conn_edge[i].append(j)
    # # print("各个用户能连接到的边user_conn_edge", user_conn_edge)

    for i in range(user_size):  # 循环 user_size 轮， 每轮选出一个最有用的用户，并根据剩余资源是否足够来进入win或loss
        user = best_i(win, wait).pop()  # 当前用户
        if user == -1:
            # print('已经没有可用用户')
            loss = loss | wait
            wait.clear()
            break
        # print('user = ', user)
        x_0_1, flag_edge = resource_0_1(user, user_conn_edge, caps, THP_edge, S)  # x 为可否分配 flag_edge为能够分配的边缘的下标
        # print('x_0_1, flag_edge = ', x_0_1, flag_edge)
        if x_0_1 == 1:  # 至少有一个边能够分配给当前用户 加入win集合 更新资源矩阵 边缘服务器处理速度矩阵 和win wait loss集合
            # print('分配', user)
            resource_alloc(user, flag_edge, result, wait, user_conn_edge, caps, THP_edge, S)  # 在哪一步更新集合
            # 分配完资源和带宽后 资源矩阵caps 和 带宽矩阵THP_edge就少了一些资源
            win.add(user)
            wait.remove(user)
        else:  # 加入loss集合
            # print('未分配', user)
            loss.add(user)
            wait.remove(user)
            # print('分配失败')
            # print()
    # print('--------结果如下------')
    # print('胜者(最小编号为0) =', win)
    # print('败者(最小编号为0) =', loss)
    # print('--------分配结果(字典)-用户：边缘(最小为0)-----')
    # print(result)

    # 计算系统的总体效益
    # print('系统的总收益为 =', value_of_win(win, bids, v, S))
    liyonglv = []
    # 计算资源利用率 1.算所有资源 2.算胜者用户的资源
    for k in range(res_size):
        temp = 0
        for j in range(edge_size):
            # 使用未经修改的caps_1计算总资源
            temp += caps_1[j][k]
        # print(temp)

        temp1 = 0
        for i in win:
            temp1 += S_1[i][k]
        # print(temp1)

        # print('第', k, '种资源的利用率为', temp1 / temp)
        liyonglv.append(temp1 / temp)
    # 带宽利用率 1.算所有带宽 2.算胜者带宽
    temp = 0
    for j in range(edge_size):
        temp += THP_edge_1[j]
    # print(temp)
    temp1 = 0
    for i in win:
        temp1 += S[i][res_size]
    # print(temp1)
    # print('带宽利用率为', temp1 / temp)
    liyonglv.append(temp1 / temp)

    return win, result, liyonglv


win, result, liyonglv = alloc(user_size, edge_size, res_size, bids, S, v, caps, THP_edge, bandwidth)
print('--------结果如下------')
print('胜者为：(最小编号为0)')
print(win)
print(result)
print('对应分配边缘')
print(' ', end='')
for i in sorted(result.keys()):
    print(result[i], end='  ')
print()
print('社会福利')
print(value_of_win(win, bids, v, S))
print('资源利用率')  # 分配资源/所有资源
for i in range(len(liyonglv)):
    print('第', i, '种资源', '利用率为', liyonglv[i])
# 定价
pi = []

for i in win:
    bids = copy.deepcopy(bids_1)
    S = copy.deepcopy(S_1)
    v = copy.deepcopy(v_1)
    caps = copy.deepcopy(caps_1)
    THP_edge = copy.deepcopy(THP_edge_1)
    bandwidth = copy.deepcopy(bandwidth_1)
    bids[i] = 2 * bids[i]

    while i in alloc(user_size, edge_size, res_size, bids, S, v, caps, THP_edge, bandwidth)[0]:
        # 每一轮分配完后要把边缘服务器的资源容量和带宽容量恢复原样 唯一变化的只有bids[i]
        caps = copy.deepcopy(caps_1)
        THP_edge = copy.deepcopy(THP_edge_1)
        bids[i] = 2 * bids[i]

    LB = bids[i] / 2
    UB = bids[i]
    # 二分法
    e = 0.0001
    while UB - LB >= e:
        bids[i] = (LB + UB) / 2
        win_temp = alloc(user_size, edge_size, res_size, bids, S, v, caps, THP_edge, bandwidth)[0]
        if i in win_temp:
            # 每一轮分配完后要把边缘服务器的资源容量和带宽容量恢复原样 唯一变化的只有bids[i]
            caps = copy.deepcopy(caps_1)
            THP_edge = copy.deepcopy(THP_edge_1)

            LB = bids[i]
            bids[i] = (LB + UB) / 2


        else:
            caps = copy.deepcopy(caps_1)
            THP_edge = copy.deepcopy(THP_edge_1)

            UB = bids[i]
            bids[i] = (LB + UB) / 2
    pi.append((LB + UB) / 2)
print('支付为：')
print(pi)

# 代码结束运行
end = time.perf_counter()
# 计算运行时间，单位为秒
print('运行时间为：{}秒'.format(end - start))

# 计算胜者4号的用户效益

# 计算败者1号的用户效益