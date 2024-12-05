from dataclasses import dataclass


@dataclass
class Problem:
    rules: list[tuple[int, int]]
    updates: list[list[int]]

def parse(filename: str) -> Problem:
    with open(filename) as f:
        rules: list[tuple[int, int]] = []
        updates: list[list[int]] = []

        for line in f.readlines():
            if line.find("|") != -1:
                rules.append(tuple([int(x) for x in line.strip().split("|")]))
            elif line.find(",") != -1:
                updates.append([int(x) for x in line.strip().split(",")])

        return Problem(rules, updates)

def update_satisfies(update: list[int], rule: tuple[int, int]) -> bool:
    if rule[0] in update and rule[1] in update:
        index_a: int = update.index(rule[0])
        index_b: int = update.index(rule[1])

        return index_a < index_b

    return True

def fix_rule(update: list[int], rule: tuple[int, int]) -> list[int]:
    index_a: int = update.index(rule[0])
    index_b: int = update.index(rule[1])

    new_update: list[int] = [0] * len(update)

    for i in range(len(update)):
        if i < index_b:
            new_update[i] = update[i]
        elif i > index_b and i <= index_a:
            new_update[i - 1] = update[i]
        elif i > index_a:
            new_update[i] = update[i]

        new_update[index_a] = update[index_b]

    return new_update

def check(update: list[int], rules: list[tuple[int, int]]) -> list[int]:
    while True:
        valid: bool = True
        violated_rules: list[tuple[int, int]] = []

        for rule in rules:
            if not update_satisfies(update, rule):
                valid = False
                violated_rules.append(rule)

        if valid:
            print("Update %s is valid" % (update))
            return update
        else:
            print("Update %s is not valid, violates rules : %s" % (update, violated_rules))

            for rule in rules:
                if not update_satisfies(update, rule):
                    fixed = fix_rule(update, rule)
                    print("Fixing rule %s : %s -> %s" % (rule, update, fixed))
                    update = fixed

if __name__ == "__main__":
    problem: Problem = parse("d5_input.txt")

    count: int = 0

    for update in problem.updates:
        update_valid: bool = True
        violated_rules: list[tuple[int, int]] = []

        for rule in problem.rules:
            if not update_satisfies(update, rule):
                update_valid = False
                violated_rules.append(rule)

        while not update_valid:
            update_valid = True

            print("Update %s is not valid, violates rules : %s" % (update, violated_rules))

            fixed = check(update, problem.rules)

            violated_rules = []

            for rule in problem.rules:
                if not update_satisfies(fixed, rule):
                    update_valid = False

            if update_valid:
                count += fixed[int((len(fixed) - 1) / 2)]

    print(count)
