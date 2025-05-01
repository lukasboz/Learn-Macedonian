# FILE: ui/selection_frame.py

import re
import customtkinter as ctk

# Manual overrides for folder-name → display text
DISPLAY_OVERRIDES = {
    'basicverbs':     'Basic Verbs',
    'commonphrases':  'Common Phrases',
    'directionstime': 'Directions & Time',
    'greetings':      'Greetings',
    'food':           'Food',
    # add more overrides here if needed
}

class SelectionFrame(ctk.CTkFrame):
    def __init__(self, master, topic_folder, sublessons, on_start, on_back):
        super().__init__(master)

        # 1) strip leading digits + underscore (e.g. "01_Greetings" → "Greetings")
        raw = re.sub(r'^\d+_?', '', topic_folder)

        # 2) normalize key to look up overrides
        key = raw.lower().replace('_', '').replace(' ', '')

        # 3) choose display name
        self.display_name = DISPLAY_OVERRIDES.get(
            key,
            raw.replace('_', ' ').title()
        )

        # Header
        ctk.CTkLabel(
            self,
            text=f'Lessons in {self.display_name}',
            font=('Arial', 20, 'bold')
        ).pack(pady=10)

        # Scrollable list of lessons
        self.lesson_scroll = ctk.CTkScrollableFrame(
            self,
            width=300,
            height=350
        )
        self.lesson_scroll.pack(pady=10)

        self.lesson_buttons = []

        for idx, fn in enumerate(sublessons):
            base = fn[:-4]  # strip “.csv”

            if base.startswith('match_'):
                # Matching‐game lesson
                title_key = base.split('match_', 1)[1]
                title = title_key.replace('_', ' ').title()
                text = f'{self.display_name} Matching: {title}'
            else:
                # Quiz lesson → now labeled as Definitions
                text = f'{self.display_name} Definitions: {idx+1}'

            btn = ctk.CTkButton(
                self.lesson_scroll,
                text=text,
                width=280,
                command=lambda idx=idx: on_start(idx)
            )
            btn.pack(pady=8)
            self.lesson_buttons.append(btn)

        # Back button
        ctk.CTkButton(
            self,
            text='Back to Topics',
            command=on_back
        ).pack(pady=5)
