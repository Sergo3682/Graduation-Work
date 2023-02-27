class Net:
    def __init__(self, sn_list=None):
        self.node_lists = []
        if sn_list is not None:
            self.node_lists.append(sn_list)

    def __repr__(self):
        return f'{self.__class__.__name__}({self.node_lists})'

    def hierarchy(self):
        n0 = []
        n0.append(self)
        appended = []
        i = 0
        while i < len(n0[0].node_lists):
            if n0[0].node_lists[i].next_net is not None:
                appended = n0[0].node_lists[i].next_net.hierarchy()
                j = 0
                for j in range(len(appended)):
                    n0.append(appended[j])
            i += 1
        return n0
