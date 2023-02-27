class BitVector(object):
    def get_bit_by_index(self, index):
        if index < 0:
            index = self.size + index
        return (self.val >> index) & 1

    def __init__(self, init_val: int, size: int):
        self.val = init_val
        self.size = size

    def __repr__(self):
        format_str = '#0%db' % (self.size + 2, )
        return f'{self.__class__.__name__}({format(self.val, format_str)}, {self.size})'

    def __str__(self):
        format_str = '#0%db' % (self.size + 2, )
        return f'{format(self.val, format_str)}'

    def __getitem__(self, item):
        if type(item) == int:
            if item >= self.size:
                raise KeyError('Bit index out of range')
            return self.get_bit_by_index(item)
        elif type(item) == slice:
            start = item.start if item.start is not None else 0
            stop = item.stop if item.stop is not None else self.size
            step = item.step if item.step is not None else 1
            if start < 0:
                start = self.size + start
            if stop < 0:
                stop = self.size + stop
            new_sz = (stop - start) // step
            if (stop - start) % step != 0:
                new_sz += 1
            new_val = 0
            i = 0
            for bit_idx in range(start, stop, step):
                new_val |= self.get_bit_by_index(bit_idx) << i
                i += 1
            return self.__class__(new_val, new_sz)

    def __len__(self):
        return self.size

    def __iter__(self):
        self.iter_idx = 0
        return self

    def __next__(self):
        tmp = 0
        if self.iter_idx < self.size:
            tmp = self.get_bit_by_index(self.size - 1 - self.iter_idx)
            self.iter_idx += 1
        else:
            raise StopIteration
        return tmp

    def calc_bits(self):
        zeros_num = 0
        ones_num = 0
        for bit in self:
            if bit:
                ones_num += 1
            else:
                zeros_num += 1
        return zeros_num, ones_num
