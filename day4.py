"""Advent of code day 4

"""
import re
import numpy as np
import pytest


def process_line(line):
    """Convert line to dictionary"""
    line = re.sub("\n", "", line)
    # split line by white space
    split_line = re.split("\s+", line)
    out_dictionary = {}
    for entry in split_line:
        entry = entry.split(":")
        if len(entry) != 2:
            raise ValueError(f" Entry {entry} key value pair not recognised")
        out_dictionary[entry[0]] = entry[1]
    return out_dictionary


def get_passport_data_list(filename):
    """Return a list of dictionaries containing all the passport data"""
    passport_list = []
    passport = {}
    f = open(filename, "r")
    for line in f.readlines():
        if line == "\n":
            passport_list.append(passport)
            passport = {}
        else:
            key_data = process_line(line)
            passport.update(key_data)
    # must add last passport in:
    passport_list.append(passport)
    return passport_list


def check_valid_passport_field_number(passport):
    valid_passport = False
    if len(passport.keys()) == 8:
        valid_passport = True
    elif len(passport.keys()) == 7 and "cid" not in passport.keys():
        print("passport.keys()", passport.keys())
        valid_passport = True
    elif len(passport.keys()) > 8:
        raise ValueError(f"Number of keys greater than expected {passport}")
    return valid_passport


def check_height(height_value):
    units = height_value[-2:]
    value = int(height_value[:-2])

    if units == "cm":
        is_correct = (value >= 150) * (value <= 193)
    elif units == "in":
        is_correct = (value >= 59) * (value <= 76)
    else:
        is_correct = False
    return is_correct


def check_hair_colour(hair_colour):
    #if hair_colour[0] == "#" and re.search("[0-9a-z]{6}",hair_colour[1:]):
    if re.search("^#[0-9a-f]{6}$", hair_colour):
        is_valid = True
    else:
        is_valid = False
    return is_valid


def check_eye_colour(eye_colour):
    if eye_colour in ("amb", "blu", "brn", "gry", "grn", "hzl", "oth"):
        is_valid = True
    else:
        is_valid = False
    return is_valid


def check_pid(pid):
    if re.search("^[0-9]{9}$", pid):
        is_valid = True
    else:
        is_valid = False
    return is_valid


def check_year(value, min_year, max_year):
    value = int(value)
    if ((value) >= min_year) and (value <= max_year):
        is_valid = True
    else:
        is_valid = False
    return is_valid


def check_valid_passport(passport):
    if not check_valid_passport_field_number(passport):
        return False
    if not check_year(passport["byr"], 1920, 2002):
        return False
    if not check_year(passport["iyr"], 2010, 2020):
        return False
    if not check_year(passport["eyr"], 2020, 2030):
        return False
    if not check_height(passport["hgt"]):
        return False
    if not check_hair_colour(passport["hcl"]):
        return False
    if not check_eye_colour(passport["ecl"]):
        return False
    if not check_pid(passport["pid"]):
        return False
    return True


def check_passports(filename):
    passports = get_passport_data_list(filename)
    valid_pp = []
    for pp in passports:
        is_valid = check_valid_passport(pp)
        valid_pp.append(is_valid)

    return np.sum(valid_pp)


@pytest.mark.parametrize("input,expected", [("#cfa07d", True), ("#ae17e1", True), ("#ae17e1", True),
                                            ("123abc", False), ("#ae17e13", False)])
def test_hcl(input, expected):
    is_valid = check_hair_colour(input)
    assert is_valid == expected


@pytest.mark.parametrize("input,expected", [("60in", True), ("190cm", True), ("190in", False),
                                            ("190", False)])
def test_hgt(input, expected):
    is_valid = check_height(input)
    assert is_valid == expected


@pytest.mark.parametrize("input,expected", [
    ("000000001", True),
    ("0123456789", False),
])
def test_pid(input, expected):
    is_valid = check_pid(input)
    assert is_valid == expected


if __name__ == "__main__":

    filename = "day4_input.txt"

    passports = get_passport_data_list(filename)
    number_of_valid_pp = check_passports(filename)
    print(f"number of valid passports = {number_of_valid_pp}")
