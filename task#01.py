import random

# Default Dataset [cite: 40-47]
DEFAULT_ITEMS = [
    (2, 12), (1, 10), (3, 20), (2, 15), (4, 25),
    (5, 30), (7, 42), (6, 35), (3, 18), (2, 14),
    (8, 50), (9, 55), (4, 24), (5, 28), (1, 8),
    (6, 33), (7, 40), (3, 16), (2, 11), (4, 22),
    (10, 60), (9, 52), (5, 29), (6, 34), (2, 13),
    (1, 7), (8, 48), (7, 39), (3, 19), (4, 23)
]

def get_user_input():
     
    choice = input("Use default dataset? (y/n): ").lower()
    if choice == 'y':
        return DEFAULT_ITEMS, 60
    
    items = []
    n = int(input("Enter number of items: "))
    for i in range(n):
        w = int(input(f"Weight of item {i+1}: "))
        v = int(input(f"Value of item {i+1}: "))
        items.append((w, v))
    capacity = int(input("Enter knapsack capacity: "))
    return items, capacity

def initialize_population(size, num_items):
     
    return [[random.randint(0, 1) for _ in range(num_items)] for _ in range(size)]

def calculate_weight(chromosome, items):
     
    return sum(chromosome[i] * items[i][0] for i in range(len(items)))

def fitness(chromosome, items, max_weight):
    
    total_weight = calculate_weight(chromosome, items)
    if total_weight > max_weight:
        return 0
    return sum(chromosome[i] * items[i][1] for i in range(len(items)))

def roulette_wheel_selection(population, fitnesses):
     
    total_f = sum(fitnesses)
    if total_f == 0: return random.choice(population)
    pick = random.uniform(0, total_f)
    current = 0
    for i, f in enumerate(fitnesses):
        current += f
        if current > pick:
            return population[i]

def tournament_selection(population, fitnesses, k=3):
     
    selected_indices = random.sample(range(len(population)), k)
    best_idx = max(selected_indices, key=lambda i: fitnesses[i])
    return population[best_idx]

def crossover(parent1, parent2):
     
    point = random.randint(1, len(parent1) - 1)
    child1 = parent1[:point] + parent2[point:]
    child2 = parent2[:point] + parent1[point:]
    return child1, child2

def mutate(chromosome, mutation_rate):
     
    for i in range(len(chromosome)):
        if random.random() < mutation_rate:
            chromosome[i] = 1 - chromosome[i]

def genetic_algorithm(items, max_weight, selection_method):
    pop_size, generations, mut_rate = 30, 50, 0.05
    pop = initialize_population(pop_size, len(items))
    best_sol = None
    best_fit = -1

    for _ in range(generations):
        fits = [fitness(ind, items, max_weight) for ind in pop]
        
        # Track best solution  
        for i, f in enumerate(fits):
            if f > best_fit:
                best_fit = f
                best_sol = pop[i][:]

        new_pop = []
        while len(new_pop) < pop_size:
            # Selection Dispatcher  
            if selection_method == '1':
                p1 = roulette_wheel_selection(pop, fits)
                p2 = roulette_wheel_selection(pop, fits)
            else:
                p1 = tournament_selection(pop, fits)
                p2 = tournament_selection(pop, fits)
            
            c1, c2 = crossover(p1, p2)
            mutate(c1, mut_rate)
            mutate(c2, mut_rate)
            new_pop.extend([c1, c2])
        pop = new_pop[:pop_size]

    return best_sol, best_fit

def main():
    items, max_weight = get_user_input()
    print("\nSelect Selection Method:\n1. Roulette Wheel\n2. Tournament")
    method = input("Choice (1/2): ")
    
    best_chrom, best_val = genetic_algorithm(items, max_weight, method)
    
    # Display results [cite: 175-182]
    print("\n--- Final Solution ---")
    print(f"Selection Method: {'Roulette' if method=='1' else 'Tournament'}")
    print(f"Best Chromosome: {best_chrom}")
    print(f"Total Value (Fitness): {best_val}")
    print(f"Total Weight: {calculate_weight(best_chrom, items)}")
    print(f"Selected Item Indices: {[i for i, val in enumerate(best_chrom) if val == 1]}")

if __name__ == "__main__":
    main()


    # --- TEST SCRIPT FOR TASK 01 ---
def test_knapsack():
     
    test_items = [
        (10, 60),   # Item 0
        (20, 100),  # Item 1
        (30, 120),  # Item 2
        (40, 150)   # Item 3
    ]
    test_capacity = 50  

    print("--- Running Knapsack Test Case ---")
    print(f"Items: {test_items} | Capacity: {test_capacity}")

    
    best_chrom, best_val = genetic_algorithm(test_items, test_capacity, selection_method='2')
    
    total_w = calculate_weight(best_chrom, test_items) 
    
    print(f"Selected Chromosome: {best_chrom}")  
    print(f"Total Weight: {total_w}") 
    print(f"Total Value: {best_val}")  
    
    if total_w <= test_capacity:
        print("Result: PASS (Within Capacity)")
    else:
        print("Result: FAIL (Over Capacity)")

test_knapsack()
