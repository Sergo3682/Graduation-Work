from truthtable import TruthTable


class SchematicBuilder:
    def __init__(self, input_truth_table: TruthTable):
        self.truth_table = input_truth_table

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
