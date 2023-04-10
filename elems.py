class Instance:
    def __init__(self, inst_type, name, connectors: [str], model=None, value=None):
        self.type = inst_type
        self.name = name
        self.connections = connectors
        if (model is not None) and (value is not None):
            raise ValueError('"model" and "value" cannot be defined at the same time!')
        if (model is None) and (value is None):
            raise ValueError('"model" or "value" must be defined')
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
        return res

    def __repr__(self):
        if self.value is None:
            optional = f"'{self.model}'"
        else:
            optional = f"model=None, value='{self.value}'"
        return f"{self.__class__.__name__}({self.type}, {self.name}, {self.connections}, {optional})"
