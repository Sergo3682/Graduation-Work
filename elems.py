
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
    def __init__(self, inst_type, name, connectors: [str], model=None, value=None):
        self.type = inst_type
        self.name = name
        self.connections = connectors
        if (model is not None) and (value is not None):
            raise ValueError('"model" and "value" cannot be defined at the same time!')
        if model is not None:
            self.model = model
            self.value = None
        if value is not None:
            self.model = None
            self.value = value

    def __str__(self):
        res = ''
        res += self.type
        res += self.name + ' '
        for con in self.connections:
            res += con + ' '
        if self.value is None:
            res += self.model
        else:
            res += self.value


class Net:
    def __init__(self):
        self.name = ''
        
    def __str__(self):
        return self.name

    def __eq__(self, other):
        return self.name == other.name
