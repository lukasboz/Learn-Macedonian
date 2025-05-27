# FILE: sentence_builder.py

import csv

class SentenceBuilderLesson:
    """
    Loads CSV rows of:
      English sentence, Macedonian sentence,
      [optional] pipe-separated Macedonian blocks,
      [optional] pipe-separated English blocks.
    If blocks aren’t provided, splits on whitespace.
    """
    def __init__(self, filepath):
        self.items = []
        with open(filepath, encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) < 2:
                    continue
                eng = row[0].strip()
                mac = row[1].strip()
                # Macedonian blocks
                if len(row) > 2 and row[2].strip():
                    mk_blocks = [b.strip() for b in row[2].split('|') if b.strip()]
                else:
                    mk_blocks = mac.split()
                # English blocks
                if len(row) > 3 and row[3].strip():
                    en_blocks = [b.strip() for b in row[3].split('|') if b.strip()]
                else:
                    en_blocks = eng.split()
                self.items.append((eng, mac, mk_blocks, en_blocks))
        self.total = len(self.items)
