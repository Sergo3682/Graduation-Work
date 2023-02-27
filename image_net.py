from net import Net
from image_node import NodeImage
from helpers import insert


class NetImage:
    def __init__(self):
        self.name = ''
        self.assets = []
        self.aligned = False

    def gen_net_image(self, net: Net):
        self.name = net
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

        startlen = len(self.assets[1])
        padding = 3
        for i in range(1, len(self.assets), 1):
            for j in range(startlen, 0, -1):
                if (j < startlen) and ((j % 5) == 0):
                    self.assets[i] = insert(self.assets[i], '~' * padding, j)        #'~'

        startlen = len(self.assets[1])
        self.assets[0] = 4 * ' ' + (startlen-5) * '_'
        self.assets[0] = insert(self.assets[0], '!', ((startlen - 5)//2 + 4))
        self.aligned = True
