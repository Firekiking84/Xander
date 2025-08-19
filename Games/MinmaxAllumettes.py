from Games.Allumettes import Allumettes


def define_choice_score(nb_allumettes, scored_choice: dict, turn: str):
    tier_part = (nb_allumettes - 1) % 3
    if tier_part == 0:
        if ((nb_allumettes - 1) % 2) == 1:
            scored_choice[3] = 1
        else:
            scored_choice[2] = 1
    else:
        scored_choice[1] = 1


def get_best_choice(scored_choice: dict):
    best_score = -1
    best_index = 0
    index = 0
    for score in scored_choice.values():
        if score > best_score:
            best_score = score
            best_index = index
        index += 1
    return best_index + 1

def minmax_allumettes_play(game: Allumettes):
    turn = game.get_turn()
    nb_allumettes = game.get_game_state()
    scored_choice = {1: 0, 2: 0, 3: 0}
    define_choice_score(nb_allumettes, scored_choice, turn)
    game.play(get_best_choice(scored_choice))
    print(f"Minmax {turn} a joué {get_best_choice(scored_choice)}")