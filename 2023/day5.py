from pathlib import Path
import sys
import timeit
from typing import List

def run(part: int) -> int:
    with open(Path(__file__).parent / 'inputs' / 'day5.txt', 'r') as f:
        a = f.readlines()

    almanac = Almanac(a)
    return almanac.run(part)

class Almanac:
    def __init__(self, almanac: List[str]) -> None:
        seeds = almanac[0].split(':', 1)[1]
        self.seeds = None
        self.num_seeds_p2 = 0
        self._init_seeds([int(x) for x in seeds.split()])

        self.maps = {}
        i = 2
        while i < len(almanac):
            connection, _ = almanac[i].split(maxsplit=1)
            source, _, dest = connection.split('-', 3)
            i += 1
            j = i
            while j < len(almanac) and almanac[j] != '\n':
                j += 1
            self.maps[source] = Map(almanac[i:j], dest)
            i = j
            i += 1

    def _init_seeds(self, seed_list: List[str]) -> None:
        seed_ranges = []
        s_i = 0
        while s_i < len(seed_list):
            start = seed_list[s_i]
            length = seed_list[s_i + 1]
            self.num_seeds_p2 += length
            seed_ranges.append((start, length))
            s_i += 2
        self.seeds = (seed_list, seed_ranges)

    def run(self, part: int) -> List[int]:
        min_loc = float('inf')
        if part == 2:
            for start, length in self.seeds[1]:
                s = start
                while s < start+length:
                    val, min_to_edge = self._process_seed(s)
                    if val < min_loc:
                        min_loc = val
                    s += min_to_edge
        else:
            for s in self.seeds[0]:
                val, _ = self._process_seed(s)
                if val < min_loc:
                    min_loc = val
        return min_loc

    def _process_seed(self, s: int) -> int:
        source = 'seed'
        min_to_edge = float('inf')
        while source in self.maps:
            m = self.maps[source]
            new_val, dist_to_edge = m.get_destination_value(s)
            if dist_to_edge < min_to_edge:
                min_to_edge = dist_to_edge
            s = new_val
            source = m.destination
        return s, min_to_edge


class Map:
    def __init__(self, map: List[str], destination: str) -> None:
        self.destination = destination
        maps = []
        for line in map:
            dest_start, source_start, length = line.split(maxsplit=3)
            maps.append((int(dest_start), int(source_start), int(length)))
        self.maps = sorted(maps, key=lambda x: x[1])

    def get_destination_value(self, source_val: int) -> (int, int):
        for d, s, l in self.maps:
            if source_val < s:
                return source_val, s-source_val
            if source_val in range(s, s+l):
                diff = source_val - s
                return d + diff, s+l - source_val
        return source_val, float('inf')

if __name__ == '__main__':
    if len(sys.argv) > 1:
        part = int(sys.argv[1])
    else:
        part = 1
    print(run(part))
