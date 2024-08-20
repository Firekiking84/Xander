from curses.ascii import isdigit
from Games.Coords import Coords


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
    return score

def check_line(turn, board, coords, axe, coefs):
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
        else:
            coords.set(x=i, y=i)
        manage_encounter(board[coords.i], line, turn)
    return calcul_score(line, coefs)


def define_slot_score(turn, board, coords, scored_board, coefs):
    if isdigit(board[coords.i]):
        scored_board[coords.i] += check_line(turn, board, coords.copy(), "x", coefs)
        scored_board[coords.i] += check_line(turn, board, coords.copy(), "y", coefs)
        scored_board[coords.i] += check_line(turn, board, coords.copy(), "up", coefs)
        scored_board[coords.i] += check_line(turn, board, coords.copy(), "down", coefs)
    else:
        scored_board[coords.i] = -1

def define_board_score(turn, board, scored_board):
    coords = Coords()
    coefs = {"close": 3, "block": 2, "end": 3}
    for index in range(len(board)):
        coords.set(i=index)
        define_slot_score(turn, board, coords, scored_board, coefs)

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
    define_board_score(turn, board, scored_board)
    print(scored_board)
    if not game.play_morpion(get_first_best_move(scored_board)):
        print("MinMax s'est trompé")