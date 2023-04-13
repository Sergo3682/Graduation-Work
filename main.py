from truthtable import TruthTable
from bitvector import BitVector
from schematicbuilder import SchematicBuilder
from generator import Generator
import yaml
import argparse

if __name__ == '__main__':

    out_file = 'netlist.sp'
    spice_lib = '~/VSU224_Sky130_fd_pr/models/sky130.lib.spice'
    cfg = {}
    with open('spgen_cfg.yml') as fd_cfg:
        cfg = yaml.load(fd_cfg, Loader=yaml.SafeLoader)
    bv = BitVector(0b10010110, 8)
    tt = TruthTable(bv, ['CI', 'A', 'B'])

    sb = SchematicBuilder(tt)
    sb.build_pull_down_network()
    sb.build_pull_up_network()

    gen = Generator(out_file, sb, spice_lib, cfg)
    gen.generate_subcircuit()
    gen.test_single_subckt()