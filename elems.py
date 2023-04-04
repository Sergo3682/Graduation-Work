class Circuit:
    def __init__(self):
        self.instances = []
        self.nets = []

    def get_net_by_name(self, name):
        for net in self.nets:
            if net.name == name:
                return net
        return None

    def __str__(self):
        res = ''
        res += 'Insts: \n'
        for inst in self.instances:
            res += str(inst)
            res += '\n'
        res += 'Nets: \n'
        for net in self.nets:
            res += str(net)
            res += ' '
        res += '\n'
        return res


class Instance:
    def __init__(self):
        self.type = ''
        self.name = ''
        self.connections = []
        self.value = None
        self.model = None

    def __str__(self):
        res = 'Type: '
        res += self.type
        res += '; Name: '
        res += self.name
        if self.value is None:
            res += '; Model: '
            res += str(self.model)
        else:
            res += '; Value: '
            res += str(self.value)
        res += '; Cons: '
        for con in self.connections:
            res += str(con)
            res += ' '
        return res


class Net:
    def __init__(self):
        self.name = ''
        
    def __str__(self):
        return self.name

    def __eq__(self, other):
        return self.name == other.name
