from pathlib import Path
import sys

def run(part: int):
    with open(Path(__file__).parent / 'inputs' / 'day2.txt', 'r') as f:
        games = f.readlines()

    total = 0
    for g in games:
        game = Game(g)
        if part == 2:
            total += game.get_power()
        elif game.eval_game(14, 13, 12):
            total += game.game_id
    return total

class Game:
    def __init__(self, game_str: str) -> None:
        label, rounds = game_str.split(':', 1)
        self.game_id = int(label.split(' ', 1)[1])
        self.max_blue = -1
        self.max_green = -1
        self.max_red = -1
        self.rounds = []
        for r in rounds.split(';'):
            round = Round(r)
            self.rounds.append(round)
            if round.blue > self.max_blue:
                self.max_blue = round.blue
            if round.green > self.max_green:
                self.max_green = round.green
            if round.red > self.max_red:
                self.max_red = round.red

    def eval_game(self, blue_limit, green_limit, red_limit):
        if self.max_blue > blue_limit:
            return False
        if self.max_green > green_limit:
            return False
        if self.max_red > red_limit:
            return False
        return True

    def get_power(self):
        return abs(self.max_blue * self.max_green * self.max_red)

class Round:
    def __init__(self, round_str: str) -> None:
        self.blue = -1
        self.green = -1
        self.red = -1
        for pair in round_str.split(','):
            count, color = pair.strip().split(' ', 1)
            if color == 'blue':
                self.blue = int(count)
            elif color == 'green':
                self.green = int(count)
            elif color == 'red':
                self.red = int(count)
            else:
                print('Unknown color encountered: ', pair)



if __name__ == '__main__':
    if len(sys.argv) > 1:
        part = int(sys.argv[1])
    else:
        part = 1
    print(run(part))
