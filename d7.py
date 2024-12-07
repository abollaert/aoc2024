from dataclasses import dataclass
from enum import IntEnum, StrEnum

class Operator(StrEnum):
    PLUS = '+'
    MULTIPLY = '*'
    CONCAT = "||"

@dataclass
class Equation:
    result: int
    operands: list[int]

def parse_input(filename: str) -> list[Equation]:
    equations: list[Equation] = []

    with open(filename) as f:
        for line in f.readlines():
            parts: list[str] = line.strip().split(":")

            result: int = int(parts[0])
            operands: list[int] = [int(x) for x in parts[1].strip().split(" ")]

            equations.append(Equation(result, operands))

    return equations

def generate_possible_solutions(equation: Equation) -> list[list[Operator]]:
    operators: list[list[Operator]] = []

    for i in range(len(equation.operands) - 1):
        if len(operators) == 0:
            operators.append([Operator.PLUS])
            operators.append([Operator.MULTIPLY])
            operators.append([Operator.CONCAT])
        else:
            new_operators: list[list[Operator]] = []

            for operation_list in operators:
                new_operators.append(operation_list + [Operator.PLUS])
                new_operators.append(operation_list + [Operator.MULTIPLY])
                new_operators.append(operation_list + [Operator.CONCAT])

            operators = new_operators

    return operators

def can_be_solved(equation: Equation) -> bool:
    possible_solutions: list[list[Operator]] = generate_possible_solutions(equation)

    for solution in possible_solutions:
        result: int = equation.operands[0]

        for i in range(len(solution)):
            operation: Operator = solution[i]

            if operation == Operator.PLUS:
                result = result + equation.operands[i + 1]
            elif operation == Operator.MULTIPLY:
                result = result * equation.operands[i + 1]
            elif operation == Operator.CONCAT:
                result = int(str(result) + str(equation.operands[i + 1]))

        #print("Equation %s : solution %s, result %d" % (equation, solution, result))

        if result == equation.result:
            return True

    return False

if __name__ == "__main__":
    equations: list[Equation] = parse_input("d7_input.txt")

    count: int = 0

    for equation in equations:
        if can_be_solved(equation):
            print("Equation %s can be solved" % (equation))
            count += equation.result

        else:
            print("Equation %s can't be solved" % (equation))

    print(count)