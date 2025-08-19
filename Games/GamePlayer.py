from Games.MinmaxAllumettes import minmax_allumettes_play
from Games.MinmaxMorpion import minmax_morpion_play
from Games.Morpion import Morpion
from Games.Allumettes import Allumettes


def player_turn(game: Allumettes, score: dict, score_for_win: int):
    turn = game.get_turn()
    end_turn = False
    while not end_turn:
        print(f"Tour de {turn}. Score actuel: X: {score['X']}, O: {score['O']}, égalité: {score['D']}. Objectif de score {score_for_win}\n")
        game.print()
        reponse = int(input(f"Quel est ta prochaine action, {turn} ?\n --> "))
        result = game.play(reponse)
        end_turn = True
        if type(result) == type(False) and not result:
            end_turn = False


def duo_game_player(game: Morpion | Allumettes, score_for_win: int,  players: dict, minmax=None, xander=None,):
    game.init()
    score = {"X": 0, "O": 0, "D": 0}
    while score["X"] < score_for_win and score["O"] < score_for_win and score["D"] < (score_for_win * 3):
        game.get_game_state()
        if minmax is not None and players[game.get_turn()] == 'Minmax':
            minmax(game)
        elif xander is not None and players[game.get_turn()] == 'Xander':
            xander(game)
        else:
            player_turn(game, score, score_for_win)
        if len(game.win) > 0:
            print(f"{game.win} marque un point !\n")
            score[game.win] += 1
            print(f"Score actuel: X: {score['X']}, O: {score['O']}, égalité: {score['D']}. Objectif de score {score_for_win}")


duo_game_player(Allumettes(), 3, {'X': 'Minmax', 'O': 'Minmax', 'Start': 'R'}, minmax_allumettes_play)
duo_game_player(Morpion(), 3, {'X': 'Minmax', 'O': 'Minmax', 'Start': 'R'}, minmax_morpion_play)
