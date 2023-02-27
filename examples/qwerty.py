from net import Net
from serialnodes import SerialNodes
from helpers import numbers_of_branches


n01 = Net()
alist = SerialNodes(['A'], n01)
N_Q = Net(alist)

n02 = Net()
rlist1 = SerialNodes(['B', '!C'])
llist1 = SerialNodes(['!B', 'C'], n02)
n01.node_lists = [rlist1, llist1]

llist2 = SerialNodes(['D'])
rlist2 = SerialNodes(['!D', 'E'])
n02.node_lists = [llist2, rlist2]





