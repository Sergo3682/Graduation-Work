from truthtable import TruthTable
from bitvector import BitVector
from net import Net
from helpers import log_2
from serialnodes import SerialNodes


def lazy_me():
    bv = BitVector(0b1010011101100110, 16)
    tt = TruthTable(bv, ['A', 'B', 'C', 'D'])
    global sc
    sc = SchematicBuilder(tt)


class SchematicBuilder:
    def __init__(self, input_truth_table: TruthTable):
        self.truth_table = input_truth_table
        self.inverted = False

        self.input_names = self.truth_table.input_names.copy()
        self.input_names.reverse()

        self.netlist = [Net()]
        self.nodelist = []

    def calc_in_bits_leading_to_res(self, out_val):
        rows_list = self.truth_table.get_rows_by_value(out_val)
        zeroes_num = 0
        ones_num = 0
        for bv, out_val in rows_list:
            zeroes_in_row, ones_in_row = bv.calc_bits()
            zeroes_num += zeroes_in_row
            ones_num += ones_in_row
        return zeroes_num, ones_num

    def is_inverting_needed(self):
        n00, n10 = self.calc_in_bits_leading_to_res(0)
        n01, n11 = self.calc_in_bits_leading_to_res(1)
        return not (n01 + n10) > (n00 + n11)

    @staticmethod
    def list_of_tuples_to_list_of_bitvectors(lst: list):
        for i in range(len(lst)):
            lst[i] = lst[i][0]
        return lst

    def algorithm_pd(self, lst: [BitVector], names: [str], idx=0):
        if not self.complete_set_of_combination(lst):
            print(idx)

            max_ones_in_column = 0
            max_zeroes_in_column = 0
            tmp_zeroes_name = ''
            tmp_ones_name = ''
            lst_copy = lst.copy()

            for col in range(lst[0].size):
                tmp_ones = 0
                tmp_zeroes = 0
                for row in range(len(lst)):
                    if lst[row][col] == 0:
                        tmp_zeroes += 1
                    else:
                        tmp_ones += 1
                if tmp_ones > max_ones_in_column:
                    max_ones_in_column = tmp_ones
                    tmp_ones_name = names[col]
                if tmp_zeroes > max_zeroes_in_column:
                    max_zeroes_in_column = tmp_zeroes
                    tmp_zeroes_name = '!' + names[col]
            self.netlist.append(Net())
            if max_zeroes_in_column > max_ones_in_column:
                max_name = tmp_zeroes_name
                lst_copy = self.grouping(lst_copy, names.index(max_name[1:]), 0)
                for i in lst_copy:
                    lst.remove(i)
                lst_copy = self.list_of_bv_idx_removing(lst_copy, names.index(max_name[1:]))
#                print(f'{max_zeroes_in_column}\t{tmp_zeroes_name}')
            else:
                max_name = tmp_ones_name
                lst_copy = self.grouping(lst_copy, names.index(max_name), 1)
                for i in lst_copy:
                    lst.remove(i)
                lst_copy = self.list_of_bv_idx_removing(lst_copy, names.index(max_name))
#                print(f'{max_ones_in_column}\t{tmp_ones_name}')

            self.netlist[idx].node_lists.append(SerialNodes([f'{max_name}'], self.netlist[idx + 1]))

            if max_name[0] == '!':
                max_name = max_name[1:]

            names_copy = names.copy()
            names_copy.remove(max_name)

            #for i in lst_copy:
            #   lst.remove(i)
            print(lst_copy, len(lst_copy))
            print(names_copy, len(names_copy))
            self.algorithm_pd(lst_copy, names_copy, idx+1)
            if len(lst) == 1:
                self.netlist[idx].node_lists.append(SerialNodes(self.gen_one_line_branch_pd(lst[0], names), None))

    @staticmethod
    def gen_one_line_branch_pd(bv: BitVector, names):
        nodes = []
        for i in range(bv.size):
            if bv[i] == 1:
                nodes.append(names[i])
            else:
                nodes.append('!' + names[i])
        return nodes

    @staticmethod
    def list_of_bv_idx_removing(lst: [BitVector], idx):
        for i in range(len(lst)):
            lst[i] = lst[i].remove_idx(idx)
        return lst

    @staticmethod
    def grouping(lst: [BitVector], grouping_idx, val: int):
        ans = []
        for i in range(len(lst)):
            if lst[i][grouping_idx] == val:
                ans.append(lst[i])
        return ans

    @staticmethod
    def complete_set_of_combination(lst: [BitVector]):
        ans = True
        checker = False
        for num in range(log_2(len(lst[0]))):
            for bv in lst:
                checker = (num == bv.val)
            ans = ans and checker
            checker = False
        return ans

    def build_pull_down_network(self):
        if self.is_inverting_needed():
            self.truth_table = self.truth_table.invert()
            self.inverted = True
            print('INVERTED!!!!!!!!')
        original_row_list = self.list_of_tuples_to_list_of_bitvectors(self.truth_table.get_rows_by_value(0))
        cp_list = original_row_list.copy()
        self.algorithm_pd(cp_list, self.input_names)
        #return cp_list
