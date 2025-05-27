# FILE: ui/match_frame.py
# Two-column matching game frame

import customtkinter as ctk
import tkinter.messagebox as mb

from constants import resource_path  # 🔁 Added for future file compatibility

class MatchFrame(ctk.CTkFrame):
    def __init__(self, master, on_finish, on_back):
        super().__init__(master)
        self.on_finish = on_finish

        # define your standard colors once
        self.default_color = 'darkblue'
        self.hover_color   = 'blue'

        # Header
        self.topic_label = ctk.CTkLabel(self, font=('Arial', 18, 'bold'))
        self.topic_label.pack(pady=(10, 5))
        self.info_label = ctk.CTkLabel(
            self,
            text='Select an English term, then its Macedonian match',
            font=('Arial', 14)
        )
        self.info_label.pack(pady=(0, 10))

        # Two-column container
        container = ctk.CTkFrame(self)
        container.pack(pady=10, fill='both', expand=True)

        self.left_frame = ctk.CTkScrollableFrame(container, width=200, height=300)
        self.left_frame.pack(side='left', padx=10)
        self.right_frame = ctk.CTkScrollableFrame(container, width=200, height=300)
        self.right_frame.pack(side='right', padx=10)

        # Back button
        self.back_btn = ctk.CTkButton(self, text='Back', command=on_back)
        self.back_btn.pack(pady=5)

    def start(self, matching_lesson, topic_display, sub_idx):
        self.match = matching_lesson
        self.sublesson_index = sub_idx
        self.matched_count = 0
        self.total = len(self.match.left_items)

        self.topic_label.configure(text=f'{topic_display} – Matching')

        # Clear old widgets
        for w in self.left_frame.winfo_children():  w.destroy()
        for w in self.right_frame.winfo_children(): w.destroy()

        # Track selection
        self.selected_left = None
        self.left_btns = {}
        self.right_btns = {}

        # Build left (English) buttons – always darkblue, never highlight
        for item in self.match.left_items:
            btn = ctk.CTkButton(
                self.left_frame,
                text=item,
                width=180,
                fg_color=self.default_color,
                hover_color=self.hover_color,
                command=lambda i=item: self.select_left(i)
            )
            btn.pack(pady=5)
            self.left_btns[item] = btn

        # Build right (Macedonian) buttons
        for item in self.match.right_items:
            btn = ctk.CTkButton(
                self.right_frame,
                text=item,
                width=180,
                fg_color=self.default_color,
                hover_color=self.hover_color,
                command=lambda i=item: self.select_right(i)
            )
            btn.pack(pady=5)
            self.right_btns[item] = btn

        self.pack()

    def select_left(self, item):
        self.selected_left = item

    def select_right(self, item):
        if not self.selected_left:
            mb.showwarning('Select first', 'Please pick an English term first.')
            return

        correct = self.match.mapping[self.selected_left]
        if item == correct:
            mb.showinfo('Correct', 'Good match!')
            self.left_btns[self.selected_left].configure(
                fg_color=self.default_color,
                state='disabled'
            )
            self.right_btns[item].configure(
                fg_color=self.default_color,
                state='disabled'
            )
            self.matched_count += 1

            if self.matched_count == self.total:
                mb.showinfo('Done', 'All pairs matched!')
                self.on_finish(self.sublesson_index, self.total)
                self.pack_forget()
        else:
            mb.showinfo('Incorrect', 'Try again.')

        self.selected_left = None
