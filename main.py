from truthtable import TruthTable
from bitvector import BitVector
from schematicbuilder import SchematicBuilder
from generator import Generator
from helpers import log_2, two_to_the_power_of
import yaml
import argparse


def gen_input_name(bv_size):
    res = []
    char_ascii = ord('A')
    for num in range(log_2(bv_size)):
        res.append(chr(char_ascii + num))
    return res

def parser_init():
    out_parser = argparse.ArgumentParser(description='Digital library compiler')
    out_parser.add_argument('-c', '--cfg', type=str, default='spgen_cfg.yml',
                        help='set custom config file (default: spgen_cfg.yml)')
    out_parser.add_argument('-o', '--out', type=str, default='netlist.sp',
                        help='set custom output file (default: netlist.sp)')
    out_parser.add_argument('--gen_cell', type=str, default=None,
                        help='generate single cell for custom bitvector')
    out_parser.add_argument('--input_names', type=str, default=None,
                        help='set custom input names for a single cell')
    out_parser.add_argument('-spice_lib_path', '--spice_lib_path', type=str,
                        default='~/VSU224_Sky130_fd_pr/models/sky130.lib.spice',
                        help='set custom path to spice library for circuit simulation')
    out_parser.add_argument('-lib', '--gen_lib', type=int, default=None,
                        help='generate subcircuits for a whole library')
    return out_parser


if __name__ == '__main__':
    parser = parser_init()

    input_args = parser.parse_args()
    spice_lib = input_args.spice_lib_path

    with open(input_args.cfg) as fd_cfg:
        cfg = yaml.load(fd_cfg, Loader=yaml.SafeLoader)

    if (input_args.gen_cell is not None) and (input_args.gen_lib is not None):
        raise KeyError(f"You can't generate single circuit and whole library at the same time")

    elif input_args.gen_cell is not None:
        fd = open(input_args.out, 'w')
        fd.close()
        val = int(input_args.gen_cell, 2)
        num_of_inputs = log_2(len(input_args.gen_cell))
        bv = BitVector(val, len(input_args.gen_cell))
        if input_args.input_names is not None:
            input_names = list(input_args.input_names.split(", "))
        else:
            input_names = gen_input_name(bv.size)
        tt = TruthTable(bv, input_names)
        sb = SchematicBuilder(tt)
        sb.build_pull_down_network()
        sb.build_pull_up_network()

        gen = Generator(input_args.out, sb, spice_lib, cfg)
        fd = gen.generate_subcircuit(f'{hex(val)}_{bv.size}')
        fd.close()

        fd_test = open(f'test.sp', 'w')
        gen.test_single_subckt(fd_test, f'{hex(val)}_{bv.size}')
        fd_test.close()

    elif input_args.gen_lib is not None:
        fd = open(input_args.out, 'w')
        fd.close()
        max_input = input_args.gen_lib
        for i in range(1, max_input + 1):
            size = two_to_the_power_of(i)
            for j in range(two_to_the_power_of(size)):
                bv = BitVector(j, size)
                tt = TruthTable(bv, gen_input_name(size))
                sb = SchematicBuilder(tt)
                sb.build_pull_down_network()
                sb.build_pull_up_network()

                gen = Generator(input_args.out, sb, spice_lib, cfg)
                fd = gen.generate_subcircuit(f'{hex(bv.val)}_{bv.size}')
        fd.close()

        # todo: gen testbench for all subcircuits in lib
