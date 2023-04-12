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
        self.spice_instances = []
        self.not_list = []
        self.name_idx = 0

    def __repr__(self):
        return f'{self.__class__.__name__}({self.output_file_name}, {self.builder.__repr__()})'

    @staticmethod
    def is_single_instance(sn: SerialNodes):
        return len(sn.nodes) == 1

    @staticmethod
    def get_next_net(sn: SerialNodes, bulk):
        if sn.next_net is None:
            return bulk
        else:
            return f'{sn.next_net.id}'

    def not_converting(self, name: str):
        if name[0] == '!':
            if 'n' + name[1:] not in self.not_list:
                self.not_list.append('n' + name[1:])
            return 'n' + name[1:]
        else:
            return name

    def spice_instances_filling(self, current_net: Net, bulk, model):
        for i in range(len(current_net.node_lists)):
            if self.is_single_instance(current_net.node_lists[i]):
                name = f'M{self.name_idx}'
                nxt_net = self.get_next_net(current_net.node_lists[i], bulk)
                tran_name = self.not_converting(current_net.node_lists[i].nodes[0])
                cons = [current_net.id, tran_name, nxt_net, bulk]
                self.name_idx += 1
                self.spice_instances.append(Instance('X', name, cons, model))
            else:
                for inst in current_net.node_lists[i].nodes:
                    if current_net.node_lists[i].nodes.index(inst) == 0:
                        name = f'M{self.name_idx}'
                        self.name_idx += 1
                        nxt_net = current_net.id + '1'
                        tran_name = self.not_converting(inst)
                        cons = [current_net.id, tran_name, nxt_net, bulk]
                        self.spice_instances.append(Instance('X', name, cons, model))
                    elif current_net.node_lists[i].nodes.index(inst) == len(current_net.node_lists[i].nodes) - 1:
                        name = f'M{self.name_idx}'
                        self.name_idx += 1
                        nxt_net = self.get_next_net(current_net.node_lists[i], bulk)
                        tran_name = self.not_converting(inst)
                        cons = [current_net.id + f'{current_net.node_lists[i].nodes.index(inst)}', tran_name, nxt_net,
                                bulk]
                        self.spice_instances.append(Instance('X', name, cons, model))
                    else:
                        name = f'M{self.name_idx}'
                        self.name_idx += 1
                        nxt_net = current_net.id + f'{current_net.node_lists[i].nodes.index(inst) + 1}'
                        tran_name = self.not_converting(inst)
                        cons = [current_net.id + f'{current_net.node_lists[i].nodes.index(inst)}', tran_name, nxt_net,
                                bulk]
                        self.spice_instances.append(Instance('X', name, cons, model))

    def gen_not(self):
        for name in self.not_list:
            instance_name = f'M{self.name_idx}'
            self.name_idx += 1
            cons = [name, name[1:], '0', '0']
            pd_not = Instance('X', instance_name, cons, self.nfet)
            self.spice_instances.append(pd_not)
            print(pd_not, file=self.fd)

            instance_name = f'M{self.name_idx}'
            self.name_idx += 1
            cons = [name, name[1:], 'VCC', 'VCC']
            pu_not = Instance('X', instance_name, cons, self.pfet)
            self.spice_instances.append(pu_not)
            print(pu_not, file=self.fd)

    def gen_vcc(self):
        vcc_name = f'{self.name_idx}'
        self.name_idx += 1
        cons = ['VCC', '0']
        val = 'DC 5'
        vcc = Instance('V', vcc_name, cons, model=None, value=val)
        self.spice_instances.append(vcc)
        print(vcc, file=self.fd)

    def gen_pulse(self):
        period = 100
        input_names = self.builder.truth_table.input_names.copy()
        input_names.reverse()
        for i_n in input_names:
            pw, period = period, period * 2
            name = f'in{i_n}{self.name_idx}'
            self.name_idx += 1
            cons = [i_n, '0']
            val = f'PULSE (0 5 2n 2n 2n {pw}n {period}n)'
            self.spice_instances.append(Instance('V', name, cons, model=None, value=val))
            print(self.spice_instances[-1], file=self.fd)
        return period

    def gen_control(self, tstep, tstop):
        print('.control', file=self.fd)
        print(f'tran {tstep}n {tstop}n', file=self.fd)
        self.fd.write('plot')
        for names in self.builder.truth_table.input_names:
            self.fd.write(' ' + names)
        self.fd.write('\n')
        print('plot Q', file=self.fd)
        print('.endc', file=self.fd)

    def gen_out_not(self):
        instance_name = f'M{self.name_idx}'
        self.name_idx += 1
        cons = ['Q', 'nQ', '0', '0']
        pd_not = Instance('X', instance_name, cons, self.nfet)
        self.spice_instances.append(pd_not)

        instance_name = f'M{self.name_idx}'
        self.name_idx += 1
        cons = ['Q', 'nQ', 'VCC', 'VCC']
        pu_not = Instance('X', instance_name, cons, self.pfet)
        self.spice_instances.append(pu_not)

    def parse(self):
        print(self.lib, file=self.fd)
        gnd = '0'
        vcc = 'VCC'
        nw = NetWalker()
        nw.walk(self.pd_root, sn_action_fn=None, sn_fn_kwargs=None, net_action_fn=self.spice_instances_filling,
                net_fn_kwargs={'bulk': gnd, 'model': self.nfet})
        nw.walk(self.pu_root, sn_action_fn=None, sn_fn_kwargs=None, net_action_fn=self.spice_instances_filling,
                net_fn_kwargs={'bulk': vcc, 'model': self.pfet})

        if self.builder.inverted:
            for inst in self.spice_instances:
                inst.replace_cons(f'{self.pd_root.id}', 'nQ')
                inst.replace_cons(f'{self.pu_root.id}', 'nQ')
            self.gen_out_not()
        else:
            for inst in self.spice_instances:
                inst.replace_cons(f'{self.pd_root.id}', 'Q')
                inst.replace_cons(f'{self.pu_root.id}', 'Q')

        for inst in self.spice_instances:
            print(inst, file=self.fd)

        self.fd.write('\n')
        self.gen_not()
        print(f'Number of transistors: {self.name_idx}')
        self.gen_vcc()
        tstop = self.gen_pulse()
        self.fd.write('\n')
        self.gen_control(1, tstop)

        print('.end', file=self.fd)
        self.fd.close()
