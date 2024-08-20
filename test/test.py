from Games.Coords import Coords

board = [0, 1, 2, 3, 4, 5, 6, 7, 8]

coords = Coords()
for i in range(9):
    coords.set(i=i)
    print(coords)


for y in range(3):
    for x in range(3):
        coords.set(x=x, y=y)
        print(coords)
