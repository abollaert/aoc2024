def parse_input(input_file_location: str) -> tuple[list[int], list[int]]:
    output: tuple[list[int], list[int]] = ([], [])
    with open(input_file_location) as input_file:
        for line in input_file.readlines():
            numbers: list[int] = [int(x) for x in line.split()]

            output[0].append(numbers[0])
            output[1].append(numbers[1])

    output[0].sort()
    output[1].sort()

    return output

def calculate_total_distance(input: tuple[list[int], list[int]]) -> int:
    return sum([abs(x - y) for x, y in zip(input[0], input[1])])

def count_occurrences(numbers: list[int]) -> dict[int, int]:
    occurrences: dict[int, int] = {}

    for number in numbers:
        if number in occurrences:
            occurrences[number] += 1
        else:
            occurrences[number] = 1

    return occurrences

def calculate_similarity(input: tuple[list[int], list[int]]) -> int:
    similarity: int = 0

    occurrences_left: dict[int, int] = count_occurrences(input[0])
    occurrences_right: dict[int, int] = count_occurrences(input[1])

    for number in occurrences_left:
        right: int = occurrences_right.get(number, 0)
        similarity += number * occurrences_left[number] * right

    return similarity

if __name__ == '__main__':
    input_data: tuple[list[int], list[int]] = parse_input("d1_input.txt")

    print(calculate_total_distance(input_data))
    print(calculate_similarity(input_data))