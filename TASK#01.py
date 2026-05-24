class Puzzle:
        def __init__(self, initial_state, goal_state):
            self.initial_state = initial_state
            self.goal_state = goal_state


        def is_solvable(self, state):
            flat = []
            
             
            for row in state:
                for val in row:
                    if val != 0:
                        flat.append(val)

            
            inversions = 0
            for i in range(len(flat)):
                for j in range(i + 1, len(flat)):
                    if flat[i] > flat[j]:
                        inversions += 1

             
            for i in range(4):
                if 0 in state[i]:
                    blank_row_from_bottom = 4 - i
                    break

            return (inversions + blank_row_from_bottom) % 2 == 0

        def generate_moves(self, state):
            moves = []
            
             
            for i in range(4):
                for j in range(4):
                    if state[i][j] == 0:
                        x, y = i, j

            directions = [(-1,0),(1,0),(0,-1),(0,1)]

            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                
                if 0 <= nx < 4 and 0 <= ny < 4:
                    new_state = [row[:] for row in state]
                    new_state[x][y], new_state[nx][ny] = new_state[nx][ny], new_state[x][y]
                    moves.append(new_state)

            return moves

        def depth_limited_search(self, state, depth, visited):
            if state == self.goal_state:
                return [state]

            if depth == 0:
                return None

            visited.add(tuple(map(tuple, state)))

            for move in self.generate_moves(state):
                if tuple(map(tuple, move)) not in visited:
                    result = self.depth_limited_search(move, depth - 1, visited)
                    if result:
                        return [state] + result

            return None

        def iddfs(self, max_depth=20):
            if not self.is_solvable(self.initial_state):
                return "Puzzle is NOT solvable"

            for depth in range(max_depth):
                visited = set()
                result = self.depth_limited_search(self.initial_state, depth, visited)
                if result:
                    return result

            return "Solution not found within depth limit"



def main():
    
    goal_state = [
        [1, 2, 3, 4],
        [5, 6, 7, 8],
        [9,10,11,12],
        [13,14,15, 0]
    ]

    #solvabe case
    initial_state_1 = [
        [1, 2, 3, 4],
        [5, 6, 7, 8],
        [9,10,11,12],
        [13,14, 0,15]
    ]

     
    puzzle1 = Puzzle(initial_state_1, goal_state)

    if puzzle1.is_solvable(initial_state_1):
        print("Puzzle is Solvable.\n")
        solution = puzzle1.iddfs()
        print("IDDFS Solution:")
        print(solution)
    else:
        print("Puzzle is NOT Solvable.")

    print("\n\n")

    #unsolvabe case
    initial_state_2 = [
        [1, 2, 3, 4],
        [5, 6, 7, 8],
        [9,10,11,12],
        [13,15,14, 0]
    ]

     
    puzzle2 = Puzzle(initial_state_2, goal_state)

    if puzzle2.is_solvable(initial_state_2):
        print("Puzzle is Solvable.\n")
        solution = puzzle2.iddfs()
        print("IDDFS Solution:")
        print(solution)
    else:
        print("Puzzle is NOT Solvable.")


if __name__ == "__main__":
    main()