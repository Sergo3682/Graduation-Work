from net import Net


def is_pow_of_2(n):
    return (n != 0) and ((n & (n-1)) == 0)


def log_2(n):
    counter = 0
    while n != 1:
        n = n >> 1
        counter += 1
    return counter


def print_partial_truth_table(list_of_tuples: list):
    res_str = ""
    i = 0
    while i < len(list_of_tuples):
        bit_list_str = [str(x) for x in list_of_tuples[i][0]]
        res_str += " ".join(bit_list_str) + " | " + str(list_of_tuples[i][1]) + "\n"
        i += 1
    print(res_str)


#def width_of_circuit(net_list: list):
#    if type(net_list) == list:
#        for net in net_list:
#            if type(net) != Net:
#                raise TypeError('Your input must be \'list\' of \'Net()\'')
#    else:
#        raise TypeError('Your input must be \'list\' of \'Net()\'')
#    i = 0
#    width = 0
#    for i in range(len(net_list)):
#        width += len(net_list[i].node_lists)
#    return width - i


def insert(source_str, insert_str, pos):
    return source_str[:pos] + insert_str + source_str[pos:]
