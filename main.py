from truthtable import TruthTable
from bitvector import BitVector
from schematicbuilder import SchematicBuilder
from generator import Generator
from helpers import log_2
import yaml
import argparse


def gen_input_name(bv_size):
    res = []
    j = ord('A')
    for i in range(log_2(bv_size)):
        res.append(chr(j + i))
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

# todo generator_init function
def generator_init():
    pass

if __name__ == '__main__':
    parser = parser_init()

    input_args = parser.parse_args()
    spice_lib = input_args.spice_lib_path

    with open(input_args.cfg) as fd_cfg:
        cfg = yaml.load(fd_cfg, Loader=yaml.SafeLoader)

    if (input_args.gen_cell is not None) and (input_args.gen_lib is not None):
        raise KeyError(f"You can't generate single circuit and whole library at the same time")

    elif input_args.gen_cell is not None:
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
        gen.generate_subcircuit(input_args.gen_cell)
        fd_test = open(f'test.sp', 'w')
        gen.test_single_subckt(fd_test, input_args.gen_cell)
        fd_test.close()

    elif input_args.gen_lib is not None:
        max_input = input_args.gen_lib
        # todo this
