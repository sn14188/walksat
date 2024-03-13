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

def get_initial_interpretation(n):
    interpretation = {}
    for i in range(1, n + 1):
        key = f"X{i}"
        value = random.choice([True, False])
        interpretation[key] = value

    print(f"- initial_interpretation: {interpretation}")
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
        if is_clause_satisfied(clause=clause, interpretation=interpretation):
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
    while time.time() - start_time < 0.001:
        satisfied_clauses, unsatisfied_clauses = evaluate_clauses(clauses=clauses, interpretation=initial_interpretation)
        satisfied, unsatisfied = len(satisfied_clauses), len(unsatisfied_clauses)
        print(f"- satisfied: {satisfied} / unsatisfied: {unsatisfied}")

        if satisfied == len(clauses):
            print(f"Success with {flips} flip(s)")
            return flips

        is_flip_greedy = random.choice([True, False])
        clause_to_flip = random.choice(unsatisfied_clauses)
        print("-" * 100)
        if is_flip_greedy:
            print("* GREEDY")
            print(f"- unsatisfied_clauses: {unsatisfied_clauses}")
            print(f"- clause_to_flip (random): {clause_to_flip}")
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
            print(f"- best_literal_to_flip (greedy): {best_literal} from {data}")
            flip_literal(initial_interpretation, best_literal)
        else:
            print("* RANDOM WALK")
            print(f"- unsatisfied_clauses: {unsatisfied_clauses}")
            print(f"- clause_to_flip (random): {clause_to_flip}")
            literal_to_flip = random.choice(clause_to_flip)
            print(f"- literal_to_flip (random): {literal_to_flip}")
            flip_literal(initial_interpretation, literal_to_flip)

        flips += 1

    print(f"Failure with {flips} flips")
    return -1

def simulation():
    # Generate 3SAT problems
    problems = []
    ratios = range(1, 11)
    c_values = list(range(20, 201, 20))
    n = 20
    for ratio in ratios:
        c = ratio * n
        for _ in range(50):
            problem = generate_randomized_3sat_problem(c, n)
            problems.append((c, problem))

    results = {}
    for c in range(20, 201, 20):
        results[c] = {
            "success": 0,
            "flips": []
        }
    for (c, problem) in problems:
        result = walk_sat(problem)
        if result != -1:
            results[c]["success"] += 1
            results[c]["flips"].append(result)

    print(results)

    successful_c_values = [c for c in c_values if results[c]["success"] > 0]
    success_counts, median_flips = [], []
    for c in successful_c_values:
        success_count = results[c]["success"]
        success_counts.append(success_count)

        if results[c]["flips"]:
            median_flip = median(results[c]["flips"])
            median_flips.append(median_flip)

    c_value_to_ratio = [c / n for c in successful_c_values]

    # Plots
    def plot_result(title, y, ylabel):
        plt.title(title)
        plt.plot(c_value_to_ratio, y)
        plt.xlabel("Ratio")
        plt.xticks(c_value_to_ratio)
        plt.ylabel(ylabel)
        plt.grid(True)
        plt.show()

    plot_result("WalkSAT Success Count by Ratio", success_counts, "Number of Successes")
    plot_result("Median Number of Flips by Ratio", median_flips, "Median Flips")

if __name__ == "__main__":
    simulation()
