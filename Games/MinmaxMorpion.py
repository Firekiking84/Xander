import time
from curses.ascii import isdigit
from logging import debug

from Games.Coords import Coords
from Games.Morpion import Morpion


def manage_encounter(slot, line, turn):
    if not isdigit(slot):
        if slot == turn:
            line["ally"] += 1
        else:
            line["ennemy"] += 1


def calcul_score(line, coefs):
    score = 0
    if line["ally"] == 0 and line["ennemy"] == 0:
        score += 1 * coefs["close"]
    if line["ennemy"] == 0:
        score += line["ally"] * coefs["end"]
    if line["ally"] == 0:
        score += line["ennemy"] * coefs["block"]
    if line["ally"] == 3:
        score += 500
    return score

def check_line(turn, board, coords, axe, coefs):
    if axe == "up" or axe == "down":
        # On vérifie que la diagonale est possible
        if (coords.x == 1 and (coords.y == 0 or coords.y == 2)) or (coords.y == 1 and (coords.x == 0 or coords.x == 2)):
            return 0
        if axe == "up" and ((coords.y == 0 and coords.x == 2) or (coords.y == 2 and coords.x == 0)):
            return 0
        if axe == "down" and ((coords.y == 0 and coords.x == 0) or (coords.y == 2 and coords.x == 2)):
            return 0
    line = {"ally": 0, "ennemy": 0}
    if axe == "x" or axe == "y" or axe == "up":
        check_range = range(3)
    else:
        check_range = range(2, -1, -1)
    for i in check_range:
        if axe == "x":
            coords.set(x=i)
        elif axe == "y":
            coords.set(y=i)
        elif axe == "up":
            coords.set(x=i, y=i)
        else:
            coords.set(x=2-i, y=i)
        manage_encounter(board[coords.i], line, turn)
    return calcul_score(line, coefs)


def get_score_from_long_range(scored_board):
    best_score = -1000
    nb_best = 0 # si plusieurs meilleurs résultats
    for slot in scored_board:
        if best_score < slot:
            best_score = best_score
            nb_best = 1
        elif best_score == slot:
            nb_best += 1
    return best_score + nb_best


def simulate_next_moves(turn, board, coords, scored_board, coefs):
    board[coords.i] = turn
    new_game = Morpion()
    if new_game.set_board(board):
        scored_board[coords.i] += 100000
        return # Coup gagnant
    turn_value = -1 # Détermine si ce sont des points gagné ou perdu. Adversaire fait perdre
    tmp_scored_board = new_scored_board()
    n_turn = 0
    turn = new_game.get_turn()
    tmp_score = 0
    while n_turn < 3 and not new_game.check_win() and turn != 'D':
        define_board_score(new_game.get_turn(), new_game.get_board(), tmp_scored_board, new_game.nb_turn)
        tmp_score += get_score_from_long_range(tmp_scored_board) * turn_value * coefs["longRange"]
        new_game.play_morpion(get_first_best_move(scored_board))
        new_game.get_turn()
        turn_value *= -1
        n_turn += 1
    if turn == 'W':
        scored_board[coords.i] += turn_value * coefs["endLongRange"]
        if turn_value == -1: # coup perdant, on y va pas
            tmp_score = 0
    scored_board[coords.i] += tmp_score


def define_slot_score(turn, board, coords, scored_board, coefs, nb_turn):
    if isdigit(board[coords.i]):
        scored_board[coords.i] += check_line(turn, board, coords.copy(), "x", coefs)
        scored_board[coords.i] += check_line(turn, board, coords.copy(), "y", coefs)
        scored_board[coords.i] += check_line(turn, board, coords.copy(), "up", coefs)
        scored_board[coords.i] += check_line(turn, board, coords.copy(), "down", coefs)
        if nb_turn > 1:
            simulate_next_moves(turn, board.copy(), coords, scored_board, coefs)
    else:
        scored_board[coords.i] = -1

def define_board_score(turn, board, scored_board, nb_turn):
    coords = Coords()
    coefs = {"close": 2, "block": 4, "end": 3, "longRange": 2, "endLongRange": 100}
    for index in range(len(board)):
        coords.set(i=index)
        define_slot_score(turn, board, coords, scored_board, coefs, nb_turn)

def new_scored_board():
    scored_board = []
    for index in range(9):
        scored_board.append(0)
    return scored_board


def get_first_best_move(scored_board):
    best_score = -1
    best_index = 0
    for index in range(len(scored_board)):
        score = scored_board[index]
        if score > best_score:
            best_score = score
            best_index = index
    return best_index


def minmax_morpion_play(game):
    turn = game.get_turn()
    board = game.get_board()
    scored_board = new_scored_board()
    nb_turn = game.nb_turn
    define_board_score(turn, board, scored_board, nb_turn)
    print(scored_board)
    if type(game.play_morpion(get_first_best_move(scored_board))) == type(True):
        return turn
    else:
        return None