from collections import defaultdict
from functools import cmp_to_key, partial
from pathlib import Path
import sys

CARD_ORDER_1 = 'AKQJT98765432'
CARD_ORDER_2 = 'AKQT98765432J'

def run(part: int) -> int:
    with open(Path(__file__).parent / 'inputs' / 'day7.txt', 'r') as f:
        hand_strs = f.readlines()
    hands = []
    for h in hand_strs:
        cards, bid = h.split()
        hand_type = get_hand_type(cards, part)
        hands.append((cards, hand_type, int(bid)))
    if part == 2:
        sort_func = partial(compare_hands, CARD_ORDER_2)
    else:
        sort_func = partial(compare_hands, CARD_ORDER_1)
    hands = sorted(hands, key=cmp_to_key(sort_func))

    total = 0
    for i in range(len(hands)):
        total += (i+1) * hands[i][2]
    return total

def get_hand_type(hand: str, part: int) -> float:
    card_counts = {}
    for card in CARD_ORDER_1:
        card_counts[card] = hand.count(card)
    count_counts = defaultdict(lambda: 0)
    for count in card_counts.values():
        count_counts[count] += 1
    max_count = max(card_counts.values())
    max_incl_j = max([card_counts[x] + card_counts['J'] for x in card_counts if x != 'J'])
    if max_count == 5:
        return 5
    elif max_incl_j > 4 and part == 2:
        return 5
    elif max_count == 4:
        return 4
    elif max_incl_j == 4 and part == 2:
        return 4
    elif max_count == 3:
        if count_counts[2] == 1:
            return 3.5
        return 3
    elif max_incl_j == 3 and part == 2:
        if card_counts['J'] == 1:
            if count_counts[2] == 2:
                return 3.5
            return 3
        return 3
    elif max_count == 2:
        if count_counts[2] == 2:
            return 2.5
        return 2
    elif max_incl_j == 2 and part == 2:
        return 2
    return 1

def compare_hands(card_order: str, hand1: (str, int, int), hand2: (str, int, int)) -> int:
    if hand1[1] > hand2[1]:
        return 1
    elif hand2[1] > hand1[1]:
        return -1
    for i in range(5):
        card1 = hand1[0][i]
        card2 = hand2[0][i]
        if card1 == card2:
            continue
        if card_order.find(card1) < card_order.find(card2):
            return 1
        elif card_order.find(card2) < card_order.find(card1):
            return -1
    return 0


if __name__ == '__main__':
    if len(sys.argv) > 1:
        part = int(sys.argv[1])
    else:
        part = 1
    print(run(part))
