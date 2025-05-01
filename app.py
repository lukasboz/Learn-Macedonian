# FILE: app.py

import os
from tkinter import PhotoImage
import customtkinter as ctk

from constants import BASE_DIR, LESSONS_DIR
from lesson import Lesson
from matching import MatchingLesson
from progress_manager import load_progress, save_progress, reset_progress

from ui.menu_frame import MenuFrame
from ui.selection_frame import SelectionFrame
from ui.quiz_frame import QuizFrame
from ui.match_frame import MatchFrame

class LearnMacedonianApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- ADDED: set window icon to mk_flag.png if present ---
        icon_path = os.path.join(BASE_DIR, 'mk_flag.png')
        if os.path.exists(icon_path):
            try:
                flag_img = PhotoImage(file=icon_path)
                # iconphoto replaces the default in the title bar
                self.iconphoto(True, flag_img)
            except Exception as e:
                print(f"Warning: could not load icon '{icon_path}': {e}")

        # window title & size
        self.title('Learn Macedonian')
        self.geometry('520x600')
        self.resizable(False, False)

        # load topics & progress
        self.topics, self.base_dir = None, None
        self._load_data()

        # build frames
        self._create_frames()

    def _load_data(self):
        # list all topic folders
        self.topics = sorted(
            d for d in os.listdir(LESSONS_DIR)
            if os.path.isdir(os.path.join(LESSONS_DIR, d))
        )
        # progress.json → unlocked & per-topic state
        self.unlocked_topic, self.topic_progress = load_progress()

    def _create_frames(self):
        # Main menu: show all topics
        self.menu = MenuFrame(
            self, self.topics, self.unlocked_topic,
            on_select=self.show_lessons,
            on_save=self.manual_save,
            on_reset=self.reset_progress,
            on_exit=self.destroy
        )
        self.menu.pack()

        # Quiz & matching (hidden until needed)
        self.quiz  = QuizFrame(
            self, on_finish=self.finish_sublesson,
            on_back=self.back_to_selection
        )
        self.match = MatchFrame(
            self, on_finish=self.finish_sublesson,
            on_back=self.back_to_selection
        )

    def show_lessons(self, topic_idx):
        topic = self.topics[topic_idx]
        display = topic.split('_', 1)[1].replace('_', ' ').title()
        path = os.path.join(LESSONS_DIR, topic)
        files = sorted(f for f in os.listdir(path) if f.endswith('.csv'))

        # switch frames
        self.menu.pack_forget()
        self.selection = SelectionFrame(
            self, topic,
            files,
            on_start=lambda idx: self.start_sublesson(topic_idx, idx),
            on_back=self.back_to_menu
        )
        self.selection.pack()

        self.current_topic_idx = topic_idx
        self.sublessons = files

    def start_sublesson(self, topic_idx, sub_idx):
        topic = self.topics[topic_idx]
        filepath = os.path.join(LESSONS_DIR, topic, self.sublessons[sub_idx])
        display = topic.split('_',1)[1].replace('_',' ').title()

        # decide quiz vs matching
        if self.sublessons[sub_idx].startswith('match_'):
            match_obj = MatchingLesson(filepath)
            self.selection.pack_forget()
            self.match.start(match_obj, display, sub_idx)
        else:
            lesson_obj = Lesson(filepath)
            self.selection.pack_forget()
            self.quiz.start(lesson_obj, display, sub_idx)

    def finish_sublesson(self, sub_idx, score):
        tp = self.topic_progress.setdefault(self.topics[self.current_topic_idx], {})
        tp['completed'] = max(tp.get('completed', 0), sub_idx+1)

        # optional: still track unlocked_topic if you want
        if (tp['completed'] >= len(self.sublessons)
           and self.current_topic_idx == self.unlocked_topic):
            self.unlocked_topic += 1

        save_progress(self.unlocked_topic, self.topic_progress)
        self.show_lessons(self.current_topic_idx)

    def back_to_menu(self):
        if hasattr(self, 'selection'):
            self.selection.pack_forget()
        self.menu = MenuFrame(
            self, self.topics, self.unlocked_topic,
            on_select=self.show_lessons,
            on_save=self.manual_save,
            on_reset=self.reset_progress,
            on_exit=self.destroy
        )
        self.menu.pack()

    def back_to_selection(self):
        self.quiz.pack_forget()
        self.match.pack_forget()
        if hasattr(self, 'selection'):
            self.selection.pack()

    def manual_save(self):
        save_progress(self.unlocked_topic, self.topic_progress)
        ctk.messagebox.showinfo('Saved','Progress saved.')

    def reset_progress(self):
        if ctk.messagebox.askyesno('Reset','Reset all progress?'):
            reset_progress()
            self.unlocked_topic = 0
            self.topic_progress = {}
            self.back_to_menu()


if __name__ == '__main__':
    LearnMacedonianApp().mainloop()
