import random
from time import sleep

class Game:
    def __init__(self):
        self.board = Board()
        self.turn_number = 1
        self.players_move = random.choice([1, 2])
        self.history = []
        self.decide_what_do()

    def get_available_moves(self):
        return self.board.get_available_moves()

    def make_move(self, player, move):
        if self.board.check_col_available(move):
            self.board.place_piece(move, player)
            self.history.append([player, move])
        else:
            print("Illegal move. Try again.")

    def player_move(self):
        while True:
            try:
                move = int(input("Please enter a move: "))
                if not self.board.check_col_available(move): 
                    print("Invalid move.")
                    continue
                break
            except ValueError:
                continue

        self.make_move(1, move)
        self.turn_number+=1
        self.players_move = 2
        self.decide_what_do()
    
    def decide_what_do(self):
        winner = self.board.check_winner()
        self.board.print(True)
        if  not len(self.get_available_moves()):
            print("It's a Tie!")
            return
        if not winner:
            if self.players_move == 1:
                self.player_move()
            else:
                self.computer_move()
        else:
            if winner == 1:
                print("Congrats! You won!")
            elif winner == 2:
                print("Sorry, you lost. =(")

    def computer_move(self):
        move = self.computer_move_minimax(self.board.copy())
        self.make_move(2, move)
        self.players_move = 1
        self.decide_what_do()

    def computer_move_minimax(self, board):
        
        def minimax(board, depth, is_maximising):
            win = board.check_winner()
            if win == 2: 
                return depth
            elif win == 1: 
                return depth * -1
            elif len(board.get_available_moves()) == 0:
                return 0
            elif depth <= 0: 
                return 0
            
            available_moves = board.get_available_moves()
            if is_maximising:
                best_score = -10000
                for move in available_moves:
                    new_board = board.copy()
                    new_board.place_piece(move, 2)
                    score = minimax(new_board, depth -1, False)
                    best_score = max(score, best_score)
                return best_score
            else:
                best_score = 10000
                for move in available_moves:
                    new_board = board.copy()
                    new_board.place_piece(move, 1)
                    score = minimax(new_board, depth -1, True)
                    best_score = min(score, best_score)
                return best_score

        available_moves = board.get_available_moves()
        def get_score(move):
            new_board = board.copy()
            new_board.place_piece(move, 2)
            return dict(move= move, score=minimax(new_board, 5, False))

        move_scores = list(map(get_score, available_moves))
        max_score = max(move_scores, key=lambda x: x['score'])
        best_move_scores = [move for move in move_scores if move['score'] == max_score['score']]
        random_move = random.choice(best_move_scores)
        return random_move['move']



class Board:
    def __init__(self):
        self.board = self.create_board(6,7)

    def create_board(self, rows, columns):
        self.rows = rows
        self.columns = columns
        return [[0 for j in range(columns)] for i in range(rows)]

    def copy(self):
        new_board = Board()
        for i in range(self.rows):
            for j in range(self.columns):
                new_board.board[i][j] = self.board[i][j]
        return new_board

    def check_col_available(self, col):
        if col >= self.columns: return False
        return self.board[self.rows-1][col] == 0

    def place_piece(self, col, player):
        if(self.check_col_available(col)):
            for i in range(self.rows):
                if(self.board[i][col] == 0):
                    self.board[i][col] = player
                    self.last_move = col
                    break
        else:
            print("Illegal move")


    def print(self, header = False):
        print(self.to_string(header))

    def print_dirty(self):
        print(self.board)

    def to_string(self, header):
        board_string = ""
        if header: 
            for i in range(self.columns):
                board_string+= str(i) + " "
            board_string += "\n"
            
        for i in range(self.rows -1, -1, -1):
            for j in range(0, self.columns):
                
                if(self.board[i][j] == 1):
                    board_string += "X "
                elif(self.board[i][j] == 2):
                    board_string += "O "
                else:
                    board_string += ". "
            board_string += "\n"

        return board_string

    def check_winner(self):
        return self.check_winner_cols() or self.check_winner_rows() or self.check_winner_diags() or self.check_winner_otherdiags()

    def check_winner_rows(self):
        for i in range(self.rows):
            last = 0
            count = 1
            for j in range(self.columns):
                if last == self.board[i][j] and last != 0:
                    count+=1
                    if count == 4: return last
                else: count = 1
                last = self.board[i][j]
        return False

    def check_winner_cols(self):
        for j in range(self.columns):
            last = 0
            count = 1
            for i in range(self.rows):
                if last == self.board[i][j] and last != 0:
                    count+=1
                    if count == 4: return last
                else: count = 1
                last = self.board[i][j]
        return False

    def check_winner_diags(self):
        for i in range(self.rows):
            last = 0
            count = 1
            current_row = i
            current_col = 0
            while current_row >= 0 and current_col < self.columns:
                if last == self.board[current_row][current_col] and last != 0:
                    count+=1
                    if count == 4: return last
                else: count = 1
                last = self.board[current_row][current_col]
                current_row-=1
                current_col+=1
        for j in range(1, self.columns):
            last = 0
            count = 1
            current_row = self.rows - 1
            current_col = j
            while current_row >= 0 and current_col < self.columns:
                if last == self.board[current_row][current_col] and last != 0:
                    count+=1
                    if count == 4: return last
                else: count = 1
                last = self.board[current_row][current_col]
                current_row-=1
                current_col+=1
        return False



    def check_winner_otherdiags(self):
        for i in range(self.rows):
            last = 0
            count = 1
            current_row = i
            current_col = self.columns -1
            while current_row >= 0 and current_col >= 0:
                if last == self.board[current_row][current_col] and last != 0:
                    count+=1
                    if count == 4: return last
                else: count = 1
                last = self.board[current_row][current_col]
                current_row-=1
                current_col-=1
        for j in range(self.columns -2, -1, -1):
            last = 0
            count = 1
            current_row = self.rows - 1
            current_col = j
            while current_row >= 0 and current_col >= 0:
                if last == self.board[current_row][current_col] and last != 0:
                    count+=1
                    if count == 4: return last
                else: count = 1
                last = self.board[current_row][current_col]
                current_row-=1
                current_col-=1
        return False

    def get_available_moves(self):
        moves = []
        for col in range(self.columns):
            if self.check_col_available(col): moves.append(col)
        return moves


Game()