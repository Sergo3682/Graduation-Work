import net


class Net:
    def __init__(self, sn_list=None):
        self._node_lists = []
        self.parent_node = None
        if sn_list is not None:
            self.node_lists = sn_list

    @property
    def node_lists(self):
        return self._node_lists

    @node_lists.setter
    def node_lists(self, val):
        new_sn = []
        for nl in val:
            nl.parent_net = self
            new_sn.append(nl)
        self._node_lists = new_sn

    def __repr__(self):
        return f'{self.__class__.__name__}({self.node_lists})'

    def __eq__(self, other):
        if type(self) == type(other) == net.Net:
            return self.node_lists == other.node_lists
        else:
            return type(self) == type(other) == type(None)
