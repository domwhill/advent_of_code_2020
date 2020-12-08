"""Advent of code day 7

Represent bags as connections (directed graph)
- search connections for bag names
- count bags

"""
import re
import numpy as np


def search_second_bg(second_bag):
    """Search second bag for its number and colour"""
    sb = re.search("([0-9]+) (.*?) bag", second_bag)
    if sb:
        out = sb.groups()
    else:
        out = None
    return out


def process_bags(fname):
    """Process bags into a list of connections and a dictionary"""
    f = open(fname, 'r')
    dict = {}
    connections = []    # tuple (left colour, right colour, number of bags)
    for line in f.readlines():
        bag_colour, contained_bags = extract_bag_colour_and_numbers(line)
        # number and colour
        if contained_bags[0] == "no other bags":
            continue
        else:
            contained_bags_tuple = [search_second_bg(second_bag) for second_bag in contained_bags]
            dict[bag_colour] = contained_bags_tuple
            connections += [
                (bag_colour, colour, int(number)) for number, colour in contained_bags_tuple
            ]
    return dict, connections


def extract_bag_colour_and_numbers(line):
    print("line", line.strip())
    bg = re.search(r"^(.*?)bags{0,1}\s+contain(.*?)\.", line)
    bag_colour = bg.groups()[0].strip()
    contained_bags = bg.groups()[1].strip().split(',')
    return bag_colour, contained_bags


def search_for_holding_bags(connections, bag_colour):
    connections = np.array(connections)
    id = connections[:, 1] == bag_colour
    return list(connections[id, 0])


def search_for_containing_bags(connections, bag_colour):
    connections = np.array(connections)
    id = connections[:, 0] == bag_colour
    return connections[id, :]


def count_containing_bags(total_number_of_bags, holding_colours, connections, number_of_bags,
                          colour):
    """Part 2: count total number of bags contained inside multiplier bags of colour 'colour'"""
    if not isinstance(colour, str):
        raise TypeError(f"Expected bag colours to be of type str" f" {colour} got {type(colour)}")

    hc = search_for_containing_bags(connections, colour)
    if hc.size > 0:
        for id, hbag in enumerate(hc[:, 1]):
            number_of_new_bags = int(hc[id, -1])
            # note lack of if statement -
            # this time we may double include bags as we want to count all
            # possible bags contained

            # number of bags is the number of previous bags multiplied
            # by the number of hbags this previous bag contains.
            new_multiplier = number_of_bags * number_of_new_bags
            total_number_of_bags += [new_multiplier]
            holding_colours += [hbag]
            # search for any bags that may hold bag with colour hc
            total_number_of_bags, holding_colours = count_containing_bags(
                total_number_of_bags, holding_colours, connections, new_multiplier, hbag)
    return total_number_of_bags, holding_colours


def get_holding_bag_colours(holding_colours, connections, colour):
    """Get the colours of all the bags that can hold bag of 'colour'"""
    if not isinstance(colour, str):
        raise TypeError(f"Expected bag colours to be of type str" f" {colour} got {type(colour)}")

    hc = search_for_containing_bags(connections, colour)
    if len(hc) > 0:
        for hbag in hc:
            if hbag not in holding_colours:
                # add to the list of holding bags
                holding_colours += [hbag]
                # search for any bags that may hold bag with colour hc
                get_holding_bag_colours(holding_colours, connections, hbag)
    return holding_colours


if __name__ == "__main__":
    fname = "day7_test_input.txt"
    fname = "day7_input.txt"
    dict, connections = process_bags(fname)

    # part 1
    holding_colours = get_holding_bag_colours([], connections, "shiny gold")
    print("holding_colours = ", holding_colours)
    print("Number of different colours = ", len(holding_colours))

    # part 2
    multiplier_list, containing_colours = count_containing_bags([1], [], connections, 1,
                                                                "shiny gold")
    print("multiplier_list = ", multiplier_list, "containing_colours = ", containing_colours)
    print("Total number of bags = ", np.sum(multiplier_list) - 1)
