# FILE: ui/menu_frame.py

import re
import customtkinter as ctk

# Manual overrides for folder-name → display text
DISPLAY_OVERRIDES = {
    'basicverbs':     'Basic Verbs',
    'commonphrases':  'Common Phrases',
    'directionstime': 'Directions & Time',
    'greetings':      'Greetings',
    'food':           'Food',
    'pronouns':       'Pronouns',
    'family':         'Family',
    # add more overrides here if needed
}

class MenuFrame(ctk.CTkFrame):
    def __init__(
        self,
        master,
        topics,
        on_select,
        on_view_progress,
        on_save,
        on_reset,
        on_exit
    ):
        super().__init__(master)
        self.topics = topics
        self.on_select = on_select

        # Title (centered by default)
        ctk.CTkLabel(
            self,
            text='Choose a Topic',
            font=('Arial', 24, 'bold')
        ).pack(pady=(20, 10))

        # Scrollable list of topics
        self.topic_scroll = ctk.CTkScrollableFrame(
            self,
            width=300,
            height=400
        )
        self.topic_scroll.pack(pady=10)

        # Build topic buttons
        self.topic_buttons = []
        self.build_topic_menu()

        # Progress-related buttons (centered)
        prog_frame = ctk.CTkFrame(self)
        prog_frame.pack(pady=(20, 5))
        ctk.CTkButton(
            prog_frame,
            text='View Progress',
            width=120,
            command=on_view_progress
        ).grid(row=0, column=0, padx=10)
        ctk.CTkButton(
            prog_frame,
            text='Save Progress',
            width=120,
            command=on_save
        ).grid(row=0, column=1, padx=10)
        ctk.CTkButton(
            prog_frame,
            text='Reset Progress',
            width=120,
            command=on_reset
        ).grid(row=0, column=2, padx=10)

        # Exit button on its own row, centered
        exit_frame = ctk.CTkFrame(self)
        exit_frame.pack(pady=(5, 20))
        ctk.CTkButton(
            exit_frame,
            text='Exit',
            width=120,
            command=on_exit
        ).pack()

    def build_topic_menu(self):
        # clear existing buttons
        for b in self.topic_buttons:
            b.destroy()
        self.topic_buttons.clear()

        for i, topic in enumerate(self.topics):
            # strip leading digits + underscore, e.g. "05_Pronouns" → "Pronouns"
            raw = re.sub(r'^\d+_?', '', topic)
            key = raw.lower().replace('_', '').replace(' ', '')

            # override or Title Case
            display = DISPLAY_OVERRIDES.get(
                key,
                raw.replace('_', ' ').title()
            )

            btn = ctk.CTkButton(
                self.topic_scroll,
                text=display,
                width=280,
                command=lambda i=i: self.on_select(i)
            )
            btn.pack(pady=5)
            self.topic_buttons.append(btn)
