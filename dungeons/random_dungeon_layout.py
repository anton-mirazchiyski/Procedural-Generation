import random

import colorama
from colorama import Fore, Style

size = 15
start_idx, end_index = 0, (size - 1)

colorama.init()


def build_dungeon_without_rooms():
    walls = '#' * size
    roomless_dungeon = [list(walls) for _ in range(size)]

    return roomless_dungeon


def determine_start_position(dungeon):
    possible_start_sides = ('top', 'left', 'bottom', 'right')

    random_start_side = random.choice(possible_start_sides)
    random_coordinates = None

    match random_start_side:
        case 'top':
            random_coordinates = (start_idx, random.randint(start_idx, end_index))
        case 'bottom':
            random_coordinates = (end_index, random.randint(start_idx, end_index))
        case 'left':
            random_coordinates = (random.randint(start_idx, end_index), start_idx)
        case 'right':
            random_coordinates = (random.randint(start_idx, end_index), end_index)

    start_row, start_col = random_coordinates
    dungeon[start_row][start_col] = Fore.YELLOW + 's' + Style.RESET_ALL

    return start_row, start_col


def position_is_available(row, col, dungeon):
    # a list of unavailable coordinates that keep the rooms spaced out
    unavailable_coordinates = [
        (row - 1, col - 1), (row - 1, col), (row - 1, col + 1), (row - 1, col + 2),
        (row, col), (row, col - 1), (row, col + 1), (row, col + 2),
        (row + 1, col - 1), (row + 1, col), (row + 1, col + 1), (row + 1, col + 2),
        (row + 2, col - 1), (row + 2, col), (row + 2, col + 1), (row + 2, col + 2),
    ]

    for current_row, current_col in unavailable_coordinates:
        if dungeon[current_row][current_col] != '#':
            return

    return True


def mark_room_cell(dungeon, row, col):
    dungeon[row][col] = Fore.BLUE + 'r' + Style.RESET_ALL


def generate_random_room_position():
    # excludes the edges and keeps the rooms within boundaries
    return random.randint(start_idx + 1, end_index - 2), random.randint(start_idx + 1, end_index - 2)


def create_room(row, col, dungeon):
    mark_room_cell(dungeon, row, col + 1)
    mark_room_cell(dungeon, row + 1, col + 1)
    mark_room_cell(dungeon, row + 1, col)
    mark_room_cell(dungeon, row, col)


def pick_random_room_cell(row, col):
    random_cell_coordinates = random.choice([(row, col + 1), (row + 1, col + 1), (row + 1, col), (row, col)])
    return random_cell_coordinates


def generate_rooms(dungeon):
    possible_number_of_rooms = random.randint(2, 7)
    random_room_cells = []

    for _ in range(possible_number_of_rooms):
        random_room_position = generate_random_room_position()
        current_row, current_col = random_room_position
        if position_is_available(current_row, current_col, dungeon):
            create_room(current_row, current_col, dungeon)
            random_cell = pick_random_room_cell(current_row, current_col)
            random_room_cells.append(random_cell)

    return random_room_cells


def mark_corridor_cell(dungeon, row, col):
    dungeon[row][col] = Fore.YELLOW + '.' + Style.RESET_ALL


def is_out_of_bounds(row, col):
    return row >= end_index or row <= start_idx or col >= end_index or col <= start_idx


def sort_coordinates_increasingly(coordinates):
    sorted_coordinates = sorted(coordinates, key=lambda x: (x[0], x[1]))
    return sorted_coordinates


def create_corridor(dungeon, row, col, previous_row, previous_col):
    if row == previous_row and col == previous_col:
        return

    if dungeon[row][col] != 's' and is_out_of_bounds(previous_row, previous_col):
        return

    if dungeon[previous_row][previous_col] == '#':
        mark_corridor_cell(dungeon, previous_row, previous_col)

    if row != previous_row:
        create_corridor(dungeon, row, col, previous_row + 1, previous_col) # move downwards

    if row == previous_row:
        if col > previous_col:
            create_corridor(dungeon, row, col, previous_row, previous_col + 1) # move towards the right

        if col < previous_col:
            create_corridor(dungeon, row, col, previous_row, previous_col - 1) # move towards the left


def generate_corridors(dungeon, rooms_coordinates):
    for idx in range(1, len(rooms_coordinates)):
        current_row, current_col = rooms_coordinates[idx]
        previous_row, previous_col = rooms_coordinates[idx - 1]
        create_corridor(dungeon, current_row, current_col, previous_row, previous_col)


dungeon = build_dungeon_without_rooms()
row_start, col_start = determine_start_position(dungeon)
rooms_coordinates = generate_rooms(dungeon)
sorted_rooms_coordinates = sort_coordinates_increasingly(rooms_coordinates + [(row_start, col_start)])
# print(sorted_rooms_coordinates)
generate_corridors(dungeon, sorted_rooms_coordinates)

print()
for row in dungeon:
    print(*row, sep=' ')
