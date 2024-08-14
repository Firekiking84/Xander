from Games.Morpion import play_morpion, print_board, init_board

board = init_board()
end = False

while not end:
    endTurn = False
    while not endTurn:
        print_board(board)
        reponse = int(input("Quel est ta prochaine action, X ?\n--> "))
        result = play_morpion(reponse)
        if type(result) == type(False):
            if result:
                print("X a gagné la partie !")
                endTurn = True
                end = True
        else:
            endTurn = True
    endTurn = False
    while not endTurn and not end:
        print_board(board)
        reponse = int(input("Quel est ta prochaine action, O ?\n--> "))
        result = play_morpion(reponse)
        if type(result) == type(False):
            if result:
                print("Y a gagné la partie !")
                end = True
        else:
            endTurn = True
