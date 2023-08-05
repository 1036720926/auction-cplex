# 用户规模大小对分配的影响
# 读取数据
from my_docplex_cp.return_data_i_j import return_all_data

from auction.cimo import main_cimo
# from my_docplex_cp.my_cplex_cp import main_cplex
from auction.tan import main_tan


# 输入用户数和边缘数和次数，输出实验结果（平均社会福利，资源利用率，总支付，运行时间）
def shiyan(user_size, edge_size, res_size, num):
    value_cimo = [0 for i in range(num)]
    liyonglv_cimo = [[] for i in range(num)]
    sum_pi_cimo = [0 for i in range(num)]
    time_cimo = [0 for i in range(num)]

    # value_cplex = [0 for i in range(num)]
    # liyonglv_cplex = [[] for i in range(num)]
    # sum_pi_cplex = [0 for i in range(num)]
    # time_cplex = [0 for i in range(num)]

    value_tan = [0 for i in range(num)]
    liyonglv_tan = [[] for i in range(num)]
    sum_pi_tan = [0 for i in range(num)]
    time_tan = [0 for i in range(num)]

    for i in range(num):
        user_size, edge_size, res_size, \
        bids_1, S_1, v_1, caps_1, THP_edge_1, bandwidth_1, bids1, \
        S1, v1, caps1, THP_edge1, bandwidth1 = return_all_data(user_size, edge_size, res_size)  # 用户 边缘 资源
        # 接收社会福利，资源利用率，总支付，运行时间 然后算平均
        value_cimo[i], liyonglv_cimo[i], sum_pi_cimo[i], time_cimo[i] = main_cimo(user_size, edge_size, res_size,
                                                                                  bids_1, S_1, v_1, caps_1, THP_edge_1,
                                                                                  bandwidth_1)
        # value_cplex[i], liyonglv_cplex[i], sum_pi_cplex[i], time_cplex[i] = main_cplex(user_size, edge_size, res_size,
        #                                                                                bids1, S1, v1, caps1, THP_edge1,
        #                                                                                bandwidth1)
        value_tan[i], liyonglv_tan[i], sum_pi_tan[i], time_tan[i] = main_tan(user_size, edge_size, res_size,
                                                                             bids_1, S_1, v_1, caps_1, THP_edge_1,
                                                                             bandwidth_1)

    # 算cimo的社会福利，资源利用率，总支付，运行时间平均
    avg = []
    for i in range(res_size + 1):
        avg.append(sum(liyonglv_cimo[i]) / num)
    print('次模的平均社会福利{}，平均资源利用率{}，平均支付{}，平均运行时间{}'
          .format(sum(value_cimo) / num, avg, sum(sum_pi_cimo) / num, sum(time_cimo) / num))

    # 算cplex的社会福利，资源利用率，总支付，运行时间平均
    # avg = []
    # for i in range(res_size + 1):
    #     avg.append(sum(liyonglv_cplex[i]) / num)
    # print('cplex的平均社会福利{}，平均资源利用率{}，平均支付{}，平均运行时间{}'
    #       .format(sum(value_cplex) / num, avg, sum(sum_pi_cplex) / num, sum(time_cplex) / num))

    # 算tan的社会福利，资源利用率，总支付，运行时间平均
    avg = []
    for i in range(res_size + 1):
        avg.append(sum(liyonglv_tan[i]) / num)
    print('tan的平均社会福利{}，平均资源利用率{}，平均支付{}，平均运行时间{}'
          .format(sum(value_tan) / num, avg, sum(sum_pi_tan) / num, sum(time_tan) / num))


shiyan(180, 20, 1, 5)
