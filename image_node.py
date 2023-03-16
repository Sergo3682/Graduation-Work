from serialnodes import SerialNodes


class NodeImage:
    def __init__(self):
        self.name = None
        self.assets = []

    def gen_trans_image(self, name: str):
        img = []
        img.append(f'    |')
        img.append(f'{name} [ ')
        if len(img[1]) < len(img[0]):
            img[1] = ' ' + img[1]
        img.append(f'    |')
        return img

    def gen_node_image(self, branch: SerialNodes):
        self.name = branch
        self.assets = []
        for i in branch.nodes:
            self.assets.append(self.gen_trans_image(i))
            self.align_node()
        self.add_gnd()
        self.margin_left()

    def align_node(self):
        maxnamelen = 0
        space = ' '
        for i in self.assets:
            maxnamelen = max(maxnamelen, len(i[1]))
        for i in self.assets:
            if len(i[1]) <= maxnamelen:
                for j in range(len(i)):
                    padding = maxnamelen - len(i[j])
                    i[j] = padding * space + i[j]

    def add_gnd(self):
        if self.name.next_net is None:
            self.assets.append([(len(self.assets[0][2]) - 1) * ' ' + '-', len(self.assets[0][2]) * ' ',
                                len(self.assets[0][2]) * ' '])

    def margin_left(self):
        width = 3
        for i in self.assets:
            for j in range(len(i)):
                i[j] = ' ' * width + '@' + i[j]

    def print_node(self):
        for i in self.assets:
            for j in i:
                print(j)

    def get_node_image(self):
        return self.assets
