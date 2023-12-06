import sys

word_forms = [
    ('one', 1),
    ('two', 2),
    ('three', 3),
    ('four', 4),
    ('five', 5),
    ('six', 6),
    ('seven', 7),
    ('eight', 8),
    ('nine', 9),
]

def run(part: int):
    with open('inputs/day1.txt', 'r') as f:
        lines = f.readlines()

    total = 0
    new_lines = []
    for l in lines:
        if part == 2:
            l = swap_word_forms(l)
            new_lines.append(l)
        total += (get_edge_int(l, 1) * 10) + get_edge_int(l, -1)

    if part == 2:
        with open('inputs/day1-revised.txt', 'w') as f:
            f.writelines(new_lines)

    return total


def get_edge_int(s: str, dir: int) -> int:
    for c in s[::dir]:
        if c.isdigit():
            return int(c)
    return None

def swap_word_forms(s: str) -> str:
    '''
    Replaces the first character of each word form with the digit

    Changes "twone" into "2w1ne"
    '''
    new_s = s
    i = 0
    while i < len(s):
        for word, num in word_forms:
            if s[i:].startswith(word):
                new_s = new_s[0:i] + str(num) + new_s[i+1:]
                break
        i += 1
    return new_s

if __name__ == '__main__':
    if len(sys.argv) > 1:
        part = int(sys.argv[1])
    else:
        part = 1
    print(run(part))
