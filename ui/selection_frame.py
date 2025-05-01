# FILE: ui/selection_frame.py

import customtkinter as ctk

# Manual overrides: normalized key → desired display name
DISPLAY_OVERRIDES = {
    'basicverbs': 'Basic Verbs',
    # you can add more overrides here in the same normalized form
}

class SelectionFrame(ctk.CTkFrame):
    def __init__(self, master, topic_display_raw, sublessons, on_start, on_back):
        super().__init__(master)

        # Normalize the incoming topic name to a key:
        #  - strip whitespace
        #  - lowercase
        #  - remove spaces & underscores
        key = (
            topic_display_raw
            .strip()
            .lower()
            .replace(' ', '')
            .replace('_', '')
        )

        # Look up an override, or fall back to the raw display
        self.display_name = DISPLAY_OVERRIDES.get(key, topic_display_raw)

        # Header
        ctk.CTkLabel(
            self,
            text=f'Lessons in {self.display_name}',
            font=('Arial', 20, 'bold')
        ).pack(pady=10)

        # Scrollable list of sub-lessons
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
                # matching game
                title = base.split('match_', 1)[1].replace('_', ' ').title()
                text = f'{self.display_name} Matching: {title}'
            else:
                # regular quiz
                text = f'{self.display_name} {idx+1}'

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
