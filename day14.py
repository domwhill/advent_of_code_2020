"""Day 14
 mem [8] = 11

 36 bits
 2^35 ... 2^0

 X bit is unchanged
"""

import re
import numpy as np
import itertools


def pad_bit(bit):
    """Ensure that the bit is of length 36 pad from the left handside with 0s """
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
    indices0 = np.where(mask_arr == '0')[0]
    indices1 = np.where(mask_arr == '1')[0]
    indicesX = np.where(mask_arr == 'X')[0]
    return (indices0, indices1, indicesX), mask_arr


def relabel_bit(bit, idx, values):
    """Relabel bit and indexes idx with integer values 'values'"""
    bit_arr = np.array(list(bit))
    bit_arr[idx] = values
    return ''.join(bit_arr)


def apply_mask(bit, mask):
    """Part 1 mask application to bit"""
    id_01x, mask_arr = process_mask(mask)
    idx = id_01x[-1]
    bit = relabel_bit(bit, idx, mask_arr[idx])
    return bit


def read_file(file_name):
    """Readlines of file as strings."""
    f = open(file_name, "r")
    data = f.readlines()
    return data


def get_mask(line):
    """Get mask details from line in file

    Returns: string = mask
    """
    mask_str = line.split("=")[-1]
    return mask_str.strip()


def process_mem_line(line):
    """ Returns mem_address int, value to write to address int"""
    split_line = [val.strip() for val in line.split("=")]

    part1 = split_line[0]
    part2 = split_line[1]

    mm = re.search(r"mem\[(\d+)\]", part1)
    mem_address = int(mm.groups()[0])
    value = int(part2)
    return mem_address, value


def process_bit_mem_address_part2(mask, address_bit):
    """Takes in the mask in bits in address_in_bits
    Returns a bit wise list of addresses to write to.
    """
    idx, mask_arr = process_mask(mask)
    idx0, idx1, idxX = idx
    # apply basic mask
    #address_bit = relabel_bit(address_bit, idx0, mask_arr[idx0])
    address_bit = relabel_bit(address_bit, idx1, mask_arr[idx1])

    # apply floating 'X' mask
    # find all combinations of 0 and 1s in Xs
    # all possible combinations is the cartesian product
    x = (0, 1)
    xl = (x for ix in range(len(idxX)))
    masks = list(itertools.product(*xl))
    # now convert a to a memory address
    mem_addresses_bit = [relabel_bit(address_bit, idxX, mask) for mask in masks]
    return mem_addresses_bit


class Process:
    """Class to process advent of code input mask & memory writing data
    Part 1 & parent class for part 2
    """

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

    def write_to_address(self, address_int, number):
        bit = num_to_bit(number)
        masked_bit = apply_mask(bit, self.mask)

        self.write_masked_bit_to_mem(address_int, masked_bit)

    def write_masked_bit_to_mem(self, address_int, masked_bit):
        if address_int in self.memory_indices:
            self.overwrite_address(address_int, masked_bit)
        else:
            self.memory_indices.append(address_int)
            self.memory.append(masked_bit)

    def overwrite_address(self, id, bit):
        mem_idx = self.memory_indices.index(id)
        self.memory[mem_idx] = bit

    def sum_mem(self):
        mem_num = [bit_to_num(mem) for mem in self.memory]
        return np.sum(mem_num)


class Process2(Process):

    def process_line(self, line):
        line = line.strip()
        if line[:4] == "mask":
            self.mask = get_mask(line)

        elif line[:3] == "mem":
            seed_address_int, value_to_write_int = process_mem_line(line)
            seed_address_bit = num_to_bit(seed_address_int)
            mask_addresses_bits = process_bit_mem_address_part2(self.mask, seed_address_bit)
            for mask_address_bit in mask_addresses_bits:
                mask_address_int = bit_to_num(mask_address_bit)
                self.write_to_address(mask_address_int, value_to_write_int)

    def write_to_address(self, address_int, masked_int):
        bit = num_to_bit(masked_int)
        self.write_masked_bit_to_mem(address_int, bit)


def main():
    file_name = "day14_input.txt"

    # part 1
    proc = Process()
    proc.process_file(file_name)
    print(f"Part1 answer = {proc.sum_mem()}")

    # part 2
    proc = Process2()
    proc.process_file(file_name)
    print(f"Part2 answer = {proc.sum_mem()}")


if __name__ == "__main__":
    main()
