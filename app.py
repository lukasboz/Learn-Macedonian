"""
LearnMacedonian App in Python using CustomTkinter

Features:
- Main menu shows unlockable lessons as a vertical, scrollable path
- Clickable lesson nodes instead of a dropdown
- Save, Reset, Exit from menu
- Lessons loaded from lessons/<folder>/<file>.csv
- Multiple-choice questions with styled buttons
- Progress unlocked per topic; cannot pick beyond the next
- Progress saved to progress.json silently on autosave
- Main menu centered horizontally and vertically
- Lesson UI fully centered (titles, questions, choices)
"""
import os
import csv
import json
import random
import customtkinter as ctk
import tkinter.messagebox as mb

# Theme setup
tk_mode = "System"  # Modes: "System", "Dark", "Light"
ctk.set_appearance_mode(tk_mode)
ctk.set_default_color_theme("blue")

BASE_DIR = os.path.dirname(__file__)
LESSONS_DIR = os.path.join(BASE_DIR, 'lessons')
PROGRESS_FILE = os.path.join(BASE_DIR, 'progress.json')

class Lesson:
    def __init__(self, folder, filename):
        self.folder = folder
        self.cards = []
        path = os.path.join(LESSONS_DIR, folder, filename)
        with open(path, encoding='utf-8') as f:
            for q, a in csv.reader(f):
                if q and a:
                    self.cards.append((q.strip(), a.strip()))
        random.shuffle(self.cards)
        self.all_answers = [ans for _, ans in self.cards]

