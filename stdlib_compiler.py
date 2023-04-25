#!/usr/bin/env python3

from truthtable import TruthTable
from bitvector import BitVector
from schematicbuilder import SchematicBuilder
from generator import Generator
from helpers import log_2, two_to_the_power_of
import yaml
import argparse
import logging as log
log.basicConfig(level=log.DEBUG)


def gen_input_name(bv_size):
    res = []
    char_ascii = ord('A')
    for num in range(log_2(bv_size)):
        res.append(chr(char_ascii + num))
    return res


def parser_init():
    out_parser = argparse.ArgumentParser(description='Standard Cell Digital Library Compiler')
    out_parser.add_argument(
        '-c',
        '--config',
        dest='config',
        type=str,
        default='spgen_cfg.yml',
        help='set custom config file (default: spgen_cfg.yml)'
    )
    out_parser.add_argument(
        '-o',
        '--out',
        dest='netlist',
        type=str,
        default='netlist.sp',
        help='set output netlist file (default: netlist.sp)'
    )
    out_parser.add_argument(
        '--gen_cell',
        dest='bit_vector',
        type=str,
        default=None,
        help='generate single cell for custom bitvector (e.g. 1001)'
    )
    out_parser.add_argument(
        '--input_names',
        type=str, default=None,
        help='set custom input names for a single cell'
    )
    out_parser.add_argument(
        '-spice_lib_path',
        '--spice_lib_path',
        type=str,
        default='~/VSU224_Sky130_fd_pr/models/sky130.lib.spice',
        help='set custom path to spice library for circuit simulation'
    )
    out_parser.add_argument(
        '-l',
        '--gen_lib',
        dest='max_inputs',
        type=int,
        default=None,
        help='generate subcircuits for a whole library'
    )
    return out_parser


if __name__ == '__main__':
    parser = parser_init()

    # grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    # red = "\x1b[31;20m"
    # bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"

    input_args = parser.parse_args()
    spice_lib = input_args.spice_lib_path

    with open(input_args.config) as fd_cfg:
        cfg = yaml.load(fd_cfg, Loader=yaml.SafeLoader)

    if (input_args.bit_vector is not None) and (input_args.max_inputs is not None):
        raise KeyError(f"You can't generate single circuit and whole library at the same time")

    elif input_args.bit_vector is not None:
        fd = open(input_args.netlist, 'w')
        fd.close()
        val = int(input_args.bit_vector, 2)
        num_of_inputs = log_2(len(input_args.bit_vector))
        bv = BitVector(val, len(input_args.bit_vector))
        if input_args.input_names is not None:
            input_names = list(input_args.input_names.split(", "))
        else:
            input_names = gen_input_name(bv.size)
        tt = TruthTable(bv, input_names)
        sb = SchematicBuilder(tt)
        sb.build_pull_down_network()
        if sb.is_useless():
            log.warning(yellow + "Current cell is useless." + reset)
        sb.build_pull_up_network()

        name = cfg['cell_name_tpl'].format(bit_vector=input_args.bit_vector, inputs_num=len(input_names))

        gen = Generator(input_args.netlist, sb, spice_lib, cfg)
        fd = gen.generate_subcircuit(name)
        fd.close()

        fd_test = open(f'test.sp', 'w')

        gen.test_single_subckt(fd_test, name)
        fd_test.close()

    elif input_args.max_inputs is not None:
        log.info(f'Generating library with maximum inputs num {input_args.max_inputs}...')
        fd = open(input_args.netlist, 'w')
        fd.close()
        max_input = input_args.max_inputs
        for i in range(1, max_input + 1):
            size = two_to_the_power_of(i)
            for j in range(two_to_the_power_of(size)):
                bv = BitVector(j, size)
                tt = TruthTable(bv, gen_input_name(size))
                sb = SchematicBuilder(tt)
                sb.build_pull_down_network()
                if not sb.is_useless():
                    sb.build_pull_up_network()
                    gen = Generator(input_args.netlist, sb, spice_lib, cfg)
                    name = cfg['cell_name_tpl'].format(bit_vector=format(j, '#0%db' % (size + 2, )),
                                                       inputs_num=len(tt.input_names))
                    fd = gen.generate_subcircuit(name)
                else:
                    log.warning(yellow + 'Current cell is useless; passed' + reset)
        fd.close()
    else:
        parser.print_help()
