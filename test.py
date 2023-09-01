from set import *

deck = create_deck()
board, deck = create_board(deck)
sets = find_sets(board)
print(sets)
print(type(sets))
print(type(sets[0]))
print(type(sets[0][0]))
for i, j in sets[0]:
    print(card_to_string(board[i][j]))
