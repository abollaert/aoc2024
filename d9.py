def parse_input(filename: str) -> list[int]:
    with open(filename) as f:
        disk: list[int] = []

        disk_map: str = f.readline().strip()

        i: int = 0
        file_id: int = 0

        while i < len(disk_map):
            num_blocks: int = int(disk_map[i])
            free_space: int = int(disk_map[i + 1]) if i < len(disk_map) - 1 else 0

            print("Num blocks %d, free space %d" % (num_blocks, free_space))

            for j in range(num_blocks):
                disk.append(file_id)

            for j in range(free_space):
                disk.append(-1)

            file_id += 1
            i += 2

    return disk

def find_first_free_index(disk: list[int], size: int) -> int:
    for i in range(len(disk)):
        if disk[i] == -1:
            large_enough: bool = True

            for j in range(size):
                if i + j >= len(disk):
                    return -1

                if disk[i + j] != -1:
                    large_enough = False
                    break

            if large_enough:
                return i

    return -1

def find_last_block(disk: list[int], file_id: int | None) -> tuple[int, int, int] | None:
    i: int = len(disk) - 1

    while i >= 0:
        if disk[i] != -1 and (file_id == None or disk[i] == file_id):
            j: int = 0

            while disk[i - j] == disk[i]:
                j += 1

            return (disk[i], (i - j) + 1, j)

        i -= 1

    return None

def compact_disk(disk: list[int]):
    last_block = find_last_block(disk, file_id=None)

    if last_block is None:
        return

    #print("Last block file ID %d, index %d, size %d" % (last_block[0], last_block[1], last_block[2]))

    file_id, index, size = last_block
    first_free: int = find_first_free_index(disk, size)

    #print("First free index of size %d: %d" % (size, first_free))

    finished: bool = False

    while not finished:
        if first_free != -1 and first_free < index:
            for i in range(size):
                disk[first_free + i] = file_id
                disk[index + i] = -1

        #print_disk(disk)

        last_block = find_last_block(disk, file_id=file_id - 1)

        if last_block is None:
            return

        #print("Last block file ID %d, index %d, size %d" % (last_block[0], last_block[1], last_block[2]))

        file_id, index, size = last_block
        first_free = find_first_free_index(disk, size)

        #print("First free index of size %d: %d" % (size, first_free))

    print_disk(disk)

def print_disk(disk: list[int]) -> None:
    for i in range(len(disk)):
        if disk[i] == -1:
            print(".", end="")
        else:
            print(str(disk[i]), end="")

    print("\n", end="")

def checksum_disk(disk: list[int]) -> int:
    checksum: int = 0

    for i in range(len(disk)):
        if disk[i] != -1:
            checksum += i * disk[i]

    return checksum


if __name__ == "__main__":
    disk = parse_input("d9_input.txt")
    print_disk(disk)
    compact_disk(disk)

    print(checksum_disk(disk))
