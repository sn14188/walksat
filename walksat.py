import random
import time
import matplotlib.pyplot as plt
from statistics import median

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

    # print(f"3SAT problem: {clauses}")
    return clauses

def generate_problems_for_simulation(c_values, n, iterations):
    problems = []
    for c in c_values:
        for _ in range(50):
            problem = generate_randomized_3sat_problem(c, 20)
            problems.append((c, problem))

    return problems

def get_initial_interpretation(n):
    interpretation = {}
    for i in range(1, n + 1):
        key = f"X{i}"
        value = random.choice([True, False])
        interpretation[key] = value

    # print(f"- initial_interpretation: {interpretation}")
    return interpretation

def is_clause_satisfied(clause, interpretation):
    for literal in clause:
        if literal.startswith("¬"):
            if not interpretation[literal.strip("¬")]:
                return True
        else:
            if interpretation[literal]:
                return True
    return False

def evaluate_clauses(clauses, interpretation):
    satisfied_clauses, unsatisfied_clauses = [], []
    for clause in clauses:
        if is_clause_satisfied(clause, interpretation):
            satisfied_clauses.append(clause)
        else:
            unsatisfied_clauses.append(clause)

    return satisfied_clauses, unsatisfied_clauses

def flip_literal(interpretation, literal):
    interpretation[literal.strip("¬")] ^= True

def walk_sat(clauses):
    numbers = set()
    for clause in clauses:
        for literal in clause:
            numbers.add(int(literal.strip("¬")[1:]))
    n = max(numbers)
    initial_interpretation = get_initial_interpretation(n)

    flips = 0
    start_time = time.time()
    while time.time() - start_time < 1:
        satisfied_clauses, unsatisfied_clauses = evaluate_clauses(clauses,
                                                                  initial_interpretation)
        satisfied, unsatisfied = len(satisfied_clauses), len(unsatisfied_clauses)
        # print(f"- satisfied: {satisfied} / unsatisfied: {unsatisfied}")

        if satisfied == len(clauses):
            print(f"Success with {flips} flip(s)")
            return flips

        is_flip_greedy = random.choice([True, False])
        clause_to_flip = random.choice(unsatisfied_clauses)
        # print("-" * 100)
        if is_flip_greedy:
            # print("* GREEDY")
            # print(f"- unsatisfied_clauses: {unsatisfied_clauses}")
            # print(f"- clause_to_flip (random): {clause_to_flip}")
            data = {}
            for literal_to_flip in clause_to_flip:
                satisfied, unsatisfied = 0, 0
                temp = initial_interpretation.copy()
                variable_to_flip = literal_to_flip.strip("¬")
                temp[variable_to_flip] = not temp[variable_to_flip]
                for clause in clauses:
                    if is_clause_satisfied(clause=clause, interpretation=temp):
                        satisfied += 1
                    else:
                        unsatisfied += 1
                data[literal_to_flip] = satisfied
            best_literal = max(data, key=data.get)
            # print(f"- best_literal_to_flip (greedy): {best_literal} from {data}")
            flip_literal(initial_interpretation, best_literal)
        else:
            # print("* RANDOM WALK")
            # print(f"- unsatisfied_clauses: {unsatisfied_clauses}")
            # print(f"- clause_to_flip (random): {clause_to_flip}")
            literal_to_flip = random.choice(clause_to_flip)
            # print(f"- literal_to_flip (random): {literal_to_flip}")
            flip_literal(initial_interpretation, literal_to_flip)

        flips += 1

    print(f"Failure with {flips} flips")
    return -1

def simulation():
    # Generate 50 3SAT problems for each c values
    n = 20
    iterations = 50
    c_values = list(range(20, 201, 20))
    problems = generate_problems_for_simulation(c_values, n, iterations)

    # Get the results as dictionary
    results = {}
    for c in c_values:
        results[c] = {
            "success": 0,
            "flips": []
        }
    for (c, problem) in problems:
        result = walk_sat(problem)
        if result != -1:
            results[c]["success"] += 1
            results[c]["flips"].append(result)
    # print(results)

    # Generate plots
    success_counts, median_flips = [], []
    successful_c_values = []
    for c in c_values:
        success_counts.append(results[c]["success"])
        if results[c]["flips"]:
            median_flip = median(results[c]["flips"])
            median_flips.append(median_flip)
            successful_c_values.append(c)
    # print(median_flips)

    c_to_ratio = [c / n for c in c_values]
    successful_c_to_ratio = [c / n for c in successful_c_values]

    plt.figure(figsize=(10, 4))

    plt.subplot(1, 2, 1)
    plt.title("WalkSAT Success Count")
    plt.plot(c_to_ratio, success_counts)
    plt.xlabel("Ratio (C/N)")
    plt.xticks(c_to_ratio)
    plt.ylabel("Number of Successes")
    plt.grid(True)

    plt.subplot(1, 2, 2)
    plt.title("Median Number of Flips")
    plt.plot(successful_c_to_ratio, median_flips)
    plt.xlabel("Ratio (C/N)")
    plt.xticks(successful_c_to_ratio)
    plt.ylabel("Median Flips")
    plt.grid(True)

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    simulation()
