from image_net import *


class SchematicDrawer:
    def __init__(self, root: Net = None):
        self.list_of_nets = []
        self.STR_list_of_nets = []
        if root is not None:
            self.sort_nets_by_level(root)

# todo Класс, ответсвенный за рисование цепи из Net()'ов
# todo - gen_schematic_image должен формировать список списка net'ов как в hierarchy, но по уровням
#     - должен формировать список изображений по той же структуре как в функции выше
#     - вывести посмотреть o.O

    def sort_nets_by_level(self, root: Net):
        self.list_of_nets = []
        self.STR_list_of_nets = []
        self.STR_list_of_nets.append(root)
        while len(self.STR_list_of_nets) > 0:
            self.list_of_nets.append(self.STR_list_of_nets[0])
            for node in self.STR_list_of_nets[0].node_lists:
                if node.next_net is not None:
                    self.STR_list_of_nets.append(node.next_net)
            self.STR_list_of_nets.pop(0)

        self.STR_list_of_nets = self.list_of_nets.copy()
        for i in range(len(self.STR_list_of_nets)):
            self.STR_list_of_nets[i] = str(self.STR_list_of_nets[i])

        list_of_nets = []
        STR_list_of_nets = []
        checker = False
        list_of_nets.append([self.list_of_nets[0]])
        STR_list_of_nets.append([self.STR_list_of_nets[0]])
        for i in range(1, len(self.STR_list_of_nets)):
            for j in STR_list_of_nets[len(STR_list_of_nets) - 1]:
                if self.STR_list_of_nets[i] in j:
                    checker = True
                    break
                    #STR_list_of_nets.append([self.STR_list_of_nets[i]])
                else:
                    checker = False
                    #STR_list_of_nets[len(STR_list_of_nets) - 1].append(self.STR_list_of_nets[i])
            if checker:
                checker = False
                STR_list_of_nets.append([self.STR_list_of_nets[i]])
            else:
                STR_list_of_nets[len(STR_list_of_nets) - 1].append(self.STR_list_of_nets[i])
        return STR_list_of_nets
'''
    ИДЕЯ:
    превратить список из обхода по ширине в список строк (лучше копию сделать)
    если следующий узел есть в этом, то они на одном уровне НЕ РАБОТАЕТ В НЕКОТОРЫХ СЛУЧАЯХ!!!!!!! СМ БУМАЖКУ
    [N_Q]
    [n01]
    [n02, n04]
    [n03, n05, n06]
    [n07, n08]
    
    И в таком порядке сохранить NodeImage.assets, чтобы было легко рисовать. Можно им дорисовывать разделитель, чтобы добавлять пробелы.
'''