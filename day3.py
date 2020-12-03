"""Advent of code 2020

 day 3
 Colliding with trees
 """
import numpy as np


def load_data(fname):
    """Load in the test data from file."""
    f = open(fname, "r")
    data = f.readlines()
    f.close()

    line_length = find_line_length(data[0])
    array_data = []  #
    print("id = ", line_length)
    for il, line in enumerate(data):
        array_data.append(list(data[il])[:line_length])
    return np.array(array_data)


def find_line_length(line):
    """Find length of test data line.    """
    if " " not in list(line):
        # minus 1 here to remove newline characters
        id = len(line) - 1
    else:
        id = np.where(np.array(list(line)) == " ")[0][0]
    return id


def column_ids(row_id, across, down, max_r, max_c):
    """Return the positions the sleigh passes through with a gradient
    across/down
    """
    col_id = (across / down) * row_id
    col_id = col_id.astype(int)
    # map column id back into the bounds of the data array
    return (col_id % max_c)


def check_tree(data, irow, icol):
    return data[irow, icol] == "#"


def get_number_of_encountered_trees(across, down, tree_map):
    """Get number of encountered trees for gradient
            across = number of squares right per step
            down = number of squares down per step
    """
    max_rows, max_cols = tree_map.shape

    rows = np.arange(0, max_rows, down, dtype=int)
    columns = column_ids(rows, across, down, max_rows, max_cols)

    indices = np.column_stack((rows, columns))

    encountered_trees = []
    for index in indices:
        encountered_trees.append(check_tree(tree_map, *index))
    number_of_trees = np.sum(encountered_trees)
    return number_of_trees


def main():
    #fname = "test_input3.txt"

    fname = "day3_input.txt"
    tree_map = load_data(fname)

    gradients = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]
    total_number_of_trees = []
    for gradient in gradients:
        across, down = gradient
        number_of_trees = get_number_of_encountered_trees(
            across, down, tree_map)
        total_number_of_trees.append(number_of_trees)

    print("total_number_of_trees = ", total_number_of_trees)
    print("final answer = ", np.product(total_number_of_trees))


if __name__ == "__main__":
    main()
