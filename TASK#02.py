import heapq
import time

class PuzzleNode:
    def __init__(self, state, parent, move, g_cost, h_cost):
        self.state = state
        self.parent = parent
        self.move = move
        self.g_cost = g_cost
        self.h_cost = h_cost
        self.f_cost = g_cost + h_cost 

    def __lt__(self, other):
        return self.f_cost < other.f_cost  

    @staticmethod
    def calculate_heuristic(state, goal_state, heuristic_type="manhattan"):
        distance = 0
        goal_positions = {goal_state[i][j]: (i, j) for i in range(4) for j in range(4)}

        for i in range(4):
            for j in range(4):
                value = state[i][j]
                if value == 0: continue
                goal_x, goal_y = goal_positions[value]

                if heuristic_type == "manhattan":
                    distance += abs(i - goal_x) + abs(j - goal_y)
                elif heuristic_type == "euclidean":
                    distance += ((i - goal_x)**2 + (j - goal_y)**2) ** 0.5
                elif heuristic_type == "misplaced_tiles":
                    if (i, j) != (goal_x, goal_y): distance += 1
                elif heuristic_type == "row_column":
                    if i != goal_x: distance += 1
                    if j != goal_y: distance += 1
                elif heuristic_type == "linear_conflict":
                    # Basic Manhattan + Row Conflict logic
                    distance += abs(i - goal_x) + abs(j - goal_y)
                    if i == goal_x: # Same row
                        for k in range(j + 1, 4):
                            other_val = state[i][k]
                            if other_val != 0 and goal_positions[other_val][0] == i:
                                if goal_positions[other_val][1] < goal_y:
                                    distance += 2
        return distance

class PuzzleSolver:
    def __init__(self, start_state, goal_state):
        self.start_state = start_state
        self.goal_state = goal_state  

    def is_solvable(self, state):
        flat = [val for row in state for val in row if val != 0]
        inversions = sum(1 for i in range(len(flat)) for j in range(i + 1, len(flat)) if flat[i] > flat[j])  
        
        blank_row_from_bottom = 0
        for i in range(4):
            if 0 in state[i]:
                blank_row_from_bottom = 4 - i  
                break
        
        # For n=4 (even), (Inversions + BlankRowFromBottom) must be odd 
        return (inversions + blank_row_from_bottom) % 2 != 0

    def generate_moves(self, state):
        moves = []
        x, y = next((r, c) for r in range(4) for c in range(4) if state[r][c] == 0)
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < 4 and 0 <= ny < 4:
                new_state = [row[:] for row in state]
                new_state[x][y], new_state[nx][ny] = new_state[nx][ny], new_state[x][y]
                moves.append(new_state)
        return moves

    def astar_search(self, heuristic_type="manhattan"):
        open_list = []
        start_h = PuzzleNode.calculate_heuristic(self.start_state, self.goal_state, heuristic_type)
        start_node = PuzzleNode(self.start_state, None, None, 0, start_h)
        heapq.heappush(open_list, start_node)
        
        visited = set()
        
        while open_list:
            current = heapq.heappop(open_list)
            if current.state == self.goal_state:
                return current
            
            state_tuple = tuple(map(tuple, current.state))
            if state_tuple in visited: continue
            visited.add(state_tuple)

            for move in self.generate_moves(current.state):
                h_cost = PuzzleNode.calculate_heuristic(move, self.goal_state, heuristic_type)
                child = PuzzleNode(move, current, None, current.g_cost + 1, h_cost)
                heapq.heappush(open_list, child)
        return None

    def trace_solution(self, node):
        path = []
        while node:
            path.append(node.state)
            node = node.parent
        for step in reversed(path):
            for row in step: print(row)
            print()

def main():
    goal_state = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 0]] 

    # Test Case 1: Solvable  
    initial_solvable = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 0, 15]]
    
    # Test Case 2: Unsolvable 
    initial_unsolvable = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 15, 14, 0]]

    for i, start_state in enumerate([initial_solvable, initial_unsolvable], 1):
        print(f"--- Test Case {i} ---")
        solver = PuzzleSolver(start_state, goal_state)  
        
        if solver.is_solvable(start_state): 

            print("The puzzle is solvable. Running A* Search...")  
            start_time = time.time()  
            solution = solver.astar_search(heuristic_type="manhattan")  
            end_time = time.time()
            
            if solution:
                solver.trace_solution(solution)  
                print(f"Execution Time: {end_time - start_time:.5f} seconds")  
        else:
            print("The puzzle is NOT solvable.")  
        print("\n")

if __name__ == "__main__":
    main()