# FILE: ui/selection_frame.py

import re
import customtkinter as ctk

DISPLAY_OVERRIDES = {
    'basicverbs':     'Basic Verbs',
    'commonphrases':  'Common Phrases',
    'directionstime': 'Directions & Time',
    'greetings':      'Greetings',
    'food':           'Food',
}

class SelectionFrame(ctk.CTkFrame):
    def __init__(self, master, topic_folder, sublessons, on_start, on_back):
        super().__init__(master)

        raw = re.sub(r'^\d+_?', '', topic_folder)
        key = raw.lower().replace('_', '').replace(' ', '')
        self.display_name = DISPLAY_OVERRIDES.get(key, raw.replace('_', ' ').title())

        # Main centered container
        container = ctk.CTkFrame(self)
        container.pack(expand=True)

        # Header
        ctk.CTkLabel(
            container,
            text=f'Lessons in {self.display_name}',
            font=('Arial', 20, 'bold')
        ).pack(pady=10)

        # Scrollable list of sub-lessons
        self.lesson_scroll = ctk.CTkScrollableFrame(container, width=300, height=350)
        self.lesson_scroll.pack(pady=10)

        self.lesson_buttons = []

        for idx, fn in enumerate(sublessons):
            base = fn[:-4]
            if base.startswith('match_'):
                title_key = base.split('match_', 1)[1]
                title = title_key.replace('_', ' ').title()
                text = f'{self.display_name} Matching: {title}'
            elif base.startswith('sentence_'):
                text = f'{self.display_name} Sentence Builder: {idx+1}'
            else:
                text = f'{self.display_name} Definitions: {idx+1}'

            btn = ctk.CTkButton(
                self.lesson_scroll,
                text=text,
                width=280,
                command=lambda idx=idx: on_start(idx)
            )
            btn.pack(pady=8)
            self.lesson_buttons.append(btn)

        ctk.CTkButton(
            container,
            text='Back to Topics',
            command=on_back
        ).pack(pady=5)
