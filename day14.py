"""Day 14
 mem [8] = 11

 36 bits
 2^35 ... 2^0

 X bit is unchanged
"""

import re
import numpy as np


def pad_bit(bit):
    """ """
    bg = 36 * '0'
    output = bg[:-len(bit)] + bit
    return output


def _num_to_bit(number):
    return bin(number)[2:]


def bit_to_num(bit):
    return int(bit, 2)


def num_to_bit(number):
    bit = _num_to_bit(number)
    return pad_bit(bit)


def process_mask(mask):
    mask_arr = np.array(list(mask))
    indices = np.where(mask_arr != 'X')[0]
    return indices, mask_arr


def relabel_bit(bit, idx, values):
    bit_arr = np.array(list(bit))
    bit_arr[idx] = values[idx]
    return ''.join(bit_arr)


def apply_mask(bit, mask):
    assert len(bit) == 36
    idx, mask_arr = process_mask(mask)
    bit = relabel_bit(bit, idx, mask_arr)
    return bit


def read_file(file_name):
    f = open(file_name, "r")
    data = f.readlines()
    return data


def get_mask(line):
    mask_str = line.split("=")[-1]
    return mask_str.strip()


def process_mem_line(line):
    split_line = [val.strip() for val in line.split("=")]

    part1 = split_line[0]
    part2 = split_line[1]

    mm = re.search(r"mem\[(\d+)\]", part1)
    mem_address = int(mm.groups()[0])
    value = int(part2)
    return mem_address, value


class Process:

    def __init__(self):
        self.mask = None
        self.mem = None
        self.memory_indices = []
        self.memory = []

    def process_file(self, file_name):

        data = read_file(file_name)
        for line in data:
            self.process_line(line)

    def process_line(self, line):
        line = line.strip()
        if line[:4] == "mask":
            self.mask = get_mask(line)

        elif line[:3] == "mem":
            id, bit = process_mem_line(line)
            self.write_to_address(id, bit)

    def write_to_address(self, id, number):
        bit = num_to_bit(number)
        masked_bit = apply_mask(bit, self.mask)

        if id in self.memory_indices:
            self.overwrite_address(id, masked_bit)
        else:
            self.memory_indices.append(id)
            self.memory.append(masked_bit)

    def overwrite_address(self, id, bit):
        mem_idx = self.memory_indices.index(id)
        self.memory[mem_idx] = bit

    def sum_mem(self):
        mem_num = [bit_to_num(mem) for mem in self.memory]
        return np.sum(mem_num)


def main():
    file_name = "day14_input.txt"
    #file_name = "day14_test_input.txt"
    proc = Process()
    proc.process_file(file_name)
    print(proc.sum_mem())


if __name__ == "__main__":
    main()
