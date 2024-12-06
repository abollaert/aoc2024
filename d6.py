from enum import IntEnum

from d4 import Direction

class Direction(IntEnum):
    N = 0,
    E = 1,
    S = 2,
    W = 3

def parse_input(filename: str) -> list[str]:
    with open(filename) as f:
        return [line.strip() for line in f]

def get_guard_location_and_direction(map: list[str]) -> tuple[int, int, Direction] | None:
    for row in range(len(map)):
        for col in range(len(map[row])):
            if map[row][col] == "^":
                return row, col, Direction.N
            elif map[row][col] == ">":
                return row, col, Direction.E
            elif map[row][col] == "v":
                return row, col, Direction.S
            elif map[row][col] == "<":
                return row, col, Direction.W

    return None

def is_obstacle(map: list[str], location: tuple[int, int]) -> bool:
    return map[location[0]][location[1]] == "#"

def get_next_location(map: list[str], current_location: tuple[int, int], direction: Direction) -> tuple[int, int]:
    current_row, current_col = current_location
    next_row: int = -1
    next_col: int = -1

    match(direction):
        case Direction.N:
            next_row = current_row -1
            next_col = current_col
        case Direction.E:
            next_row = current_row
            next_col = current_col + 1
        case Direction.S:
            next_row = current_row + 1
            next_col = current_col
        case Direction.W:
            next_row = current_row
            next_col = current_col - 1

    if next_row >= 0 and next_col >= 0 and next_row < len(map) and next_col < len(map[0]):
        return (next_row, next_col)

    return (-1, -1)

def turn(direction: Direction) -> Direction:
    if direction == Direction.N:
        return Direction.E
    elif direction == Direction.E:
        return Direction.S
    elif direction == Direction.S:
        return Direction.W
    elif direction == Direction.W:
        return Direction.N

def guard_character(direction: Direction) -> str:
    if direction == Direction.N:
        return "^"
    elif direction == Direction.E:
        return ">"
    elif direction == Direction.S:
        return "v"
    elif direction == Direction.W:
        return "<"

def set_character_at(map: list[str], location: tuple[int, int], character: str) -> list[str]:
    row, col = location
    new_map: list[str] = []

    for i in range(len(map)):
        if i != row:
            new_map.append(map[i])
        else:
            new_map.append(map[row][:col] + character + map[row][col + 1:])

    return new_map

def move_guard(map: list[str],
               guard_location: tuple[int, int, Direction],
               visited: list[tuple[int, int, Direction]]) -> tuple[int, int, Direction] | None:
    if guard_location is None:
        return
    else:
        row, col, direction = guard_location

        next_row, next_col = get_next_location(map, (row, col), direction)

        if next_row == -1 and next_col == -1:
            visited.append((row, col, direction))
            return None
        elif is_obstacle(map, (next_row, next_col)):
            new_direction: Direction = turn(direction)
            return (row, col, new_direction)
        else:
            visited.append((row, col, direction))
            return (next_row, next_col, direction)

def print_map(map: list[str]) -> None:
    for row in map:
        print(row)

def has_guard(map: list[str]) -> bool:
    return get_guard_location_and_direction(map) is not None

def run_map(map: list[str]) -> tuple[list[tuple[int, int, Direction]], bool]:
    guard_location = get_guard_location_and_direction(map)

    visited: list[tuple[int, int, Direction]] = []

    while guard_location is not None and guard_location not in visited:
        guard_location = move_guard(map, guard_location, visited)

    if guard_location is not None:
        return (visited, False)
    else:
        return (visited, True)

def distinct_locations(visited: list[tuple[int, int, Direction]]) -> set[tuple[int, int]]:
    return set([(location[0], location[1]) for location in visited])

def set_obstacle(map: list[str], location: tuple[int, int]) -> list[str]:
    new_map: list[str] = set_character_at(map, location, "#")

    return new_map

def generate_new_maps(map: list[str], obstacles: set[tuple[int, int]]) -> list[list[str]]:
    new_maps: list[list[str]] = []

    for obstacle in obstacles:
        new_maps.append(set_obstacle(map, obstacle))

    return new_maps

if __name__ == "__main__":
    map: list[str] = parse_input("d6_input.txt")

    visited, finishes = run_map(map)
    locations: set[tuple[int, int]] = distinct_locations(visited)

    new_maps: list[list[str]] = generate_new_maps(map, locations)

    print("Have %d new maps to try" % (len(new_maps)))

    count: int = 0


    for i in range(len(new_maps)):
        print("Testing map %d" % (i + 1))

        visited, finishes = run_map(new_maps[i])

        if not finishes:
            count += 1

    print(count)

