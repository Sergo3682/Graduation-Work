from net import Net
from serialnodes import SerialNodes
from image_node import *
from image_net import *
from schematicdrawer import *
from net_walker import NetWalker


N_Q = Net()
n01 = Net()
n02 = Net()
n03 = Net()
n04 = Net()
n05 = Net()
n06 = Net()
n07 = Net()
n08 = Net([SerialNodes(['O']), SerialNodes(['!O'])])

#n08.node_lists = [SerialNodes(['O']), SerialNodes(['!O'])]
n07.node_lists = [SerialNodes(['Y']), SerialNodes(['!Y'])]
n06.node_lists = [SerialNodes(['Y'], n08), SerialNodes(['!Y'])]
n05.node_lists = [SerialNodes(['Y']), SerialNodes(['!Y'])]
n04.node_lists = [SerialNodes(['F', 'O'], n05), SerialNodes(['E']), SerialNodes(['!F', 'E'], n06)]
n03.node_lists = [SerialNodes(['F', 'O'], n07), SerialNodes(['!O'])]
n02.node_lists = [SerialNodes(['D', 'E']), SerialNodes(['!D', '!E'], n03)]
n01.node_lists = [SerialNodes(['B'], n02), SerialNodes(['!B', 'C']), SerialNodes(['C', 'D'], n04)]
N_Q.node_lists = [SerialNodes(['A'], n01)]