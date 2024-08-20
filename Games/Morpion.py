import time
from curses.ascii import isdigit

from Games.Coords import Coords


class Morpion:
    def __init__(self):
        self.nb_turn = 0
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
    def check_straight_lines_win(self, gameboard, axe):
        line = {"ally": 0, "ennemy": 0}
        coords = Coords()
        for y in range(3):
            for x in range(3):
                if axe == "x":
                    coords.set(x=x, y=y)
                else:
                    coords.set(x=y, y=x)
                self.manage_encounter(gameboard[coords.i], line)
            if line["ally"] == 3 or line["ennemy"] == 3:
                return True
            line["ally"] = 0
            line["ennemy"] = 0
        return False


    @staticmethod
    def check_diagonal_lines_win(self, gameboard, axe):
        line = {"ally": 0, "ennemy": 0}
        coords = Coords()
        if axe == "up":
            check_range = range(3)
        else:
            check_range = range(2, -1, -1)
        for i in check_range:
            if axe == "down":
                coords.set(x=2 - i, y=i)
            else:
                coords.set(x=i, y=i)
            self.manage_encounter(gameboard[coords.i], line)
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
            self.init_game()
        return self.board.copy()

    def set_board(self, new_board):
        self.board = new_board.copy()
        nb_X = 0
        nb_O = 0
        for slot in self.board:
            if slot == 'X':
                nb_X += 1
            elif slot == 'O':
                nb_O += 1
        if nb_O < nb_X:
            self.player = 'O'
        else:
            self.player = 'X'
        self.nb_turn = nb_X + nb_O
        return self.check_win()

    def init_game(self):
        self.board = []
        self.previous_board = []
        self.nb_turn = 0
        for i in range(9):
            self.board.append(f"{i}")
        self.previous_board.append(self.board.copy())
        if (int(time.time()) % 2) == 0:
            self.player = 'X'
        else:
            self.player = 'O'
        return self.board.copy()


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
        if self.check_draw(self.board):
            self.player = 'D'
            return True
        if self.player == 'X':
            self.player = 'O'
        else:
            self.player = 'X'
        self.nb_turn += 1
        return self.board

    def back(self):
        if len(self.previous_board) > 0:
            self.board = self.previous_board.pop()
        else:
            self.board = []
        return self.board
