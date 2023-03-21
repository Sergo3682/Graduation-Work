from truthtable import TruthTable
from bitvector import BitVector
from net import Net
from serialnodes import SerialNodes


def lazy_me():
    bv = BitVector(0xDC, 8)
    tt = TruthTable(bv, ['a', 'b', 'c'])
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

    def group_of_lists(self, lst : list):
        pass

    @staticmethod
    def list_of_tuples_to_list_of_bitvectors(lst: list):
        for i in range(len(lst)):
            lst[i] = lst[i][0]
        return lst

    def name(self, lst: [BitVector]):
        maxonesincolumn = 0
        maxzeroesincolumn = 0

        tmpzeroesname = ''
        tmponesname = ''
        for col in range(len(self.input_names)):
            tmpones = 0
            tmpzeroes = 0
            for row in range(len(lst)):
                if lst[row][col] == 0:
                    tmpzeroes += 1
                else:
                    tmpones += 1
            if tmpones > maxonesincolumn:
                maxonesincolumn = tmpones
                tmponesname = self.input_names[col]
            if tmpzeroes > maxzeroesincolumn:
                maxzeroesincolumn = tmpzeroes
                tmpzeroesname = '!' + self.input_names[col]
        if maxzeroesincolumn > maxonesincolumn:
            pass
            #print(f'{maxzeroesincolumn}\t{tmpzeroesname}')
        else:
            pass
            #print(f'{maxonesincolumn}\t{tmponesname}')

    def build_pull_down_network(self):
        if self.is_inverting_needed():
            self.truth_table = self.truth_table.invert()
            self.inverted = True
        original_row_list = self.list_of_tuples_to_list_of_bitvectors(self.truth_table.get_rows_by_value(0))
        cp_list = original_row_list.copy()
        return cp_list


