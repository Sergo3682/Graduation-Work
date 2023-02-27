from net import Net
from serialnodes import SerialNodes
from helpers import numbers_of_branches

N_Q = Net()
n01 = Net()
n02 = Net()
n03 = Net()

n02.node_lists = [SerialNodes(['D'])]
n01.node_lists = [SerialNodes(['B'], n02), SerialNodes(['C'], n02)]

N_Q.node_lists = [SerialNodes(['A'], n01)]
