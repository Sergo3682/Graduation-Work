from bitvector import BitVector
from helpers import is_pow_of_2
from helpers import log_2


class TruthTable:
    def __init__(self, out_vec: BitVector, input_names=None):
        if not is_pow_of_2(out_vec.size):
            raise ValueError('Size of BitVector must be power of two!')
        self.out_vec = out_vec
        if input_names is not None:
            if len(input_names) != log_2(self.out_vec.size):
                raise ValueError('Size of input names list is not equal nums of inputs!')
            self.input_names = input_names
        else:
            self.input_names = []

    def __str__(self):
        res = ""
        if len(self.input_names) > 0:
            res += " ".join(self.input_names) + " | " + "Q" + "\n"
            res += '_' * (len(res) - 1) + '\n'
        for i in range(self.out_vec.size):
            bit_list_str = [str(x) for x in list(BitVector(i, log_2(self.out_vec.size)))]
            if len(self.input_names) > 0:
                for j in range(len(self.input_names)):
                    res += ' '*(len(self.input_names[j])-1) + bit_list_str[j] + ' '
                res += '| ' + str(self.out_vec[i]) + '\n'
            else:
                res += " ".join(bit_list_str) + " | " + str(self.out_vec[i]) + "\n"
        return res

    def __repr__(self):
        return f'{self.__class__.__name__}({repr(self.out_vec)}, {repr(self.input_names)})'

    def get_row_by_index(self, number):
        res_size = log_2(self.out_vec.size)
        res_tuple = (BitVector(number, res_size), self.out_vec[number])
        return res_tuple

    def get_rows_by_value(self, q_value):
        list_of_tuples = []
        for i in range(self.out_vec.size):
            if self.out_vec[i] == q_value:
                tuple_of_row = (BitVector(i, log_2(self.out_vec.size)), self.out_vec[i])
                list_of_tuples.append(tuple_of_row)
        return list_of_tuples

    def invert(self):
        new_bit_vector_val = ~self.out_vec.val & ((1 << self.out_vec.size) - 1)
        return self.__class__(BitVector(new_bit_vector_val, self.out_vec.size), self.input_names)
