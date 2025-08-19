from time import sleep
from Games.Allumettes import Allumettes
from Games.MinmaxAllumettes import minmax_allumettes_play


def player_turn(game: Allumettes, score: dict, score_for_win: int):
    turn = game.get_turn()
    end_turn = False
    while not end_turn:
        print(f"Tour de {turn}. Score actuel: X: {score['JoueurX']}, O: {score['JoueurO']}. Objectif de score {score_for_win}\n")
        game.print()
        reponse = int(input(f"Quel est ta prochaine action, {turn} ?\n --> "))
        result = game.play(reponse)
        end_turn = True
        if type(result) == type(False) and not result:
            end_turn = False


def play_allumettes(nb_player: int, start_player: str, score_for_win: int):
    game = Allumettes()
    game.init(start_player)
    score = {"JoueurX": 0, "JoueurO": 0}
    while score["JoueurX"] < score_for_win and score["JoueurO"] < score_for_win:
        game.get_game_state()
        if game.get_turn() == 'X':
            if nb_player > 0:
                player_turn(game, score, score_for_win)
            else:
                minmax_allumettes_play(game)
        if game.get_turn() == 'O' and len(game.win) == 0:
            if nb_player > 1:
                player_turn(game, score, score_for_win)
            else:
                minmax_allumettes_play(game)
        if len(game.win) > 0:
            if game.win == 'X':
                print("X marque un point !\n")
                score["JoueurX"] += 1
            else:
                print("O marque un point !\n")
                score["JoueurO"] += 1
        if nb_player == 0:
            sleep(1)
            game.print()
    if score["JoueurX"] == score_for_win:
        print(f"X a gagné le match {score['JoueurX']}:{score['JoueurO']}")
    else:
        print(f"O a gagné le match {score['JoueurO']}:{score['JoueurX']}")

play_allumettes(0, 'R', 3)