class LearnMacedonian(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title('Learn Macedonian')
        self.geometry('520x600')

        # Center grid
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Load topics
        raw = [d for d in os.listdir(LESSONS_DIR)
               if os.path.isdir(os.path.join(LESSONS_DIR, d))]
        self.topics = sorted(raw)

        # Load progress
        self.unlocked = 0
        self.topic_progress = {}
        self.load_progress()

        # Main menu UI
        self.menu_frame = ctk.CTkFrame(self)
        self.menu_frame.grid(row=0, column=0)
        ctk.CTkLabel(self.menu_frame, text='Learn Macedonian', 
                     font=('Arial', 24, 'bold')).pack(pady=10)
        self.scroll = ctk.CTkScrollableFrame(self.menu_frame, width=300, height=400)
        self.scroll.pack(pady=10)
        self.lesson_buttons = []
        self.build_lesson_path()

        btn_frame = ctk.CTkFrame(self.menu_frame)
        btn_frame.pack(pady=10)
        ctk.CTkButton(btn_frame, text='Save Progress', command=self.manual_save).grid(row=0, column=0, padx=5)
        ctk.CTkButton(btn_frame, text='Reset Progress', command=self.reset_progress).grid(row=0, column=1, padx=5)
        ctk.CTkButton(btn_frame, text='Exit', command=self.destroy).grid(row=0, column=2, padx=5)

        # Lesson UI container frame (hidden until start)
        self.lesson_frame = ctk.CTkFrame(self)
        self.lesson_frame.grid(row=0, column=0)
        self.lesson_frame.grid_remove()

        # Lesson UI elements inside lesson_frame
        self.topic_label = ctk.CTkLabel(self.lesson_frame, font=('Arial', 18, 'bold'), justify='center')
        self.question_label = ctk.CTkLabel(self.lesson_frame, wraplength=480, justify='center', font=('Arial', 16))
        self.choice_frame = ctk.CTkFrame(self.lesson_frame)
        self.choice_var = ctk.StringVar()
        self.choice_buttons = []
        self.submit_btn = ctk.CTkButton(self.lesson_frame, text='Submit', command=self.check_answer)

        # Lesson state
        self.current = None
        self.lesson = None
        self.index = 0
        self.score = 0

    def build_lesson_path(self):
        for btn in self.lesson_buttons:
            btn.destroy()
        self.lesson_buttons.clear()
        for idx, folder in enumerate(self.topics[:self.unlocked+1]):
            name = folder.split('_', 1)[1] if '_' in folder else folder
            btn = ctk.CTkButton(
                self.scroll,
                text=name,
                width=200,
                height=50,
                corner_radius=10,
                fg_color='transparent',
                hover_color='blue',
                anchor='center',
                command=lambda i=idx: self.start_lesson(i)
            )
            btn.pack(pady=5)
            self.lesson_buttons.append(btn)

    def load_progress(self):
        if os.path.exists(PROGRESS_FILE):
            try:
                data = json.load(open(PROGRESS_FILE, 'r', encoding='utf-8'))
                self.unlocked = data.get('unlocked', 0)
                self.topic_progress = data.get('topic_progress', {})
            except:
                pass

    def manual_save(self):
        self.save_progress()
        mb.showinfo('Progress', 'Progress saved.')

    def save_progress(self):
        data = {'unlocked': self.unlocked, 'topic_progress': self.topic_progress}
        with open(PROGRESS_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def reset_progress(self):
        if mb.askyesno('Reset', 'Reset all progress?'):
            try: os.remove(PROGRESS_FILE)
            except: pass
            self.unlocked = 0
            self.topic_progress = {}
            mb.showinfo('Reset', 'Progress reset.')
            self.build_lesson_path()

    def start_lesson(self, topic_idx):
        self.current = topic_idx
        folder = self.topics[topic_idx]
        files = sorted([f for f in os.listdir(os.path.join(LESSONS_DIR, folder)) if f.endswith('.csv')])
        if not files:
            mb.showwarning('Empty', 'No CSV files in this lesson.')
            return
        self.lesson = Lesson(folder, files[0])
        prog = self.topic_progress.get(folder, {})
        self.index = prog.get('last_index', 0)
        self.score = prog.get('last_score', 0)

        # Hide menu, show lesson frame
        self.menu_frame.grid_remove()
        self.lesson_frame.grid()

        # Clear previous lesson widgets
        for widget in self.lesson_frame.winfo_children():
            widget.pack_forget()

        # Pack lesson UI centered
        self.topic_label.configure(text=folder.split('_',1)[1])
        self.topic_label.pack(pady=(40,10))
        self.question_label.pack(pady=(10,10))
        self.choice_frame.pack(pady=10)
        self.submit_btn.pack(pady=(20,20))

        self.show_card()

    def show_card(self):
        if self.index >= len(self.lesson.cards):
            mb.showinfo('Done', f'Score {self.score}/{len(self.lesson.cards)}')
            if self.current == self.unlocked and self.unlocked < len(self.topics) - 1:
                self.unlocked += 1
                self.build_lesson_path()
            folder = self.topics[self.current]
            self.topic_progress[folder] = {'last_index': len(self.lesson.cards), 'last_score': self.score}
            self.save_progress()
            return self.return_to_menu()

        q, correct = self.lesson.cards[self.index]
        self.question_label.configure(text=f'Q{self.index+1}: {q}')

        distractors = [a for a in self.lesson.all_answers if a != correct]
        choices = random.sample(distractors, min(3, len(distractors))) + [correct]
        random.shuffle(choices)

        # Clear old buttons
        for b in self.choice_buttons:
            b.destroy()
        self.choice_buttons.clear()
        self.choice_var.set('')

        # Create and center new buttons
        for opt in choices:
            btn = ctk.CTkButton(
                self.choice_frame,
                text=opt,
                width=300,
                height=40,
                corner_radius=8,
                fg_color='transparent',
                hover_color='blue',
                command=lambda o=opt: self.select(o)
            )
            btn.grid(row=self.choice_buttons.__len__(), column=0, pady=5)
            self.choice_buttons.append(btn)

    def select(self, opt):
        self.choice_var.set(opt)
        for b in self.choice_buttons:
            b.configure(fg_color=('lightblue','blue') if b.cget('text') == opt else 'transparent')

    def check_answer(self):
        sel = self.choice_var.get()
        if not sel:
            mb.showwarning('Choose', 'Select an answer.')
            return
        _, corr = self.lesson.cards[self.index]
        if sel == corr:
            self.score += 1
            mb.showinfo('Good', 'Correct!')
        else:
            mb.showinfo('Oops', f'Correct: {corr}')
        self.index += 1
        folder = self.topics[self.current]
        self.topic_progress[folder] = {'last_index': self.index, 'last_score': self.score}
        self.save_progress()
        self.show_card()

    def return_to_menu(self):
        # Clear lesson UI and hide frame
        self.lesson_frame.grid_remove()
        # Return to menu
        self.menu_frame.grid()
        # Reset choice frame children
        for b in self.choice_buttons:
            b.destroy()
        self.choice_buttons.clear()

if __name__ == '__main__':
    LearnMacedonian().mainloop()
