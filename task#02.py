import random
import math

 
CITIES = {0: (2, 3), 1: (5, 4), 2: (1, 7), 3: (6, 8), 4: (9, 2), 5: (4, 6), 6: (8, 7), 7: (3, 9)}

def distance(c1, c2):
     
    return math.sqrt((c1[0]-c2[0])**2 + (c1[1]-c2[1])**2)

def total_distance(route, cities):
     
    dist = 0
    for i in range(len(route)):
        dist += distance(cities[route[i]], cities[route[(i+1) % len(route)]])
    return dist

def fitness(route, cities):
     
    return 1 / total_distance(route, cities)

def initialize_population(size, num_cities):
     
    pop = []
    base = list(range(num_cities))
    for _ in range(size):
        route = base[:]
        random.shuffle(route)
        pop.append(route)
    return pop

def crossover_ox(p1, p2):
     
    size = len(p1)
    a, b = sorted(random.sample(range(size), 2))
    
    def fill_child(parent1, parent2, start, end):
        child = [None] * size
        child[start:end+1] = parent1[start:end+1]
        
        p2_remaining = [item for item in parent2 if item not in child]
        idx = 0
        for i in range(size):
            if child[i] is None:
                child[i] = p2_remaining[idx]
                idx += 1
        return child

    return fill_child(p1, p2, a, b), fill_child(p2, p1, a, b)

def mutate_swap(route, rate):
     
    if random.random() < rate:
        idx1, idx2 = random.sample(range(len(route)), 2)
        route[idx1], route[idx2] = route[idx2], route[idx1]

def genetic_algorithm(cities, selection_method):
    pop_size, gens, mut_rate = 30, 100, 0.05
    pop = initialize_population(pop_size, len(cities))
    best_route = None
    max_fit = -1

    for _ in range(gens):
        fits = [fitness(r, cities) for r in pop]
        
        for i, f in enumerate(fits):
            if f > max_fit:
                max_fit = f
                best_route = pop[i][:]

        new_pop = []
        while len(new_pop) < pop_size:
            # Selection Dispatcher 1
            if selection_method == '1':
                # Simple Roulette implementation for TSP
                total_f = sum(fits)
                pick = random.uniform(0, total_f)
                curr = 0
                for i, f in enumerate(fits):
                    curr += f
                    if curr > pick:
                        p1 = pop[i]; break
                p2 = random.choice(pop) # Simplified second parent
            else:
                # Tournament [cite: 238, 268]
                def tourney():
                    s = random.sample(range(pop_size), 3)
                    return pop[max(s, key=lambda i: fits[i])]
                p1, p2 = tourney(), tourney()

            c1, c2 = crossover_ox(p1, p2)
            mutate_swap(c1, mut_rate)
            mutate_swap(c2, mut_rate)
            new_pop.extend([c1, c2])
        pop = new_pop[:pop_size]
    
    return best_route, max_fit

def main():
    print("TSP Genetic Algorithm")
    method = input("Select Selection (1: Roulette, 2: Tournament): ")
    best_route, best_fit = genetic_algorithm(CITIES, method)
    
    # Display results [cite: 281-287]
    print("\n--- Best Route Found ---")
    print(f"Route: {best_route}")
    print(f"Total Distance: {total_distance(best_route, CITIES):.2f}")
    print(f"Fitness Value: {best_fit:.6f}")
    print(f"Method Used: {'Roulette' if method=='1' else 'Tournament'}")

if __name__ == "__main__":
    main()



# --- TEST SCRIPT FOR TASK 02 ---
def test_tsp():
    
     
    square_cities = {
        0: (0, 0),
        1: (0, 10),
        2: (10, 10),
        3: (10, 0)
    }

    print("\n--- Running TSP Test Case (Square Path) ---")
    
    
    best_route, best_fit = genetic_algorithm(square_cities, selection_method='2')
    
    dist = total_distance(best_route, square_cities)  
    
    print(f"Best Route Found: {best_route}")  
    print(f"Total Distance: {dist:.2f}") 
    print(f"Fitness (1/Dist): {best_fit:.6f}")  
    
    
    if round(dist) == 40:
        print("Result: PASS (Optimal Path Found)")
    else:
        print("Result: CHECK (GA found a valid but perhaps sub-optimal path)")

test_tsp()