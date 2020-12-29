"""Day 15 advent of code

Refactored following solution given by: https://gist.github.com/joshbduncan/2bc3bf1c0e0d39ee52b038a765760928

"""
import pytest

def get_last_mentioned_index(val_list, val):
    id_rev = val_list[::-1].index(val)
    return len(val_list) - id_rev - 1


def update_dict_key_value(dict, key, value):
    if key in dict:
        dict[key] = [value] + [dict[key][0]]
    else:
        dict[key] = [value]
    return dict


def get_last_number(starting_numbers, final_turn=2020):
    """Get final number according to the elf game rules.

    starting_numbers, tuple, int
    final_turn, int index of last turn spoken by elves.
    """
    unique_numbers_spoken = {num: [i] for i, num in enumerate(starting_numbers)}
    turn_number = starting_numbers[-1]

    # initialise to some fake value
    for i in range(len(starting_numbers), final_turn):
        # get new turn number from previous number
        turn_hist = unique_numbers_spoken.get(turn_number, [])
        if len(turn_hist) <= 1:
            turn_number = 0
            unique_numbers_spoken = update_dict_key_value(unique_numbers_spoken, turn_number, i)

        else:
            # get difference
            turn_number = turn_hist[0] - turn_hist[1]
            # update record of turns the number is spoken at
            unique_numbers_spoken = update_dict_key_value(unique_numbers_spoken, turn_number, i)

    return turn_number


@pytest.mark.parametrize("input,expected", [((1, 3, 2), 1), ((2, 1, 3), 10), ((1, 2, 3), 27),
                                            ((2, 3, 1), 78), ((3, 2, 1), 438), ((3, 1, 2), 1836)])
def test_get_last_number(input, expected):
    final_num = get_last_number(input, final_turn=2020)
    assert final_num == expected


@pytest.mark.parametrize("input,expected", [((0, 3, 6), 175594), ((1, 3, 2), 2578),
                                            ((2, 1, 3), 3544142), ((1, 2, 3), 261214),
                                            ((2, 3, 1), 6895259), ((3, 2, 1), 18),
                                            ((3, 1, 2), 362)])
def test_get_last_number_part2(input, expected):
    final_num = get_last_number(input, final_turn=30000000)
    assert final_num == expected


if __name__ == "__main__":
    starting_numbers = (7, 14, 0, 17, 11, 1, 2)
    final_number = get_last_number(starting_numbers, final_turn=10)
    print("final number = ", final_number)
