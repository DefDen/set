import random
import numpy as np
from itertools import chain

attributes=['multiplicity', 'texture', 'color', 'shape']

# get rand deck
def create_deck(size=81, shuffle=True):
    deck = [{} for _ in range(size)]
    for i in range(size):
        card = {}
        # multiplicity
        card[attributes[0]] = i % 3
        # texture
        x = (int(i / 3)) % 3
        if x == 0:
            card[attributes[1]] = 'hollow'
        elif x == 1:
            card[attributes[1]] = 'striped'
        else:
            card[attributes[1]] = 'solid'
        # color
        x = (int(i / 9)) % 3
        if x == 0:
            card[attributes[2]] = 'red'
        elif x == 1:
            card[attributes[2]] = 'green'
        else:
            card[attributes[2]] = 'purple'
        # shape
        x = (int(i / 27)) % 3
        if x == 0:
            card[attributes[3]] = 'squiggle'
        elif x == 1:
            card[attributes[3]] = 'pill'
        else:
            card[attributes[3]] = 'diamond'
        deck[i] = card
    # shuffling
    if shuffle:
        random.shuffle(deck)
    return deck

def draw_card(deck, n=1):
    return deck[:n], deck[n:]

def create_board(deck):
    c, deck = draw_card(deck, n=12)
    return np.reshape(c, (4, 3)), deck

# takes set s and returns true if s constitutes a valid set, false otherwise
# raises TypeError if len(s) != 3
def is_set(s):
    if len(s) != 3:
        raise TypeError('Set must contain exactly 3 elements, input was ' + str(len(s)) + ' elements long')
    for attribute in attributes:
    a, b, c = s[0][attribute], s[1][attribute], s[2][attribute]
        if not ((a == b == c) or (a != b and a != c and b != c)):
            return False
    return True

def find_sets(board):
    spread = list(chain.from_iterable(board))
    spread_sets = _find_sets(spread)
    index_converter = _spread_index_to_board_index(board)
    board_indices = map(index_converter, [s[0] for s in spread_sets])
    return zip(board_indices, [s[1] for s in spread_sets])

def _find_sets(spread, current_set=[]):
    if len(current_set) == 3:
        if is_set([s[1] for s in current_set]):
            return [[s[0] for s in current_set]]
        return []
    if not spread:
        return []
    r = []
    for i in range(len(spread)):
        indices = [a[0] for a in current_set]
        indices.append(i)
        cards, remaining_spread = draw_card(spread, n=(i+1))
        if not current_set:
            current_set.append((i, cards[-1]))
        else:
            current_set.append(([s[0] for s in current_set][-1] + i + 1, cards[-1]))
        s = _find_sets(remaining_spread, current_set, solved)
        current_set.pop()
        r += s
    return r

def _spread_index_to_board_index(board, vertical_flip=False):
    if vertical_flip:
        return lambda spread_index : board_index.append((math.abs((int)(spread_index / len(board[0])) - len(board)), spread_index % len(board[0])))
    return lambda spread_index : board_index.append(((int)(spread_index / len(board[0])), spread_index % len(board[0])))

deck = create_deck()
board, deck = create_board(deck)
sets = find_sets(board)
print(sets)
print(len(sets))
