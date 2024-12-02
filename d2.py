def is_increasing(input: list[int]) -> bool:
    for i in range(1, len(input)):
        prev: int = input[i - 1]
        current: int = input[i]

        if current <= prev or current - prev > 3:
            return False

    return True

def is_decreasing(input: list[int]) -> bool:
    for i in range(1, len(input)):
        prev: int = input[i - 1]
        current: int = input[i]

        if current >= prev or prev - current > 3:
            return False

    return True

def is_safe(input: list[int]) -> bool:
    return is_decreasing(input) or is_increasing(input)

def parse_data(file_name: str) -> list[list[int]]:
    input_data: list[list[int]] = []

    with open(file_name) as file:
        for line in file:
            line_data: list[int] = [int(x) for x in line.split()]

            input_data.append(line_data)

    return input_data

def generate_variants(input_data: list[int]) -> list[list[int]]:
    variants: list[list[int]] = []

    for i in range(len(input_data)):
        variant: list[int] = input_data.copy()
        variant.pop(i)

        variants.append(variant)

    return variants

if __name__ == '__main__':
    input_data: list[list[int]] = parse_data('d2_input.txt')

    total_safe: int = 0

    for line in input_data:
        if is_safe(line):
            total_safe += 1
        else:
            for variant in generate_variants(line):
                if is_safe(variant):
                    total_safe += 1
                    break

    print(total_safe)
