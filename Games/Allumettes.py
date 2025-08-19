import time


class Allumettes:
    def __init__(self):
        self.nb_turn = 0
        self.win = ''
        self.player = 'X'
        self.start_nb_allumettes = 50
        self.nb_allumettes = self.start_nb_allumettes
        self.past = []
        self.start_player = 'X'

    # Init functions
    def set_max_nb_allumettes(self, allumettes):
        self.start_nb_allumettes = allumettes


    def init(self, start_player='R'): # Pattern Name
        self.nb_allumettes = self.start_nb_allumettes
        self.past.clear()
        self.win = ''
        if start_player == 'R':
            if (int(time.time()) % 2) == 0:
               self.player = 'X'
            else:
                self.player = 'O'
        else:
            self.player = start_player

    # Play Functions
    def play(self, quantity): # Pattern Name
        if quantity < 1 or quantity > 3:
            return False
        self.past.append(self.nb_allumettes)
        self.nb_allumettes -= quantity
        self.check_win()
        if len(self.win) > 0:
            return True
        self.next_player()
        return self.nb_allumettes


    def get_turn(self): # Pattern Name
        return self.player


    def get_game_state(self): # Pattern Name
        if len(self.win):
            self.init(self.start_player)
        return self.nb_allumettes


    def print(self): # Pattern Name
        for level in range(2):
            for i in range(self.nb_allumettes):
                if level == 0:
                    print('. ', end="")
                else:
                    print('| ', end="")
            print('\n', end="")

    # Admin Functions
    def set_game_state(self, allumettes, player):
        self.nb_allumettes = allumettes
        self.player = player
        self.check_win()
        self.next_player()


    def back(self): # Pattern Name
        if len(self.past) > 0:
            self.nb_allumettes = self.past.pop()
        else:
            self.nb_allumettes = 0

    # Game inside tools
    def next_player(self):
        if self.player == 'X':
            self.player = 'O'
        else:
            self.player = 'X'


    def check_win(self):
        if self.nb_allumettes == 1:
            self.win = self.player
        elif self.nb_allumettes < 1:
            self.next_player()
            self.win = self.player