class SerialNodes:
    def __init__(self, nodes=None, next_net=None):
        self.nodes = []
        if nodes is not None:
            self.nodes = nodes
        self._next_net = None
        if next_net is not None:
            self.next_net = next_net
        self.parent_net = None

    @property
    def next_net(self):
        return self._next_net

    @next_net.setter
    def next_net(self, val):
        self._next_net = val
        self._next_net.parent_node = self

    def __repr__(self):
        return f'{self.__class__.__name__}({self.nodes}, {self.next_net})'

    def __len__(self):
        return len(self.nodes)
