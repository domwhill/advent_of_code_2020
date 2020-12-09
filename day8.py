"""day 8

Infininte loop program
What value is in the accumulator before an instruction is run a second time?

"""
import re

def process_line(line):

    line = line.strip()
    g = re.search("^([a-z]{3}) ([+\-0-9]+)" , line)
    if not g:
        raise ValueError(f"{line} format not understood")
    instruction, jump = g.groups()
    return instruction, int(jump)

def process_instruction(current_line, accum, instruction, jump):
    # do nothing
    current_line +=1
    #if instruction == "nop":
    #    out_line = current_line
    if instruction == "acc":
        accum += jump
    elif instruction == "jmp":
        current_line += jump -1
    return current_line, accum

def switch_jmp_nop(instruction):
    if instruction == "jmp":
        out = "nop"
    elif instruction == "nop":
        out = "jmp"
    else:
        out = instruction
    return out

def read_file_instructions(data, switch_line = None):
    """Read through file instructions and sum up accum

    switch_line is an integer index that indicates a line for which
    jmp->nop or nop-> jmp
    """
    visited_lines = []
    accum = 0
    i = 0
    is_not_infinite_loop = False
    while i < len(data):
        # exit if infinite loop
        if i in visited_lines:
            print(f"breaking: line finish = {i} \n accum = {accum}")
            is_not_infinite_loop = False
            break
        else:
            visited_lines.append(i)

        # read in line
        line = data[i]
        instruction, jump = process_line(line)
        # switch jmp-> nop or nop-> jmp
        if i == switch_line:
            instruction = switch_jmp_nop(instruction)

        i, accum = process_instruction(i, accum, instruction, jump)

        # correct exit
        if i == len(data):
            print(f"accum value = {accum}")
            is_not_infinite_loop = True
            break
    return is_not_infinite_loop, accum


def read_in_data(file_name):
    f = open(file_name, "r")
    data = f.readlines()
    f.close()
    return data


def main():
    file_name = "day8_input.txt"
    data = read_in_data(file_name)
    for switch_line in range(len(data)):
        if data[switch_line][:3] == "acc":
            continue
        else:
            is_valid_answer, accum = read_file_instructions(data, switch_line)
            if is_valid_answer:
                print(f"Finished - accum = {accum}")
                break


if __name__=="__main__":
    main()