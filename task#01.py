import time
import copy

# Required helper function for win conditions [ 
def check_winner(board, player):
    win_conditions = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8), # Rows  
        (0, 3, 6), (1, 4, 7), (2, 5, 8), # Cols  
        (0, 4, 8), (2, 4, 6)             # Diagonals  
    ]
    return any(all(board[pos] == player for pos in condition) for condition in win_conditions) 

class Minimax:
    def __init__(self, board, max_depth=9):
        self.board = board
        self.max_depth = max_depth
        self.nodes_expanded = 0  
    def is_terminal(self, state):
        # Check if the game has reached a terminal state (win, lose, draw)  
        return check_winner(state, 'X') or check_winner(state, 'O') or ' ' not in state

    def utility(self, state):
        # AI is 'O' (Maximizer), Human is 'X' (Minimizer)  
        if check_winner(state, 'O'): return 1
        if check_winner(state, 'X'): return -1
        return 0

    def heuristic(self, state):
        # Simple heuristic for evaluating non-terminal states  
        return 0 

    def minimax(self, state, depth, maximizing_player):
        self.nodes_expanded += 1 # Track number of explored nodes 
        
        # Terminal states are evaluated using utility; non-terminal using heuristic 
        if self.is_terminal(state):
            return self.utility(state)
        if depth == 0:
            return self.heuristic(state)

        if maximizing_player:
            max_eval = float('-inf')
            for i in range(9):
                if state[i] == ' ':
                    state[i] = 'O'
                    eval = self.minimax(state, depth - 1, False)
                    state[i] = ' '
                    max_eval = max(max_eval, eval)
            return max_eval
        else:
            min_eval = float('inf')
            for i in range(9):
                if state[i] == ' ':
                    state[i] = 'X'
                    eval = self.minimax(state, depth - 1, True)
                    state[i] = ' '
                    min_eval = min(min_eval, eval)
            return min_eval

    def best_move(self, state):
        # Determine the best move using Minimax  
        start_time = time.time()
        self.nodes_expanded = 0 # Reset for current move search
        best_val = float('-inf')
        move = -1
        
        for i in range(9):
            if state[i] == ' ':
                state[i] = 'O'
                move_val = self.minimax(state, self.max_depth - 1, False)
                state[i] = ' '
                if move_val > best_val:
                    best_val = move_val
                    move = i
        
        end_time = time.time()
        duration = end_time - start_time
        return move, self.nodes_expanded, duration # Record nodes and time [cite: 67, 68]

def test_cases():
    # Initial board state for testing  
    test_board = ['X', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
    depths = [9, 4, 2]  
    
    print(f"{'Depth':<10} | {'Best Move':<10} | {'Nodes Expanded':<15} | {'Time (s)':<10}")
    print("-" * 55)
    
    for d in depths:
        ai = Minimax(test_board, max_depth=d)
        
        move, nodes, taken = ai.best_move(copy.deepcopy(test_board))
        print(f"{d:<10} | {move:<10} | {nodes:<15} | {taken:<10.5f}")

if __name__ == "__main__":
    test_cases()