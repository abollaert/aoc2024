def parse_input(filename: str) -> list[str]:
    with open(filename) as f:
        return [line.strip() for line in f]

def find_antennas(map: list[str]) -> dict[str, list[tuple[int, int]]]:
    antenna_locations: dict[str, list[tuple[int, int]]] = {}

    for row in range(len(map)):
        for col in range(len(map[0])):
            if map[row][col] != ".":
                frequency: str = map[row][col]

                locations_for_frequency: list[tuple[int, int]] = antenna_locations.get(frequency, None)

                if locations_for_frequency is None:
                    locations_for_frequency = []
                    antenna_locations[frequency] = locations_for_frequency

                locations_for_frequency.append((row, col))

    return antenna_locations

def is_on_map(map: list[str], location: tuple[int, int]) -> bool:
    return location[0] >= 0 and location[0] < len(map) and location[1] >= 0 and location[1] < len(map[0])

def antinodes_for_frequency(map: list[str],
                            antennas: list[tuple[int, int]]) -> list[tuple[int, int]]:
    antinode_locations: list[tuple[int, int]] = []

    for antenna in antennas:
        for other_antenna in antennas:
            if other_antenna != antenna:
                distance_row: int = antenna[0] - other_antenna[0]
                distance_col: int = antenna[1] - other_antenna[1]

                still_on_map: bool = True
                multiplier: int = 0

                while still_on_map:
                    antinode_1: tuple[int, int] = (antenna[0] + distance_row * multiplier, antenna[1] + distance_col * multiplier)
                    antinode_2: tuple[int, int] = (other_antenna[0] - distance_row * multiplier, other_antenna[1] - distance_col * multiplier)

                    print("Frequency %s, antenna %s, other antenna %s : antinode 1 %s, antinode 2 %s" % (frequency, antenna, other_antenna, antinode_1, antinode_2))

                    if is_on_map(map, antinode_1) and antinode_1 not in antinode_locations:
                        antinode_locations.append(antinode_1)

                    if is_on_map(map, antinode_2) and antinode_2 not in antinode_locations:
                        antinode_locations.append(antinode_2)

                    multiplier += 1
                    still_on_map = is_on_map(map, antinode_1) or is_on_map(map, antinode_2)

    return antinode_locations

if __name__ == "__main__":
    map: list[str] = parse_input("d8_input.txt")

    antennas: dict[str, list[tuple[int, int]]] = find_antennas(map)
    antinode_locations: list[tuple[int, int]] = []

    for frequency in antennas:
        locations_for_frequency: list[tuple[int, int]] = antinodes_for_frequency(map, antennas[frequency])

        for location in locations_for_frequency:
            if location not in antinode_locations:
                antinode_locations.append(location)

    print(antinode_locations)
    print(len(antinode_locations))

