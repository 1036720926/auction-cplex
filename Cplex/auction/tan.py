# 分配
import copy
from math import sqrt
from math import exp
import time


def main_tan(user_size, edge_size, res_size, bids, S, v, caps, THP_edge, bandwidth):
    # 代码开始运行
    start = time.perf_counter()
    # from my_docplex_cp.read_data_from_excel import user_size, edge_size, res_size, bids_1, S_1, v_1, caps_1, THP_edge_1, bandwidth_1
    # bids = bids_1
    # S = S_1
    # v = v_1
    # caps = caps_1
    # THP_edge = THP_edge_1
    # bandwidth = bandwidth_1

    # 读取数据 _1是数组
    # from my_docplex_cp.return_data_i_j import return_all_data
    # user_size, edge_size, res_size, \
    # bids_1, S_1, v_1, caps_1, THP_edge_1, bandwidth_1, bids1, \
    # S1, v1, caps1, THP_edge1, bandwidth1 = return_all_data(10, 5, 1)  # 用户 边缘 资源
    # bids = copy.deepcopy(bids_1)
    # S = copy.deepcopy(S_1)
    # v = copy.deepcopy(v_1)
    # caps = copy.deepcopy(caps_1)
    # THP_edge = copy.deepcopy(THP_edge_1)
    # bandwidth = copy.deepcopy(bandwidth_1)

    # 写死的小例子, 用于测试 (规模小)
    # user_size, edge_size, res_size = 10, 5, 1  # 用户数量, edge数量, 资源类型数量
    # bids = [6.0, 4.0, 2.0, 29.0, 7.0, 40.0, 16.0, 13.0, 2.0, 49.0]
    # S = [[12.34, 4.0], [12.37, 3.0], [10.42, 6.0], [15.9, 2.0], [12.49, 1.0], [7.27, 8.0], [14.22, 1.0], [15.83, 2.0],
    #      [6.22, 7.0], [15.71, 9.0]]
    # v = [26.08, 13.75, 105.1, 77.06, 96.08, 6.99, 19.07, 1.06, 64.16, 55.56]
    # caps = [[32.0], [32.0], [32.0], [32.0], [32.0]]
    # THP_edge = [10.0, 10.0, 10.0, 10.0, 10.0]
    # bandwidth = [[0, 4.5, 15.0, 12.7, 0], [4.4, 10.2, 4.9, 0, 7.2], [12.2, 0, 0, 0, 7.1], [11.3, 15.7, 3.7, 0, 16.9],
    #              [8.1, 4.0, 0, 0, 9.0], [0, 0, 6.0, 14.1, 0], [3.5, 5.2, 0, 0, 7.0], [12.6, 8.6, 0, 0, 11.8],
    #              [7.5, 0.4, 0, 0, 6.4], [10.8, 9.4, 0, 0, 14.0]]

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
    # 标识数组（可否传输）
    bandwidth_01 = [[0 for i in range(edge_size)] for i in range(user_size)]
    for i in range(user_size):
        for j in range(edge_size):
            if S[i][res_size] <= bandwidth[i][j]:
                bandwidth_01[i][j] = bandwidth[i][j]
            else:
                bandwidth_01[i][j] = 0
    print('用户对各个边缘的信道带宽 0为不可到达bandwidth_01', bandwidth_01)

    # 每个边缘的待选用户
    sort_user = [[] for i in range(edge_size)]
    sort_suanzi = [[] for i in range(edge_size)]
    for j in range(edge_size):
        for i in range(user_size):
            if bandwidth_01[i][j] != 0:
                sort_user[j].append(i)
    print('每个边缘的待选用户sort_user', sort_user)

    # 计算算子
    def func(i, j):
        num = v[i] / (bids[i] * sqrt(
            sum(pow(S[i][k] / caps[j][k], 2) for k in range(res_size)) + pow(S[i][res_size] / THP_edge[j], 2)))
        return num

    # 冒泡 把待选用户 及其算子从大到小排序 对sort_user 和 sort_suanzi 排序
    def mao_pao(list1, list2):
        for i in range(len(list1)):
            sign = False
            for j in range(0, len(list1) - i - 1):
                if list1[j] < list1[j + 1]:
                    list1[j], list1[j + 1] = list1[j + 1], list1[j]
                    list2[j], list2[j + 1] = list2[j + 1], list2[j]
                    sign = True
                # 如果没有交换说明列表已经有序，结束循环
                if not sign:
                    break

    temp = []
    for j in range(edge_size):
        for i in sort_user[j]:
            temp.append(func(i, j))
        sort_suanzi[j] = temp
        temp = []
    print('每个边缘的待选用户的算子sort_suanzi', sort_suanzi)

    # 调用冒泡 给用户及其算子排序
    for j in range(edge_size):
        mao_pao(sort_suanzi[j], sort_user[j])
    print('排序后的用户顺序sort_user', sort_user)
    print('排序后的算子sort_suanzi', sort_suanzi)
    sort_user_1 = copy.deepcopy(sort_user)
    sort_suanzi_1 = copy.deepcopy(sort_suanzi)

    # 分配
    # 先选出待选用户少的边 返回用户最少的边的下标
    def short_edge(list, user_size):  # 这里的list是sort_user 二维数组
        mi = user_size + 1
        temp_j = len(list) + 1
        for j in range(len(list)):
            if 0 < len(list[j]) < mi:
                mi = len(list[j])
                temp_j = j
        return mi, temp_j  # temp_j表示sort_user[temp_j]是入度最小，mi表示这个边有几个潜在用户

    # 拿 sort_suanzi[temp_j][0]分配 判断资源是否足够 若足够则sort_user[temp_j][0]和sort_suanzi[temp_j][0]消去

    # 让入度少的边缘先分配，如果该入度少的边缘的当前第一个用户因为资源不够无法分配，则单独删掉这个用户然后顺移到下一个用户判断资源是否足够，
    # 如果这个入度少的边的所有用户都因为资源不够无法分配，则该边缘退出竞争（清空这个边缘对应的数组但不影响其他数组中的用户）
    # 如果有足够的资源分配给某个用户，那么就更新资源矩阵和删除sort_user sort_suanzi 中所有该用户
    # win = {}
    # loss = []
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
            cost += delta_g * (S[temp][res_size] * a + m * b + m * r) + delta_g * S[temp][res_size] * a1 + S[temp][
                0] * (
                            a2 + delta_l * delta_g * m * b2) + bids[temp]
            # print('边缘成本',delta_g * (S[temp][res_size] * a + m * b + m * r))
            # print('云端成本',delta_g * S[temp][res_size] * a1)
            # print('用户成本',S[temp][0] * (a2 + delta_l * delta_g * m * b2))
            # print('出价',bids[temp])
        fai_w = k1 - k3 * exp(-k2 * sum1)
        V_w = fai_w - cost
        return V_w

    def alloc_tan():
        win = {}
        while 1:
            # 找入度最小的边 返回 入度 和 边的下标
            mi, temp_j = short_edge(sort_user, user_size)
            if temp_j == len(sort_user) + 1:  # 意味着当前没有入度至少为1的边了，没得分了，直接结束
                break
            else:
                # 还有得分 那就先创建一个能分的边缘的复制数组
                temp_sort_user = copy.deepcopy(sort_user[temp_j])
                # flag表示这一轮是否分配过了
                flag = 0
                for i in range(len(sort_user[temp_j])):
                    if flag == 0 and i < len(sort_user[temp_j]) - 1:
                        # 当前预选用户 temp_win
                        temp_win = sort_user[temp_j][i]
                        # print(sort_user[temp_j])
                        # print(temp_sort_user)
                        for k in range(res_size):
                            # temp_suanzi = sort_suanzi[temp_j][i]
                            # 如果资源或带宽不够
                            if caps[temp_j][k] < S[temp_win][k] or THP_edge[temp_j] < S[temp_win][res_size]:
                                # print('i=', i)
                                # print(temp_win, '资源不够')
                                temp_sort_user.remove(temp_win)
                                # temp_sort_suanzi.remove(sort_suanzi[temp_j][i])
                                break
                            # 如果资源够
                            else:  # 分配资源
                                flag = 1  # 表示分配成功
                                # print('i=', i)
                                # print(temp_win, '资源够')
                                win[temp_win] = temp_j
                                # print(win)
                                temp_sort_user.remove(temp_win)
                                # temp_sort_suanzi.remove(sort_suanzi[temp_j][i])

                                # 更新资源矩阵 和 带宽矩阵
                                for k in range(res_size):
                                    caps[temp_j][k] -= S[temp_win][k]
                                THP_edge[temp_j] -= S[temp_win][res_size]
                                # print('分配后的剩余资源矩阵', caps)

                                # 更新当前边缘的一维数组
                                sort_user[temp_j] = copy.deepcopy(temp_sort_user)
                                # sort_suanzi[temp_j] = temp_sort_suanzi

                                # 更新其他排序矩阵中的该用户
                                for j in range(edge_size):
                                    if sort_user[j].count(temp_win) > 0:
                                        sort_user[j].remove(temp_win)
                                        # sort_suanzi[j].remove(temp_suanzi)
                                # print('排序后的用户顺序sort_user', sort_user)
                    elif flag == 0 and i == len(sort_user[temp_j]) - 1:
                        temp_win = sort_user[temp_j][i]
                        for k in range(res_size):
                            if caps[temp_j][k] < S[temp_win][k] or THP_edge[temp_j] < S[temp_win][res_size]:
                                # print('i=', i)
                                # print(temp_win, '资源不够')
                                sort_user[temp_j] = []
                                # print('边缘', temp_j, '=', sort_user[temp_j], '退出')
                                break
                            # 如果资源够
                            else:  # 分配资源
                                flag = 1  # 表示分配成功
                                # print('i=', i)
                                # print(temp_win, '资源够')
                                win[temp_win] = temp_j
                                # print(win)
                                temp_sort_user.remove(temp_win)

                                # 更新资源矩阵和带宽矩阵
                                for k in range(res_size):
                                    caps[temp_j][k] -= S[temp_win][k]
                                THP_edge[temp_j] -= S[temp_win][res_size]
                                # print('分配后的剩余资源矩阵', caps)

                                # 更新当前边缘的一维数组
                                sort_user[temp_j] = copy.deepcopy(temp_sort_user)
                                # print('边缘', temp_j, '=', sort_user[temp_j], '退出')
                                # 更新其他排序矩阵中的该用户
                                for j in range(edge_size):
                                    if sort_user[j].count(temp_win) > 0:
                                        sort_user[j].remove(temp_win)
                                        # sort_suanzi[j].remove(temp_suanzi)
                                # print('排序后的用户顺序sort_user', sort_user)

                    elif flag == 1:
                        break
        return win

    win = alloc_tan()
    # 计算利用率
    liyonglv = []
    # 算所有的资源
    for k in range(res_size):
        temp = 0
        temp1 = 0
        for j in range(edge_size):
            temp += caps_1[j][k]
            temp1 += caps[j][k]
        liyonglv.append(1 - (temp1 / temp))
    temp = 0
    temp1 = 0
    for j in range(edge_size):
        temp += THP_edge_1[j]
        temp1 += THP_edge[j]
    liyonglv.append(1 - (temp1 / temp))

    print(win)
    print('胜者为：(最小编号为0)')
    print(sorted(win.keys()))
    print('对应分配边缘')
    print(end=' ')
    for i in sorted(win.keys()):
        print(win[i], end='  ')
    print()
    print('社会福利')
    value = value_of_win(win.keys(), bids, v, S)
    print(value)
    print('资源利用率')  # 分配资源/所有资源
    for i in range(len(liyonglv)):
        print('第', i, '种资源', '利用率为', liyonglv[i])

    # 支付（二分法）
    pi = []
    for i in win.keys():
        bids = copy.deepcopy(bids_1)
        S = copy.deepcopy(S_1)
        v = copy.deepcopy(v_1)
        caps = copy.deepcopy(caps_1)
        THP_edge = copy.deepcopy(THP_edge_1)
        bandwidth = copy.deepcopy(bandwidth_1)
        sort_user = copy.deepcopy(sort_user_1)
        # sort_suanzi = copy.deepcopy(sort_suanzi_1)
        bids[i] = 2 * bids[i]
        # flag1 表示探测多少次没探测到上届 就结束 flag2 表示是否进入二分法
        flag1 = 0
        flag2 = 1
        while i in alloc_tan().keys():
            if flag1 > 10:
                # 表示不用二分
                flag2 = 0
                break
            else:
                # 每一轮分配完后要把边缘服务器的资源容量和带宽容量恢复原样 唯一变化的只有bids[i]
                caps = copy.deepcopy(caps_1)
                THP_edge = copy.deepcopy(THP_edge_1)
                sort_user = copy.deepcopy(sort_user_1)
                # sort_suanzi = copy.deepcopy(sort_suanzi_1)
                bids[i] = 2 * bids[i]
                flag1 += 1
        LB = bids[i] / 2
        UB = bids[i]
        # 二分法
        e = 0.0001
        while UB - LB >= e and flag2 == 1:
            bids[i] = (LB + UB) / 2
            win_temp = alloc_tan().keys()
            if i in win_temp:
                # 每一轮分配完后要把边缘服务器的资源容量和带宽容量恢复原样 唯一变化的只有bids[i]
                caps = copy.deepcopy(caps_1)
                THP_edge = copy.deepcopy(THP_edge_1)
                sort_user = copy.deepcopy(sort_user_1)
                # sort_suanzi = copy.deepcopy(sort_suanzi_1)
                LB = bids[i]
                bids[i] = (LB + UB) / 2


            else:
                caps = copy.deepcopy(caps_1)
                THP_edge = copy.deepcopy(THP_edge_1)
                sort_user = copy.deepcopy(sort_user_1)
                # sort_suanzi = copy.deepcopy(sort_suanzi_1)
                UB = bids[i]
                bids[i] = (LB + UB) / 2
        if flag2 == 1:
            pi.append((LB + UB) / 2)
        else:
            pi.append(100000)
        flag1 = 0
        flag2 = 1

    print('支付为：')
    print(pi)

    # 代码结束运行
    end = time.perf_counter()
    # 计算运行时间，单位为秒
    print('运行时间为：{}秒'.format(end - start))
    # 返回社会福利 资源利用率，总支付，运行时间
    return value, liyonglv, sum(pi), end - start
