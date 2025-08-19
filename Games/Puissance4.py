import time
from mimetypes import inited
from os import times

from Games.Coords import Coords


class Puissance4:
    def __init__(self):
        self.nb_turn = 0
        self.player = 'X'
        self.win = ''
        self.board = []
        self.past = []
        self.start_player = 'X'
        self.width = 7
        self.height = 6

    # Init functions
    def init(self, start_player:str ='R'):
        self.start_player = start_player
        self.reset_var()

    # Play functions
    def set_token(self, coords: Coords):
        for y in range(self.height):
            coords.set(y=y)
            if self.board[coords.i] == ' ':
                self.past.append(self.board.copy())
                self.board[coords.i] = self.player
                self.nb_turn += 1
                return


    def play(self, column):
        coords = Coords(x=column, y=5)
        if column < 0 or column >= self.width or self.board[coords.i] != ' ':
            return False
        self.set_token(coords)

    # Inside tools functions
    def check_horizontal_win(self, coords: Coords, test_win_target: str):
        total_token = 1 # 1 Parceque on est déjà sur une case
        test_coords = Coords(x=coords.x - 1, y=coords.y)
        while test_coords.x > 0 and total_token < 4 and self.board[test_coords.i] == test_win_target:
            total_token += 1
        while test_coords.x < self.width and total_token < 4 and self.board[test_coords.i] == test_win_target:
            total_token += 1
        if total_token == 4:
            return True
        return False


    def check_win_slot(self, index: int):
        coords = Coords(i=index)
        test_win_target = self.board[coords.i]
        if test_win_target == ' ':
            return False
        self.check_horizontal_win(coords, test_win_target)


    def check_win(self):
        for i in range(self.width * self.height):
            if self.check_win_slot(i):
                return True


    def next_player(self):
        if self.player == 'X':
            self.player = 'O'
        else:
            self.player = 'X'


    def reset_player(self):
        if self.start_player == 'R':
            if (int(time.time()) % 2) == 0:
                self.player = 'X'
            else:
                self.player = 'O'
        else:
            self.player = self.start_player


    def reset_board(self):
        self.board.clear()
        for i in range(self.width * self.height):
            self.board.append(' ')


    def reset_var(self):
        self.nb_turn = 0
        self.reset_player()
        self.win = ''
        self.reset_board()
        self.past.clear()
