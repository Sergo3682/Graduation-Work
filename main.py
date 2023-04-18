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


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Digital library compiler')
    parser.add_argument('-c', '--cfg', type=str, default='spgen_cfg.yml',
                        help='set custom config file (default: spgen_cfg.yml)')
    parser.add_argument('-o', '--out', type=str, default='netlist.sp',
                        help='set custom output file (default: netlist.sp)')
    parser.add_argument('--gen_cell', type=str, default=None,
                        help='generate single cell for custom bitvector')
    parser.add_argument('--input_names', type=str, default=None,
                        help='set custom input names for a single cell')
    parser.add_argument('-spice_lib_path', '--spice_lib_path', type=str,
                        default='~/VSU224_Sky130_fd_pr/models/sky130.lib.spice',
                        help='set custom path to spice library for circuit simulation')
    #todo gen_lib 3
    #todo parser_init function
    #todo generator_init function
    input_args = parser.parse_args()
    spice_lib = input_args.spice_lib_path
    with open(input_args.cfg) as fd_cfg:
        cfg = yaml.load(fd_cfg, Loader=yaml.SafeLoader)

    if input_args.gen_cell is not None:
        val = int(input_args.gen_cell, 2)
        num_of_inputs = log_2(len(input_args.gen_cell))
        bv = BitVector(val, len(input_args.gen_cell))
        if input_args.input_names is not None:
            input_names = list(input_args.input_names.split(", "))
        else:
            input_names = gen_input_name(bv.size)
        tt = TruthTable(bv, input_names)

    if (input_args.gen_cell is not None) and (input_args.gen_lib is not None):
        raise KeyError(f"You can't generate single circuit and whole library at the same time")

    sb = SchematicBuilder(tt)
    sb.build_pull_down_network()
    sb.build_pull_up_network()

    gen = Generator(input_args.out, sb, spice_lib, cfg)
    gen.generate_subcircuit()
    gen.test_single_subckt()
