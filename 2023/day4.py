from pathlib import Path
import sys

def run(part: int) -> int:
    with open(Path(__file__).parent / 'inputs' / 'day4.txt', 'r') as f:
        cards = f.readlines()

    total_points = 0
    counts = [1 for x in range(len(cards))]
    for idx, c in enumerate(cards):
        matches, points = count_card_points(c)
        total_points += points
        for i in range(matches):
            if idx + i + 1 >= len(counts):
                break
            counts[idx + i + 1] += counts[idx]
    if part == 2:
        return sum(counts)
    return total_points

def count_card_points(card: str) -> (int, int):
    _, numbers = card.split(':', 1)
    winning, yours = numbers.split('|', 1)
    winning = set(winning.split())
    count = 0
    for num in yours.split():
        if num in winning:
            count += 1
    if count == 0:
        return 0, 0
    return count, 2**(count - 1)



if __name__ == '__main__':
    if len(sys.argv) > 1:
        part = int(sys.argv[1])
    else:
        part = 1
    print(run(part))
