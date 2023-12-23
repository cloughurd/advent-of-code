import argparse
from collections import defaultdict
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
import sys
from typing import Dict, List, Set, Tuple
import numpy as np
import importlib
import shared

def part1(lines: List[str]) -> int:
    bp = [i for i in range(len(lines)) if lines[i] == '\n'][0]
    w = WorkflowEngine.from_lines(lines[0:bp])
    accepted = []
    for i in range(bp+1, len(lines)):
        p = Part.from_str(lines[i])
        if w.accept_part(p):
            accepted.append(p)
    return sum([x.total_rating for x in accepted])

def part2(lines:List[str]) -> int:
    pass

@dataclass
class Part:
    ratings: Dict[str, int]

    @property
    def total_rating(self) -> int:
        return sum(self.ratings.values())

    @classmethod
    def from_str(cls, s: str) -> 'Part':
        _, s = s.split('{', 1)
        s, _ = s.split('}', 1)
        ratings = {}
        for r in s.split(','):
            cat, v = r.split('=', 1)
            ratings[cat] = int(v)
        return cls(ratings)

@dataclass
class WorkflowStep:
    value: str
    comparison: str
    threshold: int
    destination: str

    @classmethod
    def from_str(cls, s: str) -> 'WorkflowStep':
        s, dest = s.split(':')
        v = s[0]
        c = s[1]
        t = s[2:]
        return cls(v, c, int(t), dest)

    def test(self, num: int) -> bool:
        if self.comparison == '<':
            return num < self.threshold
        return num > self.threshold

@dataclass
class Workflow:
    name: str
    steps: List[WorkflowStep]
    default_destination: str

    @classmethod
    def from_str(cls, s: str) -> 'Workflow':
        name, s = s.split('{', 1)
        s = s.split('}', 1)[0]
        steps_raw = s.split(',')
        steps = []
        for i in range(len(steps_raw)-1):
            steps.append(WorkflowStep.from_str(steps_raw[i]))
        fin = steps_raw[-1]
        return cls(name, steps, fin)

    def run(self, p: Part) -> str:
        for s in self.steps:
            if s.test(p.ratings[s.value]):
                return s.destination
        return self.default_destination

@dataclass
class WorkflowEngine:
    workflows: Dict[str, Workflow]

    @classmethod
    def from_lines(cls, lines: List[str]) -> 'WorkflowEngine':
        workflows = {}
        for line in lines:
            w = Workflow.from_str(line)
            workflows[w.name] = w
        return cls(workflows)

    def accept_part(self, p: Part) -> bool:
        d = 'in'
        while d not in ['A', 'R']:
            d = self.workflows[d].run(p)
        if d == 'A':
            return True
        return False


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('part', choices=[1, 2], default=1, type=int)
    parser.add_argument('-f', '--file', dest='filename', default='day19.txt')
    args = parser.parse_args()

    with open(Path(__file__).parent / 'inputs' / args.filename, 'r') as f:
        lines = f.readlines()

    if args.part == 2:
        print(part2(lines))
    else:
        print(part1(lines))
