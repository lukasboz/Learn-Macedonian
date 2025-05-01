# FILE: ui/menu_frame.py

import re
import customtkinter as ctk

# Manual overrides for folder-name → display text
DISPLAY_OVERRIDES = {
    'basicverbs':    'Basic Verbs',
    'commonphrases': 'Common Phrases',
    'directionstime':'Directions & Time',
    # add more overrides here as needed
}

class MenuFrame(ctk.CTkFrame):
    def __init__(
        self,
        master,
        topics,
        unlocked_topic,   # still accepted but no longer used for gating
        on_select,
        on_save,
        on_reset,
        on_exit
    ):
        super().__init__(master)
        self.topics    = topics
        self.on_select = on_select

        # Title
        ctk.CTkLabel(
            self,
            text='Choose a Topic',
            font=('Arial', 24, 'bold')
        ).pack(pady=10)

        # Scrollable container for topic buttons
        self.topic_scroll = ctk.CTkScrollableFrame(
            self,
            width=300,
            height=400
        )
        self.topic_scroll.pack(pady=10)

        # build buttons (will show all topics)
        self.topic_buttons = []
        self.build_topic_menu()

        # Bottom controls: Save, Reset, Exit
        btnf = ctk.CTkFrame(self)
        btnf.pack(pady=10)
        ctk.CTkButton(btnf, text='Save Progress',  command=on_save)\
            .grid(row=0, column=0, padx=5)
        ctk.CTkButton(btnf, text='Reset Progress', command=on_reset)\
            .grid(row=0, column=1, padx=5)
        ctk.CTkButton(btnf, text='Exit',           command=on_exit)\
            .grid(row=0, column=2, padx=5)

    def build_topic_menu(self):
        # clear existing buttons
        for b in self.topic_buttons:
            b.destroy()
        self.topic_buttons.clear()

        # iterate ALL topics
        for i, topic in enumerate(self.topics):
            # 1) strip leading numbers + underscore, e.g. "06_CommonPhrases" → "CommonPhrases"
            raw = re.sub(r'^\d+_?', '', topic)
            key = raw.lower()

            # 2) apply override or default Title Case
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
