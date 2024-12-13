from queue import Queue

from ansible.plugins.filter.core import to_yaml


def parse_input(filename: str) -> list[str]:
    with open(filename) as f:
        return [line.strip() for line in f]

def find_trailheads(map: list[str]) -> list[tuple[int, int]]:
    trailheads: list[tuple[int, int]] = []

    for row in range(len(map)):
        for col in range(len(map[row])):
            if map[row][col] == "0":
                trailheads.append((row, col))

    return trailheads

def height(map: list[str], location: tuple[int, int]) -> int:
    if map[location[0]][location[1]] == ".":
        return -1

    return int(map[location[0]][location[1]])

def find_next(map: list[str], location: tuple[int, int]) -> list[tuple[int, int]]:
    next_locations: list[tuple[int, int]] = []

    left: tuple[int, int] = (location[0], location[1] - 1)
    up: tuple[int, int] = (location[0] - 1, location[1])
    right: tuple[int, int] = (location[0], location[1] + 1)
    down: tuple[int, int] = (location[0] + 1, location[1])

    current_height: int = height(map, location)

    for next_row, next_col in (left, up, right, down):
        if next_row >= 0 and next_row < len(map) and next_col >= 0 and next_col < len(map[next_row]):
            next_height: int = height(map, (next_row, next_col))

            if next_height == current_height + 1:
                next_locations.append((next_row, next_col))

    return next_locations

def find_trails(map: list[str], trailhead: tuple[int, int]) -> list[list[tuple[int, int]]]:
    fringe: Queue[tuple[tuple[int, int], list[tuple[int, int]]]] = Queue()
    fringe.put((trailhead, []))
    paths: list[list[tuple[int, int]]] = []

    while not fringe.empty():
        next_location: tuple[tuple[int, int], list[tuple[int, int]]] = fringe.get_nowait()

        if height(map, next_location[0]) == 9:
            next_location[1].append(next_location[0])
            paths.append(next_location[1])
        elif next_location[0] not in next_location[1]:
            neighbors: list[tuple[int, int]] = find_next(map, next_location[0])

            for neighbor in neighbors:
                path: list[tuple[int, int]] = []

                path.extend(next_location[1])
                path.append(next_location[0])

                print("Exploring %s, height %d via %s" % (neighbor, height(map, neighbor), path))
                fringe.put((neighbor, path))

    return paths

if __name__ == "__main__":
    map: list[str] = parse_input("d10_input.txt")

    trailheads: list[tuple[int, int]] = find_trailheads(map)

    total_endpoints: int = 0
    total_trails: int = 0

    for trailhead in trailheads:
        trails: list[list[tuple[int, int]]] = find_trails(map, trailhead)

        print(trails)

        endpoints: set[tuple[int, int]] = set()

        for trail in trails:
            endpoints.add(trail[len(trail) - 1])

        total_endpoints += len(endpoints)
        total_trails += len(trails)

    print(total_endpoints)
    print(total_trails)