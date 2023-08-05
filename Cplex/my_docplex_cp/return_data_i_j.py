import copy

import numpy as np
import xlrd
import openpyxl
import random
import math

edge_x_y = [[25, 34], [25, 160], [25, 313], [25, 402], [10, 500], [10, 600], [185, 18], [185, 158], [200, 229],
            [205, 316], [177, 408], [150, 465], [137, 533], [141, 600], [212, 538], [212, 607], [287, 11], [287, 158],
            [287, 300], [287, 400], [287, 535], [287, 600], [287, 692], [430, 11], [430, 56], [430, 105], [430, 160],
            [430, 220], [430, 310], [430, 400], [430, 550], [430, 600], [430, 690], [580, 11], [580, 80], [580, 164],
            [580, 220], [580, 315], [580, 400], [580, 475], [580, 550], [580, 600], [580, 690], [680, 11], [680, 85],
            [680, 170], [680, 250], [680, 315], [680, 600], [766, 11], [766, 162], [766, 316], [766, 404], [766, 541],
            [766, 600], [766, 690], [870, 42], [870, 162], [870, 260], [870, 360], [870, 465], [870, 540], [870, 600],
            [1000, 11], [1000, 162], [1000, 250], [1000, 470], [1000, 543], [1000, 690], [1122, 78], [1082, 263],
            [1104, 433]]
# 地图大小
x = 1201
y = 719
# 用户的覆盖范围为半径500的圆圈
user_xhqd = 500
user_zddk = 20
user_x_y = []
# excel中的预选用户数
exc_user = 200


# 从圆内选出num个整数坐标
def getRandomPointInCircle(num, radius, centerx, centery):  # num为数量，radius为圆的半径，（centerx, centery）为圆心坐标。
    samplePoint = []
    for i in range(num):
        while True:
            x = random.uniform(-radius, radius)
            y = random.uniform(-radius, radius)
            if (x ** 2) + (y ** 2) <= (radius ** 2):
                samplePoint.append(int(x) + centerx)
                samplePoint.append(int(y) + centery)
                break

        # plt.plot(x + centerx, y + centery, '*', color="blue")

    return samplePoint


