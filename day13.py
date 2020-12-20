"""day13


Finding bus wait times.

This solution is brute force and pretty slow.
"""
import numpy as np
import pytest


def read_file_lines(file_name):
    f = open(file_name, "r")
    data = f.readlines()
    departure_time = int(data[0].strip())
    bus_time = data[1].strip()
    bus_list = bus_time.split(',')
    f.close()
    return bus_list, departure_time


def load_file_part1(file_name):
    bus_list, departure_time = read_file_lines(file_name)
    running_buses = []
    for bus in bus_list:
        if bus != "x":
            running_buses.append(int(bus))
    return departure_time, running_buses


def load_file_part2(file_name):
    bus_list, departure_time = read_file_lines(file_name)
    bus_dept_times, running_buses = process_file_string_to_bus_info(bus_list)
    return bus_dept_times, running_buses


def process_file_string_to_bus_info(bus_list):
    bus_intervals = []
    bus_delays = []
    for _delay, bus in enumerate(bus_list):
        if bus != "x":
            bus_delays.append(int(_delay))
            bus_intervals.append(int(bus))
    return bus_delays, bus_intervals


def get_wait_times(buses, dept_time):
    wait_times = []
    for time in buses:
        wait_time = time - (dept_time % time)
        wait_times.append(wait_time)
    return wait_times


def part1(file_name):
    dept_time, buses = load_file_part1(file_name)
    wait_times = get_wait_times(buses, dept_time)
    # index of shortest wait time
    id = int(np.argmin(wait_times))
    return wait_times[id] * buses[id]


def get_bus_remainders(time0, bus_delay_time, bus_interval):
    """Returns zero if the time0 satisfies the earliest time stamp criterion.
    """
    remainder = (time0 + bus_delay_time) % bus_interval
    return remainder


def part2(file_name):
    bus_dept_times, bus_intervals = load_file_part2(file_name)
    # looking for n for which where n is an integer
    return get_simultaneous_stop_time(bus_dept_times, bus_intervals)


def get_simultaneous_stop_time(bus_delays, bus_intervals):
    bus_intervals = np.array(bus_intervals)
    bus_delays = np.array(bus_delays)

    # Use the bus with the maximum interval value to loop over.
    id_max_interval = np.argmax(bus_intervals)
    n = 0
    bus_delay0 = bus_delays[id_max_interval]
    bus_interval0 = bus_intervals[id_max_interval]
    while True:
        # get zero delay time
        time = -bus_delay0 + bus_interval0 * n
        # time interval remainder from required arrival time for buses
        remainders = get_bus_remainders(time, bus_delays, bus_intervals)
        if np.sum(remainders) == 0:
            print("Matching time = ", time)
            break
        n += 1
    return time


@pytest.mark.parametrize("input,expected", [
    ("17,x,13,19", 3417),
    ("67,7,59,61", 754018),
    ("67,x,7,59,61", 779210),
    ("67,7,x,59,61", 1261476),
    ("1789,37,47,1889", 1202161486),
])
def test_part2(input, expected):
    bus_delays, bus_intervals = process_file_string_to_bus_info(input.split(','))
    stop_time = get_simultaneous_stop_time(bus_delays, bus_intervals)
    assert stop_time == expected


def main():
    file_name = "day13_input.txt"
    wait_times_by_bus_interval = part1(file_name)
    print(f"Part1 answer = {wait_times_by_bus_interval}")
    earliest_timestamp = part2(file_name)
    print(f"Part 2 answer = {earliest_timestamp}")


if __name__ == "__main__":
    main()
