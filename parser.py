from schematicbuilder import SchematicBuilder
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
            self.lib = '.lib ' + lib
            self.nfet = 'sky130_fd_pr__nfet_g5v0d10v5 w=1 l=1'
            self.pfet = 'sky130_fd_pr__pfet_g5v0d10v5 w=1 l=1'

    def __repr__(self):
        return f'{self.__class__.__name__}({self.output_file_name}, {self.builder.__repr__()})'

    def not_creating(self):
        res = []
        nw = NetWalker(self.pd_root)
        print(f'{type(self.pd_root)}\t\t{self.pd_root}')
        nw.walk(self.pd_root, sn_action_fn=None, sn_fn_kwargs=None, net_action_fn=self.builder.get_inverted_inputs,
                net_fn_kwargs={'res_lst': res})
        nw.walk(self.pu_root, sn_action_fn=None, sn_fn_kwargs=None, net_action_fn=self.builder.get_inverted_inputs,
                net_fn_kwargs={'res_lst': res})
        return res

    def parse(self):
        self.fd.write(self.lib)
        self.fd.close()
