class Morpion:
    def __init__(self):
        self.player = "X"
        self.board = []
        self.previous_board = []

    def check_win(self):
        row = True
        i = 0
        x = 0
        while x < 3:
            y = 0
            while y < 3 and row:
                if self.board[i] != self.player:
                    row = False
                i += 1
                y += 1
            if row:
                return True
            row = True
            x += 1
        column = True
        x = 0
        while x < 3:
            i = x
            y = 0
            while y < 3 and column:
                if self.board[i] != self.player:
                    column = False
                y += 1
                i += 3
            if column:
                return True
            column = True
            x += 1
        if self.board[4] == self.player:
            if self.board[0] == self.player and self.board[8] == self.player:
                return True
            if self.board[2] == self.player and self.board[6] == self.player:
                return True
        return False

    def print_board(self):
        print(f"Plateau :\n")
        for y in range(3):
            for x in range(3):
                print(f"[{self.board[y * 3 + x]}] ", end="")
            print("\n")

    def get_board(self):
        return self.board

    def init_board(self):
        self.board = []
        self.previous_board = []
        for i in range(9):
            self.board.append(f"{i}")
        self.previous_board.append(self.board.copy())
        return self.board

    def play_morpion(self, move):
        if move < 0 or move > len(self.board):
            return False
        if '0' <= self.board[move] <= '9':
            self.previous_board.append(self.board.copy())
            self.board[move] = self.player
        else:
            return False
        if self.check_win():
            self.player = 'W'
            return True
        if self.player == 'X':
            self.player = 'O'
        else:
            self.player = 'X'
        return self.board

    def back(self):
        if len(self.previous_board) > 0:
            self.board = self.previous_board.pop()
        else:
            self.board = []
        return self.board
