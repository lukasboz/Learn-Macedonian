# FILE: matching.py
# NEW: MatchingLesson class to parse “matching” CSVs

import csv
import random

class MatchingLesson:
    def __init__(self, filepath):
        self.pairs = []
        with open(filepath, encoding='utf-8') as f:
            reader = csv.reader(f)
            for left, right in reader:
                if left and right:
                    self.pairs.append((left.strip(), right.strip()))
        # shuffle display order
        self.left_items = [l for l, r in self.pairs]
        self.right_items = [r for l, r in self.pairs]
        random.shuffle(self.left_items)
        random.shuffle(self.right_items)
        # map left→right
        self.mapping = {l: r for l, r in self.pairs}
