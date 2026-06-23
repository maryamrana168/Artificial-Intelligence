import time
import copy

def check_winner(board, player):
    win_conditions = [(0,1,2), (3,4,5), (6,7,8), (0,3,6), (1,4,7), (2,5,8), (0,4,8), (2,4,6)]  
    return any(all(board[pos] == player for pos in condition) for condition in win_conditions)  

class AlphaBetaPruning:
    def __init__(self, board, depth=9):
        self.max_depth = depth  
        self.nodes_expanded = 0 

    def alphabeta(self, state, depth, alpha, beta, maximizing_player):
        self.nodes_expanded += 1  
        
        # Terminal check [cite: 114, 115]
        if check_winner(state, 'O'): return 1
        if check_winner(state, 'X'): return -1
        if ' ' not in state or depth == 0: return 0

        if maximizing_player:
            v = float('-inf')
            for i in range(9):
                if state[i] == ' ':
                    state[i] = 'O'
                    v = max(v, self.alphabeta(state, depth - 1, alpha, beta, False))
                    state[i] = ' '
                    alpha = max(alpha, v)  
                    if beta <= alpha: break # PRUNE [cite: 101, 102]
            return v
        else:
            v = float('inf')
            for i in range(9):
                if state[i] == ' ':
                    state[i] = 'X'
                    v = min(v, self.alphabeta(state, depth - 1, alpha, beta, True))
                    state[i] = ' '
                    beta = min(beta, v)  
                    if beta <= alpha: break # PRUNE [cite: 101, 102]
            return v

    def best_move(self, state):
        start_time = time.time()
        self.nodes_expanded = 0
        best_v = float('-inf')
        move = -1
        for i in range(9):
            if state[i] == ' ':
                state[i] = 'O'
                # Initialize alpha as -infinity and beta as +infinity [cite: 5, 121]
                val = self.alphabeta(state, self.max_depth - 1, float('-inf'), float('inf'), False)
                state[i] = ' '
                if val > best_v:
                    best_v = val
                    move = i
        duration = time.time() - start_time
        return move, self.nodes_expanded, duration

def run_cases():
    test_board = ['X', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
    depths = [9, 4, 2]
    
    print("TASK 02: Alpha-Beta Pruning Performance Test")
    print(f"{'Depth':<10} | {'Move':<6} | {'Nodes Expanded':<15} | {'Time (s)':<10}")
    print("-" * 55)
    
    for d in depths:
        ab = AlphaBetaPruning(test_board, depth=d)
        move, nodes, taken = ab.best_move(copy.deepcopy(test_board))
        print(f"{d:<10} | {move:<6} | {nodes:<15} | {taken:<10.5f}")

if __name__ == "__main__":
    run_cases()
    