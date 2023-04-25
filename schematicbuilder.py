from truthtable import TruthTable
from bitvector import BitVector
from net import Net
from helpers import two_to_the_power_of
from serialnodes import SerialNodes
from net_walker import NetWalker
import logging as log


class SchematicBuilder:
    def __init__(self, input_truth_table: TruthTable):
        self.bitvector = input_truth_table.out_vec
        self.old_truth_table = input_truth_table
        self.truth_table = input_truth_table
        self.inverted = False

        self.input_names = self.truth_table.input_names.copy()
        self.input_names.reverse()

        self.pd_netlist = [Net()]
        self.pu_netlist = [Net()]
        log.debug(f'{self.__class__.__name__}: BitVector: {self.bitvector}')

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
        return (n01 + n10) < (n00 + n11)

    @staticmethod
    def list_of_tuples_to_list_of_bitvectors(lst: list):
        for i in range(len(lst)):
            lst[i] = lst[i][0]
        return lst

    def algorithm(self, lst: [BitVector], names: [str], idx, network: str):
        if not self.complete_set_of_combination(lst):
            netlist = []
            if network == 'pull_down':
                netlist = self.pd_netlist
            elif network == 'pull_up':
                netlist = self.pu_netlist

            if len(lst) == 1:
                netlist[idx].node_lists.append(SerialNodes(self.gen_one_line_branch(lst[0], names, network), None))
                netlist[idx].id = f'{network[5]}{idx}'
                return

            max_name = ''
            max_ones_in_column = 0
            max_zeroes_in_column = 0
            tmp_zeroes_name = ''
            tmp_ones_name = ''
            lst_copy = lst.copy()

            for col in range(lst[0].size-1, -1, -1):
                tmp_ones = 0
                tmp_zeroes = 0
                for row in range(len(lst)):
                    if lst[row][col] == 0:
                        tmp_zeroes += 1
                    else:
                        tmp_ones += 1
                if tmp_ones > max_ones_in_column:
                    max_ones_in_column = tmp_ones
                    if network == 'pull_down':
                        tmp_ones_name = names[col]
                    elif network == 'pull_up':
                        tmp_ones_name = '!' + names[col]
                if tmp_zeroes > max_zeroes_in_column:
                    max_zeroes_in_column = tmp_zeroes
                    if network == 'pull_down':
                        tmp_zeroes_name = '!' + names[col]
                    elif network == 'pull_up':
                        tmp_zeroes_name = names[col]
            netlist.append(Net())

            if network == 'pull_down':
                if max_zeroes_in_column > max_ones_in_column:
                    max_name = tmp_zeroes_name
                    tmp_name = max_name
                    if max_name[0] == '!':
                        tmp_name = max_name[1:]
                    lst_copy = self.grouping(lst_copy, names.index(tmp_name), 0)
                    for i in lst_copy:
                        lst.remove(i)
                    lst_copy = self.list_of_bv_idx_removing(lst_copy, names.index(tmp_name))
                else:
                    max_name = tmp_ones_name
                    tmp_name = max_name
                    if max_name[0] == '!':
                        tmp_name = max_name[1:]
                    lst_copy = self.grouping(lst_copy, names.index(tmp_name), 1)
                    for i in lst_copy:
                        lst.remove(i)
                    lst_copy = self.list_of_bv_idx_removing(lst_copy, names.index(tmp_name))

            if network == 'pull_up':
                if max_zeroes_in_column >= max_ones_in_column:
                    max_name = tmp_zeroes_name
                    tmp_name = max_name
                    if max_name[0] == '!':
                        tmp_name = max_name[1:]
                    lst_copy = self.grouping(lst_copy, names.index(tmp_name), 0)
                    for i in lst_copy:
                        lst.remove(i)
                    lst_copy = self.list_of_bv_idx_removing(lst_copy, names.index(tmp_name))
                else:
                    max_name = tmp_ones_name
                    tmp_name = max_name
                    if max_name[0] == '!':
                        tmp_name = max_name[1:]
                    lst_copy = self.grouping(lst_copy, names.index(tmp_name), 1)
                    for i in lst_copy:
                        lst.remove(i)
                    lst_copy = self.list_of_bv_idx_removing(lst_copy, names.index(tmp_name))

            netlist[idx].node_lists.append(SerialNodes([f'{max_name}'], netlist[len(netlist)-1]))

            netlist[idx].id = f'{network[5]}{idx}'

            if max_name[0] == '!':
                max_name = max_name[1:]

            names_copy = names.copy()
            names_copy.remove(max_name)

            self.algorithm(lst_copy, names_copy, len(netlist) - 1, network)
            if len(lst) == 1:
                netlist[idx].node_lists.append(SerialNodes(self.gen_one_line_branch(lst[0], names, network), None))

            if len(lst) > 1:
                self.algorithm(lst, names, idx, network)

    @staticmethod
    def gen_one_line_branch(bv: BitVector, names, network):
        nodes = []
        for i in range(bv.size-1, -1, -1):
            if network == 'pull_down':
                if bv[i] == 1:
                    nodes.append(names[i])
                else:
                    nodes.append('!' + names[i])
            elif network == 'pull_up':
                if bv[i] == 0:
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
        if len(lst) == 0:
            return ans
        checker = False
        for num in range(two_to_the_power_of(lst[0].size)):
            for bv in lst:
                if num == bv.val:
                    checker = True
            ans = ans and checker
            checker = False
        return ans

    @staticmethod
    def next_net_fixer(lst):
        for net in lst:
            for node in net.node_lists:
                if node.next_net == Net([]):
                    node.next_net = None

    def build_pull_down_network(self):
        log.debug('Building pull-down network...')
        if self.is_inverting_needed():
            self.truth_table = self.truth_table.invert()
            self.inverted = True
            log.info('Inversion is needed')
        original_row_list = self.list_of_tuples_to_list_of_bitvectors(self.truth_table.get_rows_by_value(0))
        cp_list = original_row_list.copy()
        self.algorithm(cp_list, self.input_names, 0, 'pull_down')
        self.next_net_fixer(self.pd_netlist)

    def build_pull_up_network(self):
        log.debug('Building pull-up network...')
        original_row_list = self.list_of_tuples_to_list_of_bitvectors(self.truth_table.get_rows_by_value(1))
        cp_list = original_row_list.copy()
        self.algorithm(cp_list, self.input_names, 0, 'pull_up')
        self.next_net_fixer(self.pu_netlist)

    def __repr__(self):
        return f'{self.__class__.__name__}({self.truth_table.__repr__()})'

    @staticmethod
    def get_inverted_inputs(origin_net, res_lst):
        for sn in origin_net.node_lists:
            for inst in sn.nodes:
                if inst[0] == '!' and inst[1:] not in res_lst:
                    res_lst.append(inst[1:])

    @staticmethod
    def is_name_in_serial_node(sn: SerialNodes, name: str, prev_checker: list):
        for node in sn.nodes:
            prev_checker[-1] = prev_checker[-1] or (name in node)

    def is_useless(self):
        checker = []
        nw = NetWalker()
        for name in self.input_names:
            checker.append(False)
            nw.walk(
                net=self.pd_netlist[0],
                sn_action_fn=self.is_name_in_serial_node,
                sn_fn_kwargs={'name': name, 'prev_checker': checker}
            )
        res = True
        for statement in checker:
            res = res and statement
        return not res

