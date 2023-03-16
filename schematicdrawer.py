from image_net import *
from serialnodes import SerialNodes


def get_serial_node_width(node: SerialNodes):
    width = 1
    nets = [node.next_net]
    if nets[0] is not None:
        if (len(nets[0].node_lists) % 2) != 0:
            width -= 1
        while len(nets) > 0:
            for nodes in nets[0].node_lists:
                print(nodes)
                width += 1
                if nodes.next_net is not None:
                    nets.append(nodes.next_net)
            nets.pop(0)
    return width

def get_list_of_widths_by_net(net: Net):
    lst = []
    for nodes in net.node_lists:
        lst.append(get_serial_node_width(nodes))
    return lst


class SchematicDrawer:
    def __init__(self, root: Net = None):
        self.list_of_nets = []
        self.schematic_assets_list = []
        self.root = None
        if root is not None:
            self.sort_nets_by_level(root)
            self.root = root

    def __repr__(self):
        return f'{self.__class__.__name__}({self.root})'

    def sort_nets_by_level(self, root: Net):
        order = []
        order.append(root)
        self.list_of_nets = []
        self.list_of_nets.append([root])
        while len(order) > 0:
            next_lvl_counter = 0
            for i in self.list_of_nets[-1]:
                next_lvl_counter += 1
            self.list_of_nets.append([])
            for i in range(next_lvl_counter):
                for node in order[0].node_lists:
                    if node.next_net is not None:
                        order.append(node.next_net)
                        self.list_of_nets[-1].append(node.next_net)
                order.pop(0)
        for i in range(len(self.list_of_nets)):
            if len(self.list_of_nets[i]) == 0:
                self.list_of_nets.pop(i)
        self.schematic_assets_list = self.list_of_nets.copy()

    def memes(self):
        print('купил мужик шляпу, надел, а она ему как раз\n')
