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


def insert(source_str, insert_str, pos):
    return source_str[:pos] + insert_str + source_str[pos:]


def two_to_the_power_of(n):
        return 2 << (n - 1)
