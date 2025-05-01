# FILE: ui/quiz_frame.py

import random
import customtkinter as ctk
import tkinter.messagebox as mb

class QuizFrame(ctk.CTkFrame):
    def __init__(self, master, on_finish, on_back):
        super().__init__(master)
        self.on_finish = on_finish

        # Title label
        self.topic_label = ctk.CTkLabel(self, font=('Arial', 18, 'bold'))
        self.topic_label.pack(pady=(10, 5))

        # --- EDITED: show "Question X of Y" ---
        self.qnum_label = ctk.CTkLabel(self, font=('Arial', 14))
        self.qnum_label.pack(pady=(0, 10))

        # Question prompt
        self.question_label = ctk.CTkLabel(self, wraplength=480, font=('Arial', 16))
        self.question_label.pack(pady=5)

        # Choices container
        self.choice_frame = ctk.CTkFrame(self)
        self.choice_frame.pack(pady=10)

        self.choice_var = ctk.StringVar()
        self.choice_buttons = []

        # Navigation buttons
        nav_frame = ctk.CTkFrame(self)
        nav_frame.pack(pady=5)
        self.prev_btn = ctk.CTkButton(nav_frame, text='Previous',
                                      command=self.prev_card)
        self.prev_btn.grid(row=0, column=0, padx=10)
        self.submit_btn = ctk.CTkButton(nav_frame, text='Submit',
                                        command=self.check_answer)
        self.submit_btn.grid(row=0, column=1, padx=10)

        # Internal state
        self.card_idx = 0
        self.score = 0
        self.lesson = None
        self.sublesson_index = None

    def start(self, lesson_obj, topic_display, sub_idx):
        self.lesson = lesson_obj
        self.sublesson_index = sub_idx
        self.card_idx = 0
        self.score = 0

        self.topic_label.configure(text=f'{topic_display} - Lesson {sub_idx+1}')
        self.show_card()
        self.pack()

    def show_card(self):
        total = len(self.lesson.cards)
        if self.card_idx >= total:
            return self.finish()

        # --- EDITED: update question counter ---
        self.qnum_label.configure(
            text=f'Question {self.card_idx+1} of {total}'
        )

        q, a = self.lesson.cards[self.card_idx]
        self.question_label.configure(text=f"Translate '{q}' into Macedonian:")

        for btn in self.choice_buttons:
            btn.destroy()
        self.choice_buttons.clear()
        self.choice_var.set('')

        opts = random.sample(
            [x for x in self.lesson.all_answers if x != a], 3
        ) + [a]
        random.shuffle(opts)

        for opt in opts:
            btn = ctk.CTkButton(
                self.choice_frame,
                text=opt,
                width=300, height=40,
                fg_color='darkblue',
                hover_color='blue',
                command=lambda o=opt: self.select_answer(o)
            )
            btn.pack(fill='x', pady=8)
            self.choice_buttons.append(btn)

    def select_answer(self, choice):
        self.choice_var.set(choice)
        for btn in self.choice_buttons:
            btn.configure(
                fg_color=('lightblue','blue')
                if btn.cget('text') == choice else 'darkblue'
            )

    def check_answer(self):
        sel = self.choice_var.get()
        if not sel:
            mb.showwarning('No Selection','Please choose an answer.')
            return

        _, correct = self.lesson.cards[self.card_idx]
        if sel == correct:
            self.score += 1
            mb.showinfo('Correct','Well done!')
        else:
            mb.showinfo('Incorrect',f'The correct answer was: {correct}')

        self.card_idx += 1
        self.show_card()

    def prev_card(self):
        if self.card_idx > 0:
            self.card_idx -= 1
            self.show_card()

    def finish(self):
        total = len(self.lesson.cards)
        mb.showinfo('Lesson Complete', f'You scored {self.score}/{total}')
        self.on_finish(self.sublesson_index, self.score)
        self.pack_forget()
