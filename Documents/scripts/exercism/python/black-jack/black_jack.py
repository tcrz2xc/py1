"""Functions to help play and score a game of blackjack.

How to play blackjack:    https://bicyclecards.com/how-to-play/blackjack/
"Standard" playing cards: https://en.wikipedia.org/wiki/Standard_52-card_deck
"""


def value_of_card(card):
    """Determine the scoring value of a card.

    :param card: str - given card.
    :return: int - value of a given card.  See below for values.

    1.  'J', 'Q', or 'K' (otherwise known as "face cards") = 10
    2.  'A' (ace card) = 1
    3.  '2' - '10' = numerical value.
    """
    if card =='2' or card == '3' or card  == '4' or card =='5' or card =='6' or card =='7' or card =='8' or card =='9' or card=='10':
        return int(card)
    elif card == 'J' or card == 'Q' or card == 'K':
        return 10
    else:
        return 1
    pass


def higher_card(card_one, card_two):
    """Determine which card has a higher value in the hand.

    :param card_one, card_two: str - cards dealt in hand.  See below for values.
    :return: str or tuple - resulting Tuple contains both cards if they are of equal value.

    1.  'J', 'Q', or 'K' (otherwise known as "face cards") = 10
    2.  'A' (ace card) = 1
    3.  '2' - '10' = numerical value.
    """
    if value_of_card(card_one)> value_of_card(card_two):
        return card_one
    elif value_of_card(card_one)<value_of_card(card_two):
        return card_two
    else:
        return card_one, card_two
    pass


def value_of_ace(card_one, card_two):
    """Calculate the most advantageous value for the ace card.

    :param card_one, card_two: str - card dealt. See below for values.
    :return: int - either 1 or 11 value of the upcoming ace card.

    1.  'J', 'Q', or 'K' (otherwise known as "face cards") = 10
    2.  'A' (ace card) = 11 (if already in hand)
    3.  '2' - '10' = numerical value.
    """
    sum_of_cards1= value_of_card(card_one)+value_of_card(card_two)
    if sum_of_cards1 <=10 and not (card_one == 'A' or card_two == 'A'):
        return 11
    else:
        return 1
    pass


def is_blackjack(card_one, card_two):
    """Determine if the hand is a 'natural' or 'blackjack'.

    :param card_one, card_two: str - card dealt. See below for values.
    :return: bool - is the hand is a blackjack (two cards worth 21).

    1.  'J', 'Q', or 'K' (otherwise known as "face cards") = 10
    2.  'A' (ace card) = 11 (if already in hand)
    3.  '2' - '10' = numerical value.
    """
    if card_one == 'A' and (card_two == '10' or card_two == 'K' or card_two == 'Q' or card_two =='J'):
        return True
    elif (card_one == '10' or card_one == 'K' or card_one == 'Q' or card_one == 'J') and card_two == 'A':
        return True
    else:
        return False
    pass


def can_split_pairs(card_one, card_two):
    """Determine if a player can split their hand into two hands.

    :param card_one, card_two: str - cards dealt.
    :return: bool - can the hand be split into two pairs? (i.e. cards are of the same value).
    """
    if value_of_card(card_one) == value_of_card(card_two):
        return True
    else:
        return False
    pass


def can_double_down(card_one, card_two):
    """Determine if a blackjack player can place a double down bet.

    :param card_one, card_two: str - first and second cards in hand.
    :return: bool - can the hand can be doubled down? (i.e. totals 9, 10 or 11 points).
    """
    sum_of_cards = value_of_card(card_one)+value_of_card(card_two)
    if sum_of_cards == 9 or sum_of_cards == 10 or sum_of_cards == 11:
        return True
    else:
        return False
    pass
