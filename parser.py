from schematicbuilder import SchematicBuilder
from serialnodes import SerialNodes
from net import Net
from elems import Instance
from net_walker import NetWalker


class Parser:
    def __init__(self, output_file: str, builder: SchematicBuilder, lib: str):
        self.output_file_name = self.pd_root = self.pu_root = self.lib = None
        if output_file is not None:
            self.output_file_name = output_file
            self.fd = open(self.output_file_name, 'w')
        if builder is not None:
            self.pd_root = builder.pd_netlist[0]
            self.pu_root = builder.pu_netlist[0]
            self.builder = builder
        if lib is not None:
            self.lib = '.lib ' + lib + ' tt'
            self.nfet = 'sky130_fd_pr__nfet_g5v0d10v5 w=20 l=3'
            self.pfet = 'sky130_fd_pr__pfet_g5v0d10v5 w=60 l=3'
        self.pd_instances = []
        self.name_idx = 0

    def __repr__(self):
        return f'{self.__class__.__name__}({self.output_file_name}, {self.builder.__repr__()})'

    # def not_creating(self):
    #     res = []
    #     nw = NetWalker(self.pd_root)
    #     print(f'{type(self.pd_root)}\t\t{self.pd_root}')
    #     nw.walk(self.pd_root, sn_action_fn=None, sn_fn_kwargs=None, net_action_fn=self.builder.get_inverted_inputs,
    #             net_fn_kwargs={'res_lst': res})
    #     nw.walk(self.pu_root, sn_action_fn=None, sn_fn_kwargs=None, net_action_fn=self.builder.get_inverted_inputs,
    #             net_fn_kwargs={'res_lst': res})
    #     return res

    @staticmethod
    def is_single_instance(sn: SerialNodes):
        return len(sn.nodes) == 1

    @staticmethod
    def get_next_net(sn: SerialNodes):
        if sn.next_net is None:
            return '0'
        else:
            return f'{sn.next_net.id}'

    @staticmethod
    def not_converting(name: str):
        if name[0] == '!':
            return 'n' + name[1:]
        else:
            return name

    def spice_instances_filling(self, current_net: Net):
        for i in range(len(current_net.node_lists)):
            if self.is_single_instance(current_net.node_lists[i]):
                inst_type = 'X'
                name = f'M{self.name_idx}'
                nxt_net = self.get_next_net(current_net.node_lists[i])
                tran_name = self.not_converting(current_net.node_lists[i].nodes[0])
                cons = [current_net.id, tran_name, nxt_net, '0']
                self.name_idx += 1
                self.pd_instances.append(Instance(inst_type, name, cons, self.nfet))
            else:
                print('dude')



    def parse(self):
        self.fd.write(self.lib)
        self.fd.close()
