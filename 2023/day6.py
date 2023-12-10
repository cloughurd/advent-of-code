from pathlib import Path
import sys

def run(part: int) -> int:
    with open(Path(__file__).parent / 'inputs' / 'day6.txt', 'r') as f:
        records = f.readlines()
    if part == 2:
        times = [int(records[0].split(':', 1)[1].replace(' ', ''))]
        distances = [int(records[1].split(':', 1)[1].replace(' ', ''))]
    else:
        times = [int(x) for x in records[0].split()[1:]]
        distances = [int(x) for x in records[1].split()[1:]]
    ways_to_win = 1
    for i in range(len(times)):
        t = times[i]
        count = 0
        for j in range(t):
            d = j * (t-j)
            if d > distances[i]:
                count += 1
            elif count > 0:
                break
        ways_to_win *= count
    return ways_to_win



if __name__ == '__main__':
    if len(sys.argv) > 1:
        part = int(sys.argv[1])
    else:
        part = 1
    print(run(part))
