from image_net import *


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
        self.gen_schematic_image()

    def gen_schematic_image(self):
        for i in range(len(self.schematic_assets_list)):
            for j in range(len(self.schematic_assets_list[i])):
                generator = NetImage(self.schematic_assets_list[i][j])
                self.schematic_assets_list[i][j] = generator.get_net_image()
