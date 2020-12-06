"""
Advent of code day 6


26 yes no question (a-z)
Identify questions for which anyone in your group answers yes


each question counts at smot once
"""
import numpy as np


def update_sublist(sub_list, line):
    if not isinstance(sub_list, str):
        raise TypeError("sub_list = {type(sub_list)} expected string")
    return sub_list + line.strip()


def load_file(file_name):
    """Return a list of dictionaries containing all the passport data"""
    sub_list = ""
    number_of_people_in_group = 0
    group_numbers = []
    combined_list = []
    f = open(file_name, "r")
    for line in f.readlines():
        if line == "\n":
            combined_list.append(sub_list)
            group_numbers.append(number_of_people_in_group)
            sub_list = ""
            number_of_people_in_group = 0
        else:
            sub_list = update_sublist(sub_list, line.strip())
            number_of_people_in_group += 1
    # must add last passport in:
    combined_list.append(sub_list)
    group_numbers.append(number_of_people_in_group)
    assert len(group_numbers) == len(combined_list)
    return combined_list, group_numbers


def get_unique_letters(answer):
    """Return a list of unique letters in answer"""
    return np.unique(list(answer))


def get_shared_answers(answer, people_in_group):
    """Count number of unique letters"""
    shared_answers = []
    for letter in get_unique_letters(answer):
        letter_count = answer.count(letter)
        if letter_count == people_in_group:
            shared_answers.append(letter)
    return len(shared_answers)


def count_unique_letters(answer):
    """Counts the number of unique letters in answer

    input: answer, string
    output: number of unique letters, integer
    """
    return len(get_unique_letters(answer))


def get_number_of_yes_answers(answers):
    """

    Args:
        answers:

    Returns:

    """
    unique_letters = []
    for answer in answers:
        unique_letters.append(count_unique_letters(answer))
    return np.sum(unique_letters)


def get_number_of_universal_answers(answers, group_numbers):
    """

    Args:
        answers:

    Returns:

    """
    shared_answers_per_group = []
    for igroup, answer in enumerate(answers):
        number_of_shared_answers = get_shared_answers(answer, group_numbers[igroup])
        shared_answers_per_group.append(number_of_shared_answers)
    return np.sum(shared_answers_per_group)


def main():
    #file_name = "day6_test_input.txt"
    file_name = "day6_input.txt"
    answers, group_numbers = load_file(file_name)
    number_of_unique_letters = get_number_of_yes_answers(answers)
    number_of_universal_answers = get_number_of_universal_answers(answers, group_numbers)
    print(f"number_of_unique_letters = {number_of_unique_letters}")
    print(f"part 2: number of universal answers = {number_of_universal_answers}")


if __name__ == "__main__":
    main()
