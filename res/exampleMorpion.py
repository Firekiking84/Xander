# include
from Games.Morpion import Morpion

# init
game = Morpion()  # game
board = game.init_board()  # array 9

# back
board = game.back()  # array 9

# player X
board = game.get_board()  # array 9
board = game.play_morpion(4)  # array 9

# player O
board = game.get_board()  # array 9
board = game.play_morpion(5)  # array 9

# player X
board = game.get_board()  # array 9
board = game.play_morpion(1)  # array 9

# player O
board = game.get_board()  # array 9
board = game.play_morpion(2)  # array 9

# player X
board = game.get_board()  # array 9
board = game.play_morpion(7)  # bool 1

# end player X
