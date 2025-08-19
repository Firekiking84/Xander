from time import sleep
from Games.MinmaxMorpion import minmax_morpion_play
from Games.Morpion import Morpion

game = Morpion()
board = game.init('R')
end = False
Score = {"Joueur": 0, "MinMax": 0, "Draw": 0}

while not end:
    if game.win == 'D':
        Score["Draw"] += 1
        print("Egalité !")
    board = game.get_game_state()
    if game.get_turn() == 'X':
        endTurn = False
        while not endTurn:
            print(f"\nVotre Score : {Score['Joueur']}, Score MinMax : {Score['MinMax']}, Egalité : {Score['Draw']}")
            game.print()
            reponse = int(input(f"Quel est ta prochaine action, {game.get_turn()} ?\n--> "))
            if reponse == -1:
                end = True
                endTurn = True
            else:
                result = game.play(reponse)
                if type(result) == type(False) and game.win == 'X':
                    if result:
                        Score["Joueur"] += 1
                        print("Vous avez gagné la partie !")
                        sleep(5)
                        endTurn = True
                else:
                    endTurn = True
    if not end and game.get_turn() == 'O':
        if minmax_morpion_play(game) == 'O' and game.win == 'O':
            Score["MinMax"] += 1
            print("MinMax a gagné la partie !!")