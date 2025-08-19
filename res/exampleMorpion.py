# include
from Games.Morpion import Morpion

# init
game = Morpion()  # game
board = game.init()  # array 9

# back
board = game.back()  # array 9

# player X
board = game.get_game_state()  # array 9
board = game.play(4)  # array 9

# player O
board = game.get_game_state()  # array 9
board = game.play(5)  # array 9

# player X
board = game.get_game_state()  # array 9
board = game.play(1)  # array 9

# player O
board = game.get_game_state()  # array 9
board = game.play(2)  # array 9

# player X
board = game.get_game_state()  # array 9
board = game.play(7)  # bool 1

# end player X
