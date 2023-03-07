from image_net import *


class SchematicDrawer:
    def __init__(self):
        pass

# todo Класс, ответсвенный за рисование цепи из Net()'ов
# todo - gen_schematic_image должен формировать список списка net'ов как в hierarchy, но по уровням
#     - должен формировать список изображений по той же структуре как в функции выше
#     - вывести посмотреть o.O

    def sort_nets_by_level(self, net: Net):
        sourcenetlist = net.hierarchy()
        netlist = []
        strnetlist = []
        for n in sourcenetlist:
            netlist.append([n])
            strnetlist.append([str(n)])
        return(strnetlist)

'''
    РАБОЧИЙ ОБХОД ПО ШИРИНЕ:
    a = []
    O = []
    O.append(N_Q)
    while len(O) > 0:
    ...:     z.append(O[0])
    ...:     for q in O[0].node_lists:
    ...:         if q.next_net is not None:
    ...:             O.append(q.next_net)
    ...:     O.pop(0)
'''

'''
    ИДЕЯ:
    превратить список из обхода по ширине в список строк (лучше копию сделать)
    если следующий узел есть в этом, то они на одном уровне
    [N_Q]
    [n01]
    [n02, n04]
    [n03, n05, n06]
    [n07, n08]
    
    И в таком порядке сохранить NodeImage.assets, чтобы было легко рисовать. Можно им дорисовывать разделитель, чтобы добавлять пробелы.
'''