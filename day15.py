"""Day 15 advent of code

"""
import pytest


def get_last_mentioned_index(val_list, val):
    id_rev = val_list[::-1].index(val)
    return len(val_list) - id_rev - 1


def get_last_number(starting_numbers, final_turn=2020):
    """Get final number according to the elf game rules.

    starting_numbers, tuple, int
    final_turn, int index of last turn spoken by elves.
    """
    numbers_spoken = []
    for i in range(final_turn):
        if i < len(starting_numbers):
            turn_number = starting_numbers[i]
        else:
            previous_number = numbers_spoken[-1]
            if previous_number not in numbers_spoken[:-1]:
                turn_number = 0
            else:
                id_last = get_last_mentioned_index(numbers_spoken[:-1], previous_number)
                diff = i - id_last - 1
                turn_number = diff

        numbers_spoken.append(turn_number)
    return numbers_spoken[-1]


@pytest.mark.parametrize("input,expected", [((1, 3, 2), 1), ((2, 1, 3), 10), ((1, 2, 3), 27),
                                            ((2, 3, 1), 78), ((3, 2, 1), 438), ((3, 1, 2), 1836)])
def test_get_last_number(input, expected):
    final_num = get_last_number(input, final_turn=2020)
    assert final_num == expected


if __name__ == "__main__":
    starting_numbers = (7, 14, 0, 17, 11, 1, 2)
    # loop through starting numbers
    final_turn = 30000000
    final_number = get_last_number(starting_numbers, final_turn=30000000)
    print("final number = ", final_number)
