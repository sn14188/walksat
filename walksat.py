import random

def generate_clause(n):
    clause_set = set()
    while len(clause_set) < 3:
        variable = f"X{random.randint(1, n)}"
        clause_set.add(variable)

    clause_list = list(clause_set)
    for i in range(len(clause_list)):
        if random.choice([True, False]):
            clause_list[i] = "¬" + clause_list[i]

    return clause_list

def generate_randomized_3sat_problem(c, n):
    clauses = []
    for _ in range(c):
        clauses.append(generate_clause(n))

    print(f"3SAT problem: {clauses}")
    return clauses

def is_clause_satisfied(clause, interpretation):
    for literal in clause:
        if literal.startswith("¬"):
            if not interpretation[literal.strip("¬")]:
                return True
        else:
            if interpretation[literal]:
                return True
    return False

def walk_sat(clauses):
    numbers = set()
    for clause in clauses:
        for literal in clause:
            numbers.add(int(literal.strip("¬")[1:]))
    n = max(numbers)

    initial_interpretation = {}
    for i in range(1, n + 1):
        key = f"X{i}"
        value = random.choice([True, False])
        initial_interpretation[key] = value
    print(f"- initial_interpretation: {initial_interpretation}")

    flips = 0
    max_flips = 10000
    while flips < max_flips:
        satisfied_clauses, unsatisfied_clauses = [], []
        satisfied, unsatisfied = 0, 0
        for clause in clauses:
            if is_clause_satisfied(clause=clause, interpretation=initial_interpretation):
                satisfied_clauses.append(clause)
                satisfied += 1
            else:
                unsatisfied_clauses.append(clause)
                unsatisfied += 1
        print(f"- satisfied: {satisfied} & unsatisfied: {unsatisfied}")
        assert satisfied + unsatisfied == len(clauses)
        if satisfied == len(clauses):
            print(f"flips done: {flips}")
            return flips

        is_flip_greedy = random.choice([True, False])
        print("-" * 100)
        if is_flip_greedy:
            print("* GREEDY")
            print(f"- unstatisfied_clauses: {unsatisfied_clauses}")
            clause_to_flip = random.choice(unsatisfied_clauses)
            print(f"- clause_to_flip (random): {clause_to_flip}")
            data = {}
            for literal_to_flip in clause_to_flip:
                satisfied, unsatisfied = 0, 0
                copy = initial_interpretation.copy()
                variable_to_flip = literal_to_flip.strip("¬")
                copy[variable_to_flip] = not copy[variable_to_flip]
                for clause in clauses:
                    if is_clause_satisfied(clause=clause, interpretation=copy):
                        satisfied += 1
                    else:
                        unsatisfied += 1
                data[literal_to_flip] = satisfied
            best_literal = max(data, key=data.get)
            print(f"- best_literal_to_flip (greedy): {best_literal} from {data}")
            variable_to_flip = best_literal.strip("¬")
            initial_interpretation[variable_to_flip] = not initial_interpretation[variable_to_flip]
        else:
            print("* RANDOM WALK")
            print(f"- unstatisfied_clauses: {unsatisfied_clauses}")
            clause_to_flip = random.choice(unsatisfied_clauses)
            print(f"- clause_to_flip (random): {clause_to_flip}")
            literal_to_flip = random.choice(clause_to_flip)
            print(f"- literal_to_flip (random): {literal_to_flip}")
            variable_to_flip = literal_to_flip.strip("¬")
            initial_interpretation[variable_to_flip] = not initial_interpretation[variable_to_flip]
        flips += 1

    print("failure")

if __name__ == "__main__":
    walk_sat(generate_randomized_3sat_problem(20, 20))
