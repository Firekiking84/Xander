from Games.MinmaxMorpion import minmax_morpion_play
from Games.Morpion import Morpion

game = Morpion()
board = game.init_board()
end = False

while game.player != 'W':
    endTurn = False
    while not endTurn:
        game.print_board()
        reponse = int(input(f"Quel est ta prochaine action, {game.get_turn()} ?\n--> "))
        result = game.play_morpion(reponse)
        if type(result) == type(False):
            if result:
                print("X a gagné la partie !")
                endTurn = True
                end = True
        else:
            endTurn = True
    print("Minmax joue...")
    minmax_morpion_play(game)
