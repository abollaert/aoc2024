import functools


def read_input(filename: str) -> dict[int, int]:
    with open(filename) as f:
        stone_count: dict[int, int] = {}
        stones: list[int] = [int(part.strip()) for part in f.readline().split(" ")]

        for stone in stones:
            if stone not in stone_count:
                stone_count[stone] = 1
            else:
                stone_count[stone] += 1

    return stone_count

def blink_one(stone: int) -> list[int]:
    if stone == 0:
        return [1]
    elif len(str(stone)) % 2 == 0:
        stone_as_str: str = str(stone)
        left: int = int(stone_as_str[0: int(len(stone_as_str) / 2)])
        right: int = int(stone_as_str[int(len(stone_as_str) / 2):])

        return [left, right]
    else:
        return [stone * 2024]

def blink(stones: dict[int, int]) -> dict[int, int]:
    new_stone_count: dict[int, int] = {}

    for stone in stones:
        num_stones: int = stones[stone]
        new_stones: list[int] = blink_one(stone)

        stones[stone] = 0

        for new_stone in new_stones:
            if new_stone not in new_stone_count:
                new_stone_count[new_stone] = num_stones
            else:
                new_stone_count[new_stone] += num_stones

    return new_stone_count

if __name__ == "__main__":
    stones: dict[int, int] = read_input("d11_input.txt")

    for i in range(75):
        stones = blink(stones)

    total: int = 0

    for stone in stones:
        total += stones[stone]

    print(total)