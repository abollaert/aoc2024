import re

REGEX_PATTERN: str = "mul\((\d+),(\d+)\)"
REGEX: re.Pattern = re.compile(REGEX_PATTERN)

def parse_input(filename: str) -> str:
    data: str = ""

    with open(filename) as f:
        for line in f.readlines():
            data += line

    return data

def prune_input(input: str) -> str:
    pruned_data: str = ""
    instructions_enabled: bool = True
    index: int = 0
    section_start: int = 0
    section_end: int = 0

    while index != -1:
        if instructions_enabled:
            index = input.find("don't()", index, None)
            print(index)
            section_end = index

            if index == -1:
                section_end = len(input)

            pruned_data += input[section_start:section_end]

            section_start = index
            instructions_enabled = False
        else:
            index = input.find("do()", index, None)
            section_start = index
            instructions_enabled = True

    print(pruned_data)
    return pruned_data


if __name__ == '__main__':
    input: str = prune_input(parse_input("d3_input.txt"))
    total: int = 0

    matches: list[tuple[str, str]] = re.findall(REGEX, input)

    for match in matches:
        print(match)
        total += int(match[0]) * int(match[1])

    print(total)