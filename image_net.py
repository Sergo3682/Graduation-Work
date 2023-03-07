from net import Net
from image_node import NodeImage


class NetImage:
    def __init__(self, net: Net = None):
        self.name = ''
        self.assets = []
        self.aligned = False
        if net is not None:
            self.gen_net_image(net)

    def __repr__(self):
        return f'{self.__class__.__name__}({self.name})'

    def gen_net_image(self, net: Net):
        self.name = str(net)
        self.assets = []
        branch = []
        printer = NodeImage()
        maxlen = 0
        for node in net.node_lists:
            printer.gen_node_image(node)
            branch.append(printer.get_node_image())
            maxlen = max(maxlen, len(branch[len(branch)-1]))
        img = [''] * (maxlen*3+1)
        img[0] = '!'
        for b in branch:
            for i in range(len(b)):
                for j in range(len(b[i])):
                    img[1+i*3+j] += b[i][j]
            for j in range(len(img)-1, len(b)*3, -1):
                img[j] += ' ' * len(b[0][0])         #'~'
        self.assets = img
        self.aligned = False
        self.align_net()

    def get_net_image(self):
        return self.assets

    def print_net_image(self):
        for s in self.assets:
            print(s)

    def align_net(self):
        if self.aligned:
            return 'This net is already aligned!'

        first_trans_idx = self.assets[2].find('[')
        connectors_len = (len(self.assets[2]) - first_trans_idx - 2) // 2
        self.assets[0] = (first_trans_idx + 1) * ' ' + connectors_len * '_' + self.assets[0] + connectors_len * '_'
        self.aligned = True
