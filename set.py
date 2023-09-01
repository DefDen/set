import random
import numpy as np
from itertools import chain

attributes = ['multiplicity', 'texture', 'color', 'shape']

def create_deck(size=81, shuffle=True):
    """
    Creates a deck of cards.

    Creates a list of cards. Each card is represented by a dictionary mapping attributes to values.

    Params:
    size (int, optional): The number of cards in the deck.
                          Defaults to 81.
    shuffle (bool, optional): If True, shuffle the deck.
                              If False, do not shuffle the deck.
                              Defaults to True.

    Returns:
    list of dict: A list of dictionaries each representing a card.
    """
    deck = [{} for _ in range(size)]
    for i in range(size):
        card = {}
        # multiplicity
        card[attributes[0]] = i % 3 + 1
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

def card_to_string(card):
    """
    Produces a string representation of a card.

    Produces a string representation of a card.

    Parameters:
    card (dict): The card to convert to a string.

    Returns:
    (string): The string representation of the card.
    """
    r = ''
    for a in attributes:
        r += str(card[a]) + ' '
    r = r.strip()
    if card['multiplicity'] == 1:
        return r
    return r + 's'

def draw_card(deck, n=1):
    """
    Draws cards from a deck.

    Draws n cards from a deck and returns both the drawn cards and the remaining deck. Does not
    mutate the deck.

    Parameters:
    deck (list of dict): The deck of cards that will be drawn from.
    n (int, optional): The number of cards to draw.
                       Defaults to 1.

    Returns:
    (list of dict, list of dict): A tuple of the drawn cards and the remaining deck.
    """
    return deck[:n], deck[n:]

def create_board(deck):
    """
    Creates a board.

    Draws cards from a deck to create a board guaranteed to contain a set. If no set occurs in the 
    first 12 cards drawn it will continue to draw until there is one. The board returned will be
    either a (4, 3), (5, 3) or (6, 3) matrix. Does not mutate the deck. Raises a ValueError if the
    deck is not large enough to create a board.

    Parameters:
    deck (list of dict): The deck of cards that will be drawn from to make the board.

    Returns:
    (list of list of dict, list of dict): A tuple of the matrix representing the board of cards and
                                          the remaining deck.

    Raises:
    ValueError: If the deck is not large enough to create a board.
    """
    cards, deck = draw_card(deck, n=12)
    return np.reshape(cards, (4, 3)), deck

def is_set(s):
    """
    Checks whether a group of 3 cards constitutes a set.

    Checks whether a group of 3 cards constitutes a set. A set is defined as for each attribute of 
    the cards they must all have the same or different value. Raises a ValueError if not exactly 3
    cards are given as parameter.

    Parameters:
    s (list of dict): A porposed set of cards.

    Returns:
    (bool): If s is a set, True.
            If s is not a set, False.

    Raises:
    ValueError: If exactly 3 cards are not given as parameter.
    """
    if len(s) != 3:
        raise TypeError('Set must contain exactly 3 elements, input was ' + str(len(s)) + \
                        ' elements long')
    for attribute in attributes:
        a, b, c = s[0][attribute], s[1][attribute], s[2][attribute]
        if not ((a == b == c) or (a != b and a != c and b != c)):
            return False
    return True

def find_sets(board):
    """
    Finds all sets present in a board.

    Finds all sets present in a board and returns the index of each card in each set as well as
    the card themselves.

    Parameters:
    board (list of list of dict): A board of cards

    Returns:
    (list of list of (int, int)): A list of sets. Each set is a list of tuples containing the index
                                  of each card.
    """
    spread = list(chain.from_iterable(board))
    spread_sets = _find_sets(spread)
    index_converter = _spread_index_to_board_index(board)
    board_indices = [list(map(index_converter, s)) for s in spread_sets]
    return board_indices
    #return list(zip(board_indices, [s[1] for s in spread_sets]))

def _find_sets(spread, current_set=[]):
    """
    Finds all sets present in a spread.

    Finds all sets present in a spread, which is a flattened board. Returns a list of lists for 
    each set relative to the card's index in the spread.

    Parameters:
    spread (list of dict): A spread, or flattened board of cards.
    current_set (list of (int, dict), optional): The current group of indices and cards being
                                                 tested.
                                                 Defaults to an empty list.

    Returns:
    (list of list of int): A list of sets found in the spread. Each set contains the indices of
                           3 cards in the spread that constitute a set.
    """
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
        s = _find_sets(remaining_spread, current_set)
        current_set.pop()
        r += s
    return r

def _spread_index_to_board_index(board, vertical_flip=False):
    """
    Creates a lambda function that converts a spread index into a board index.
    
    Creates a lambda function that converts a spread index into a board index. The spread and the 
    board represent the same cards as the spread is just a flattened board. Option to flip the 
    converted indices if the spread represents a flipped board.

    Parameters:
    board (list of list of dict): The board of cards used to create the spread.
    vertical_flip (bool, optional): If True, flip the converted indices.
                                    If False, do not flip the converted indices.
                                    Defaults to False.

    Returns:
    (function): A lambda function that converts a spread index into a board index.
        Parameters:
        spread_index (int): The spread index to be converted.

        Returns:
        ((int, int)): The corresponding board index.
    """
    if vertical_flip:
        return lambda spread_index : (math.abs((int)(spread_index / len(board[0])) - len(board)), spread_index % len(board[0]))
    return lambda spread_index : ((int)(spread_index / len(board[0])), spread_index % len(board[0]))
