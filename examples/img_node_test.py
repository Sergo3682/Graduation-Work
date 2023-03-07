from serialnodes import SerialNodes
from net import Net
from helpers import width_of_circuit
from image_node import NodeImage

one = SerialNodes(['A'])
two = SerialNodes(['!A', 'B'])
many = SerialNodes(['Q', 'WER', 'OMEGA', 'BOOM', '!E'])

n01 = Net()
n02 = Net()
n03 = Net()
n01.node_lists = [one]
n02.node_lists = [two]
n03.node_lists = [many]