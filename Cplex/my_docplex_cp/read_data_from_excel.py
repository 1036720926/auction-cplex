import xlrd

# Cplex求解时需要用到的变量
user_size, edge_size, res_size = 10, 6, 1  # 用户数量, edge数量, 资源类型数量
bids, S, v, caps, THP_edge, bandwidth = {}, {}, {}, {}, {}, {}

set_I, set_J, set_K = range(1, user_size + 1), range(1, edge_size + 1), range(1, res_size + 1)

path = r'..\xml数据集\数据集提炼.xlsx'

user_sheet = 'user'
user_temp_sheet = 'user_temp'
edge_sheet = 'edge'
bandwidth_sheet = 'bandwidth'
user_file = xlrd.open_workbook(path).sheet_by_name(user_sheet)  # 打开指定路径下的user表
user_temp_file = xlrd.open_workbook(path).sheet_by_name(user_temp_sheet)  # 打开指定路径下的user表
edge_file = xlrd.open_workbook(path).sheet_by_name(edge_sheet)  # 打开指定路径下的edge表
bandwidth_file = xlrd.open_workbook(path).sheet_by_name(bandwidth_sheet)  # 打开指定路径下的bandwidth表

# 数组
bids_1 = []
S_1 = [[0 for i in range(res_size + 1)] for i in range(user_size)]
v_1 = []
caps_1 = [[0 for i in range(res_size)] for i in range(edge_size)]
THP_edge_1 = []
bandwidth_1 = [[0 for i in range(edge_size)] for i in range(user_size)]
# 用户出价bids
for i in set_I:
    bids[i] = user_file.cell_value(i, 20)
    bids_1.append(bids[i])
print("用户报价bids=", bids)

# 用户需求S
for i in set_I:  # 用户i对资源k的需求矩阵 包含 内存需求和带宽需求
    for k in range(1, res_size + 2):
        S[i, k] = user_file.cell_value(i, 20 + k)
        S_1[i - 1][k - 1] = S[i, k]
print("用户需求S=", S)

# 用户数据价值v
for i in set_I:
    v[i] = user_file.cell_value(i, 5)
    v_1.append(v[i])
print("用户价值v=", v)

# 边缘服务器的容量caps
for j in set_J:
    for k in set_K:
        caps[j, k] = edge_file.cell_value(j, k)
        caps_1[j - 1][k - 1] = caps[j, k]
print("边缘服务器容量caps=", caps)

# 边缘服务器的处理转发速度
for j in set_J:
    THP_edge[j] = edge_file.cell_value(j, 2)
    THP_edge_1.append(THP_edge[j])
print("边缘服务器处理转发速度THP_edge=", THP_edge)
# 部署矩阵(N x M)信号强度矩形
for i in set_I:
    for j in set_J:
        bandwidth[i, j] = bandwidth_file.cell_value(i, j)
        bandwidth_1[i - 1][j - 1] = bandwidth[i, j]
print("信号强度bandwidth=", bandwidth)

# 打印数组
print('bids =', bids_1)
print('S =', S_1)
print('v =', v_1)
print('caps =', caps_1)
print('THP_edge =', THP_edge_1)
print('bandwidth =', bandwidth_1)
