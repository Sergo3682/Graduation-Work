from truthtable import TruthTable
from bitvector import BitVector
from schematicbuilder import SchematicBuilder
from image_net import NetImage
from parser import Parser

if __name__ == '__main__':
    bv = BitVector(0b00101101, 8)
    tt = TruthTable(bv, ['A', 'B', 'C'])
    sb = SchematicBuilder(tt)
    sb.build_pull_down_network()
    sb.build_pull_up_network()