# 当i个用户 j个边缘时,k种资源时,分配算法所需的各项数据
def return_all_data(i, j, k):
    global edge_x_y, user_x_y, x, y, user_xhqd, user_zddk
    user_size, edge_size, res_size = i, j, k  # 用户数量, edge数量, 资源类型数量
    bids, S, v, caps, THP_edge, bandwidth = {}, {}, {}, {}, {}, {}
    path = r'../xml数据集/数据集提炼.xlsx'

    user_sheet = 'user'
    edge_sheet = 'edge'
    bandwidth_sheet = 'bandwidth'
    user_file = xlrd.open_workbook(path).sheet_by_name(user_sheet)  # 打开指定路径下的user表
    edge_file = xlrd.open_workbook(path).sheet_by_name(edge_sheet)  # 打开指定路径下的edge表
    bandwidth_file = xlrd.open_workbook(path).sheet_by_name(bandwidth_sheet)  # 打开指定路径下的bandwidth表

    # 数组
    bids_1 = []
    S_1 = []
    v_1 = []
    caps_1 = [[0 for i in range(res_size)] for i in range(edge_size)]
    THP_edge_1 = []
    bandwidth_1 = [[0 for i in range(edge_size)] for i in range(user_size)]

    # ***********************随机从200个用户中抽取i个用户 抽的时excel中的用户序号***********************
    set_I = random.sample(range(1, exc_user + 1), i)

    # 随机抽j个边缘节点
    set_J = random.sample(edge_x_y, j)

    set_K = range(1, res_size + 1)

    # 用户出价bids
    # for i in set_I:
    print('excel中被抽中的',user_size,'个用户（从1开始）','列表中被抽中的',edge_size,'个边缘')
    print(set_I)
    for i in range(1, user_size + 1):
        bids[i] = user_file.cell_value(set_I[i - 1], 20)
        bids_1.append(bids[i])
    print('*******************字典*********************')
    print('bids =', bids)  # 注：只有这个字典中的key标注了 excel文件中用户的序号，在其他的列表中用户序号均以下标表示

    # 用户需求S
    for i in range(1, user_size + 1):  # 用户i对资源k的需求矩阵 包含 内存需求和带宽需求
        S_temp = []
        for k in range(1, res_size + 2):
            S[i, k] = round(user_file.cell_value(set_I[i - 1], 20 + k), 2)
            # S_1[i - 1][k - 1] = S[i, k]
            S_temp.append(round(user_file.cell_value(set_I[i - 1], 20 + k), 2))
        S_1.append(S_temp)
    print('S =', S)

    # 用户数据价值v
    for i in range(1, user_size + 1):
        v[i] = round(user_file.cell_value(set_I[i - 1], 5), 2)
        v_1.append(v[i])
    print('v =', v)

    # 边缘服务器的容量caps
    for j in range(1, edge_size + 1):
        for k in set_K:
            caps[j, k] = edge_file.cell_value(j, k)
            caps_1[j - 1][k - 1] = caps[j, k]
    print('caps =', caps)

    # 边缘服务器的处理转发速度
    for j in range(1, edge_size + 1):
        THP_edge[j] = edge_file.cell_value(j, 2)
        THP_edge_1.append(THP_edge[j])
    print('THP_edge =', THP_edge)

    # 计算部署矩阵 1.先给user定义位置 2.算与各个服务器的距离
    # 定义位置 用户的位置要在边缘服务器的近点 先随一个edge点，在这个edge点的带宽距离之内生成坐标
    # 获取用户的带宽 S_1[i][1]
    # 根据带宽算最小距离
    for i in range(user_size):
        center = random.randrange(0, edge_size, 1)  # 随机一个edge 当作圆心
        center_x = set_J[center][0]
        center_y = set_J[center][1]
        distance_min = (user_zddk - S_1[i][1]) * (user_xhqd / user_zddk)
        samp = getRandomPointInCircle(1, distance_min, center_x, center_y)  # 数量 半径 x,y
        # append 用户坐标
        user_x_y.append(samp)

    # 计算与set_J的距离
    for i in range(user_size):
        for j in range(edge_size):
            # 计算距离
            distance = math.sqrt(pow(user_x_y[i][0] - set_J[j][0], 2) + pow(user_x_y[i][1] - set_J[j][1], 2))
            # print('用户', i, '边缘', j, '距离为', distance)
            # 计算带宽
            if distance > user_xhqd:
                # 距离太远 带宽为0
                bandwidth[i + 1, j + 1] = 0
                bandwidth_1[i][j] = 0
            else:
                bandwidth[i + 1, j + 1] = round(user_zddk - (distance / (user_xhqd / user_zddk)), 1)
                bandwidth_1[i][j] = round(user_zddk - (distance / (user_xhqd / user_zddk)), 1)
    print("bandwidth =", bandwidth)

    print('用户坐标', user_x_y)
    print('边缘节点坐标', set_J)
    # # 部署矩阵(N x M)信号强度矩形
    # for i in range(1, user_size + 1):
    #     for j in range(1, edge_size + 1):
    #         bandwidth[i, j] = bandwidth_file.cell_value(i, j)
    #         bandwidth_1[i - 1][j - 1] = bandwidth[i, j]
    # print("信号强度bandwidth=", bandwidth)

    # 打印数组
    print('*******************数组*********************')
    print('bids =', bids_1)
    print('S =', S_1)
    print('v =', v_1)
    print('caps =', caps_1)
    print('THP_edge =', THP_edge_1)
    print('bandwidth =', bandwidth_1)
    return user_size, edge_size, res_size, bids_1, S_1, v_1, caps_1, THP_edge_1, bandwidth_1, bids, S, v, caps, THP_edge, bandwidth

# return_all_data(5, 3, 1)
