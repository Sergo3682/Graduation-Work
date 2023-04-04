from schematicbuilder import SchematicBuilder


class Parser:
    def __init__(self, output_file: str, builder: SchematicBuilder):
        self.output_file = self.pd_root = self.pu_root = None
        if output_file is not None:
            self.output_file = output_file
        if builder is not None:
            self.pd_root = builder.pd_netlist[0]
            self.pu_root = builder.pu_netlist[0]
            self.builder = builder

    def __repr__(self):
        return f'{self.__class__.__name__}({self.output_file}, {self.builder.__repr__()})'
