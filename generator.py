from schematicbuilder import SchematicBuilder
from serialnodes import SerialNodes
from net import Net
from elems import Instance
from net_walker import NetWalker


class Generator:
    def __init__(self, output_file: str, builder: SchematicBuilder, lib: str, config: dict):
        self.cfg = config
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
            self.nfet = config["nmos"] + f' w={config["default_nmos_w"]}' + f' l={config["default_nmos_l"]}'
            self.pfet = config["pmos"] + f' w={config["default_pmos_w"]}' + f' l={config["default_pmos_l"]}'
        self.spice_instances = []
        self.not_list = []
        self.name_idx = 0

    def __repr__(self):
        return f'{self.__class__.__name__}({self.output_file_name}, {self.builder.__repr__()})'

    @staticmethod
    def is_single_instance(sn: SerialNodes):
        return len(sn.nodes) == 1

    @staticmethod
    def get_next_net(sn: SerialNodes, pin):
        if sn.next_net is None:
            return pin
        else:
            return f'{sn.next_net.id}'

    def not_converting(self, name: str):
        if name[0] == '!':
            if 'n' + name[1:] not in self.not_list:
                self.not_list.append('n' + name[1:])
            return 'n' + name[1:]
        else:
            return name

    def spice_instances_filling(self, current_net: Net, bulk, supply_pin, model):
        for i in range(len(current_net.node_lists)):
            if self.is_single_instance(current_net.node_lists[i]):
                name = f'M{self.name_idx}'
                nxt_net = self.get_next_net(current_net.node_lists[i], supply_pin)
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
                        nxt_net = self.get_next_net(current_net.node_lists[i], supply_pin)
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

    def gen_not(self, gnd, vdd, nmos_bulk, pmos_bulk):
        for name in self.not_list:
            instance_name = f'M{self.name_idx}'
            self.name_idx += 1
            cons = [name, name[1:], gnd, nmos_bulk]
            pd_not = Instance('X', instance_name, cons, self.nfet)
            self.spice_instances.append(pd_not)
            print(pd_not, file=self.fd)

            instance_name = f'M{self.name_idx}'
            self.name_idx += 1
            cons = [name, name[1:], vdd, pmos_bulk]
            pu_not = Instance('X', instance_name, cons, self.pfet)
            self.spice_instances.append(pu_not)
            print(pu_not, file=self.fd)

    def gen_supply(self, vdd, gnd, stream):
        vdd_name = f'{self.name_idx}'
        self.name_idx += 1
        cons = [vdd, '0']
        val = 'DC 5'
        vdd = Instance('V', vdd_name, cons, model=None, value=val)
        self.spice_instances.append(vdd)
        print(vdd, file=stream)

        vdd_name = f'{self.name_idx}'
        self.name_idx += 1
        cons = [gnd, '0']
        val = 'DC 0'
        gnd_sup = Instance('V', vdd_name, cons, model=None, value=val)
        self.spice_instances.append(gnd_sup)
        print(gnd_sup, file=stream)

    def gen_pulse(self, gnd, stream):
        period = 50
        input_names = self.builder.truth_table.input_names.copy()
        input_names.reverse()
        for i_n in input_names:
            pw, period = period, period * 2
            name = f'in{i_n}{self.name_idx}'
            self.name_idx += 1
            cons = [i_n, gnd]
            val = f'PULSE (0 5 {pw}n 2n 2n {pw}n {period}n)'
            self.spice_instances.append(Instance('V', name, cons, model=None, value=val))
            print(self.spice_instances[-1], file=stream)
        return period

    def gen_control(self, tstep, tstop, stream):
        print('.control', file=stream)
        print(f'tran {tstep}n {tstop}n', file=stream)
        stream.write('plot')
        for names in self.builder.truth_table.input_names:
            stream.write(' ' + names)
        stream.write('\n')
        print('plot Q', file=stream)
        print('.endc', file=stream)

    def gen_out_not(self, gnd, vdd, nmos_bulk, pmos_bulk):
        instance_name = f'M{self.name_idx}'
        self.name_idx += 1
        cons = ['Q', 'nQ', gnd, nmos_bulk]
        pd_not = Instance('X', instance_name, cons, self.nfet)
        self.spice_instances.append(pd_not)

        instance_name = f'M{self.name_idx}'
        self.name_idx += 1
        cons = ['Q', 'nQ', vdd, pmos_bulk]
        pu_not = Instance('X', instance_name, cons, self.pfet)
        self.spice_instances.append(pu_not)

    def generate_subcircuit(self):
        # print(self.lib, file=self.fd)
        gnd = self.cfg["ground_pin"]
        vdd = self.cfg["power_pin"]
        nmos_bulk = self.cfg["nmos_bulk_pin"]
        pmos_bulk = self.cfg["pmos_bulk_pin"]
        nw = NetWalker()
        nw.walk(self.pd_root, sn_action_fn=None, sn_fn_kwargs=None, net_action_fn=self.spice_instances_filling,
                net_fn_kwargs={'bulk': nmos_bulk, 'supply_pin': gnd, 'model': self.nfet})
        nw.walk(self.pu_root, sn_action_fn=None, sn_fn_kwargs=None, net_action_fn=self.spice_instances_filling,
                net_fn_kwargs={'bulk': pmos_bulk, 'supply_pin': vdd, 'model': self.pfet})

        if self.builder.inverted:
            for inst in self.spice_instances:
                inst.replace_cons(f'{self.pd_root.id}', 'nQ')
                inst.replace_cons(f'{self.pu_root.id}', 'nQ')
            self.gen_out_not(gnd, vdd, nmos_bulk, pmos_bulk)
        else:
            for inst in self.spice_instances:
                inst.replace_cons(f'{self.pd_root.id}', 'Q')
                inst.replace_cons(f'{self.pu_root.id}', 'Q')

        self.fd.write(f'.subckt bv_{self.builder.bitvector.val} Q')
        for i in self.builder.truth_table.input_names:
            self.fd.write(f' {i}')
        print(f' {vdd} {gnd} {nmos_bulk} {pmos_bulk}', file=self.fd)

        for inst in self.spice_instances:
            print(inst, file=self.fd)

        self.fd.write('\n')
        self.gen_not(gnd, vdd, nmos_bulk, pmos_bulk)
        print(f'Number of transistors: {self.name_idx}')
        print('.ends', file=self.fd)
        self.fd.close()

    def test_single_subckt(self):
        vdd= 'VDD'
        gnd = 'VSS'
        nmos_bulk = gnd
        pmos_bulk = vdd
        fd_test = open(f'test_{self.output_file_name}', 'w')
        print(self.lib, file=fd_test)
        print(f'.include {self.output_file_name}', file=fd_test)
        self.gen_supply(self.cfg["power_pin"], self.cfg["ground_pin"], fd_test)

        cons = ['Q']
        for i in self.builder.truth_table.input_names:
            cons.append(i)
        cons.append(vdd)
        cons.append(gnd)
        cons.append(nmos_bulk)
        cons.append(pmos_bulk)
        sbckt = Instance('X', f'S{self.name_idx}', cons, f'bv_{self.builder.bitvector.val}')
        self.name_idx += 1
        print(sbckt, file=fd_test)

        tstop = self.gen_pulse(self.cfg["ground_pin"], fd_test)
        fd_test.write('\n')
        self.gen_control(1, tstop, fd_test)
        print('.end', file=fd_test)
        fd_test.close()