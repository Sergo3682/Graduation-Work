from net import Net
from serialnodes import SerialNodes
from helpers import width_of_circuit
from image_node import *
from image_net import *

N_Q = Net()
n01 = Net()
n02 = Net()
n03 = Net()

n02.node_lists = [SerialNodes(['D']), SerialNodes(['!D', 'E'])]
n03.node_lists = [SerialNodes(['E']), SerialNodes(['!E', 'F'])]

n01.node_lists = [SerialNodes(['!B', 'C'], n02), SerialNodes(['B', '!C']), SerialNodes(['D'], n03)]

N_Q.node_lists = [SerialNodes(['A'], n01)]
