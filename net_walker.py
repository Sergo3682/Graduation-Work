from net import Net


class NetWalker:
    def __init__(self, root: Net):
        self.root_net: Net = root

    def walk(self, net, sn_action_fn=None, sn_fn_kwargs=None, net_action_fn=None, net_fn_kwargs=None):
        if net_action_fn is not None:
            net_action_fn(net, **net_fn_kwargs)
        for sn in net.node_lists:
            if sn_action_fn is not None:
                sn_action_fn(sn, **sn_fn_kwargs)
            if sn.next_net is not None:
                self.walk(sn.next_net, sn_action_fn, sn_fn_kwargs, net_action_fn, net_fn_kwargs)
