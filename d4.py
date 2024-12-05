from enum import IntEnum


class Direction(IntEnum):
    N = 0
    NE = 1
    E = 2
    SE = 3
    S = 4
    SW = 5
    W = 6
    NW = 7

def get_next_location(input: list[str], current: tuple[int, int], direction: Direction) -> tuple[int, int] | None:
    match direction:
        case Direction.N:
            row: int = current[0] - 1
            col: int = current[1]
        case Direction.NE:
            row = current[0] - 1
            col = current[1] + 1
        case Direction.E:
            row = current[0]
            col = current[1] + 1
        case Direction.SE:
            row = current[0] + 1
            col = current[1] + 1
        case Direction.S:
            row = current[0] + 1
            col = current[1]
        case Direction.SW:
            row = current[0] + 1
            col = current[1] - 1
        case Direction.W:
            row = current[0]
            col = current[1] - 1
        case Direction.NW:
            row = current[0] - 1
            col = current[1] - 1

    if row >= 0 and col >= 0 and col < len(input[0]) and row < len(input):
        return (row, col)

    return None

def get_character_at(input: list[str], location: tuple[int, int]) -> str:
    # print("Character at %s, input size : x %d, y %d" % (location, len(input[0]), len(input)))
    return input[location[0]][location[1]]

def parse_input(filename: str) -> list[str]:
    with open(filename) as f:
        return [line.strip() for line in f.readlines()]

def find_starting_points(input: list[str]) -> list[tuple[int, int]]:
    starting_points: list[tuple[int, int]] = []

    for row in range(len(input)):
        for col in range(len(input[row])):
            if input[row][col] == "A":
                starting_points.append((row, col))

    return starting_points

def is_xmas(input: list[str], starting_location: tuple[int, int], direction: Direction) -> bool:
    next_location = get_next_location(input, starting_location, direction)

    if next_location is not None and get_character_at(input, next_location) == "M":
        next_location = get_next_location(input, next_location, direction)

        if next_location is not None and get_character_at(input, next_location) == "A":
            next_location = get_next_location(input, next_location, direction)

            if next_location is not None and get_character_at(input, next_location) == "S":
                return True

    return False

def is_xmas_part_2(input: list[str], a_location: tuple[int, int]) -> bool:
    nw_location: tuple[int, int] | None = get_next_location(input, a_location, Direction.NW)
    ne_location: tuple[int, int] | None = get_next_location(input, a_location, Direction.NE)
    sw_location: tuple[int, int] | None = get_next_location(input, a_location, Direction.SW)
    se_location: tuple[int, int] | None = get_next_location(input, a_location, Direction.SE)

    nw_character: str | None = get_character_at(input, nw_location) if nw_location else None
    ne_character: str | None = get_character_at(input, ne_location) if ne_location else None
    sw_character: str | None = get_character_at(input, sw_location) if sw_location else None
    se_character: str | None = get_character_at(input, se_location) if se_location else None

    if nw_character is not None and ne_character is not None and sw_character is not None and se_character is not None:
        return (((nw_character == "M" and se_character == "S") or
                (nw_character == "S" and se_character == "M")) and
                ((ne_character == "M" and sw_character == "S") or
                (ne_character == "S" and sw_character == "M")))
    else:
        return False


if __name__ == "__main__":
    input: list[str] = parse_input("d4_input.txt")

    total: int = 0

    for starting_location in find_starting_points(input):
        xmas: bool = is_xmas_part_2(input, starting_location)

        print("Starting location : %s, xmas %s" % (starting_location, xmas))

        if xmas:
            total += 1

    print("total : %d" % (total))