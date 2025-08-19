import random

from Games.Coords import Coords

class Jumper:
    def __init__(self):
        self.ticks = 0
        self.board = []
        self.previous_boards = []
        self.obstacles = set()
        self.last_obstacle = 0
        self.board_size = Coords(x=40, y=5)
        self.player_pos = Coords(width=40)
        self.player_pos.set(x=1, y=4)
        self.player_ascending = False
        self.game_over = False

    def init(self):
        self.ticks = 0
        self.board.clear()
        self.previous_boards.clear()
        self.obstacles = set()
        self.last_obstacle = 0
        self.player_pos.set(x=1, y=4)
        self.player_ascending = False
        self.game_over = False
        for y in range(5):
            content = " "
            if y == 4:
                content = "-"
            for x in range(40):
                self.board.append(content)

    def play(self, do_jump=False):
        self.ticks += 1
        # Manage input
        if do_jump and self.player_pos.y == 4:
            self.player_ascending = True

        # Go next tick

        # Manage player
        if self.player_ascending:
            self.player_pos.set(y=self.player_pos.y - 1)
            if self.player_pos.y == 0:
                self.player_ascending = False
        elif self.player_pos.y != 4:
            self.player_pos.set(y=self.player_pos.y + 1)

        # Update board
        self.shift_left_board()

        # Draw the board
        print_board = self.board.copy()

        #   Draw obstacles and manage player hits
        for obstacle in self.obstacles:
            obstacle.draw(print_board, self.board_size.x, 4)
            if self.player_pos.y == 4 and obstacle.position <= self.player_pos.x <= (obstacle.position + obstacle.length):
                self.game_over = True
                return False

        #   Draw Player
        print_board[self.player_pos.i] = '*'

        #   Print
        print(f"Distance: {self.ticks}")
        i = 0
        for y in range(5):
            for x in range(40):
                print(print_board[i], end='')
                i += 1
            print("\n", end='')

        return print_board


    def shift_left_board(self):
        self.previous_boards.append(self.board)
        if (self.ticks - self.last_obstacle) > 10:
            if random.randint(1, 5) == 1:
                self.last_obstacle = self.ticks
                self.obstacles.add(Obstacle(self.ticks, self.board_size.x, random.randint(1, 3)))
        for obstacle in self.obstacles.copy():
            if obstacle.shift_left_board() is False:
                self.obstacles.discard(obstacle)


    def back(self):
        if len(self.previous_boards):
            self.board = self.previous_boards.pop()
            self.game_over = False
        return self.board.copy()

    def get_board(self):
        return self.board.copy()

class Obstacle:
    def __init__(self, creation_date, board_length, length):
        self.creation_date = creation_date
        self.length = length
        self.position = board_length - 1

    def __hash__(self):
        return hash(self.creation_date)

    def __eq__(self, other):
        return self.creation_date == other.creation_date

    def draw(self, board, width, floor=4):
        coords = Coords(width=width)
        coords.set(x=self.position, y=floor)
        for i in range(self.length):
            if 40 > coords.x + i >= 0:
                board[coords.i + i] = 'T'

    def shift_left_board(self):
        self.position -= 1
        if (self.position + self.length) < 0:
            return False
        return True