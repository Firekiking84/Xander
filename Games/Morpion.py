from curses.ascii import isdigit

from Games.Coords import Coords
from Games.mainMorpion import board


class Morpion:
    def __init__(self):
        self.player = "X"
        self.board = []
        self.previous_board = []


    @staticmethod
    def manage_encounter(slot, line):
        if isdigit(slot):
            return
        if slot == 'X':
            line["ally"] += 1
        else:
            line["ennemy"] += 1


    @staticmethod
    def check_straight_lines_win(self, board, axe):
        line = {"ally": 0, "ennemy": 0}
        coords = Coords()
        for y in range(3):
            for x in range(3):
                if axe == "x":
                    coords.set(x=x, y=y)
                else:
                    coords.set(x=y, y=x)
                self.manage_encounter(board[coords.i], line)
            if line["ally"] == 3 or line["ennemy"] == 3:
                return True
            line["ally"] = 0
            line["ennemy"] = 0
        return False


    @staticmethod
    def check_diagonal_lines_win(self, board, axe):
        line = {"ally": 0, "ennemy": 0}
        coords = Coords()
        if axe == "up":
            check_range = range(3)
        else:
            check_range = range(2, -1, -1)
        for i in check_range:
            coords.set(x=i, y=i)
            self.manage_encounter(board[coords.i], line)
        if line["ally"] == 3 or line["ennemy"] == 3:
            return True
        return False


    def check_win(self):
        if self.check_straight_lines_win(self, self.board, "x"):
            return True
        if self.check_straight_lines_win(self, self.board, "y"):
            return True
        if self.check_diagonal_lines_win(self, self.board, "up"):
            return True
        if self.check_diagonal_lines_win(self, self.board, "down"):
            return True
        return False


    def print_board(self):
        print(f"Plateau :\n")
        for y in range(3):
            for x in range(3):
                print(f"[{self.board[y * 3 + x]}] ", end="")
            print("\n")

    def get_turn(self):
        return self.player

    def get_board(self):
        if self.player == 'W' or self.player == 'D':
            self.init_board()
        return self.board

    def init_board(self):
        self.board = []
        self.previous_board = []
        for i in range(9):
            self.board.append(f"{i}")
        self.previous_board.append(self.board.copy())
        return self.board


    @staticmethod
    def check_draw(gameboard):
        for slot in gameboard:
            if isdigit(slot):
                return False
        return True


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
        if self.check_draw(board):
            self.player = 'D'
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
