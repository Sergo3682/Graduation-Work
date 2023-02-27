from serialnodes import SerialNodes


class NodeImage:
    def __init__(self):
        self.name = ''
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

    def align_node(self):
        maxnamelen = 0
        space = ' '
        for i in self.assets:
            maxnamelen = max(maxnamelen, len(i[1]))
        for i in self.assets:
            if len(i[1]) <= maxnamelen:
                j = 0
                for j in range(len(i)):
                    padding = maxnamelen - len(i[j])
                    i[j] = padding*space + i[j]

    def print_node(self):
        for i in self.assets:
            for j in i:
                print(j)

    def get_node_image(self):
        return self.assets
