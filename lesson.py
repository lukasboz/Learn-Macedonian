import csv, random

class Lesson:
    def __init__(self, filepath):
        self.cards = []
        with open(filepath, encoding='utf-8') as f:
            for q, a in csv.reader(f):
                if q and a:
                    self.cards.append((q.strip(), a.strip()))
        random.shuffle(self.cards)
        self.all_answers = [a for _, a in self.cards]
