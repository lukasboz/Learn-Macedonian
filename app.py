# FILE: app.py

import os
import re
import customtkinter as ctk
from tkinter import PhotoImage

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

        # Set a larger 16:9 window (1024×576)
        base_width  = 1024
        base_height = int(base_width * 11 / 16)  # → 576
        self.geometry(f"{base_width}x{base_height}")
        self.resizable(False, False)

        # Load window icon (must be .ico on Windows)
        ico_path = os.path.join(BASE_DIR, 'mk_flag.ico')
        if os.path.exists(ico_path):
            try:
                self.iconbitmap(ico_path)
            except Exception as e:
                print(f"Warning loading icon: {e}")

        self.title('Learn Macedonian')

        # load topics & progress
        self._load_data()
        # build UI frames
        self._create_frames()

    def _load_data(self):
        self.topics = sorted(
            d for d in os.listdir(LESSONS_DIR)
            if os.path.isdir(os.path.join(LESSONS_DIR, d))
        )
        # We still track progress in JSON
        self.unlocked_topic, self.topic_progress = load_progress()

    def _create_frames(self):
        self.menu = MenuFrame(
            self,
            self.topics,
            on_select=self.show_lessons,
            on_view_progress=self.view_progress,
            on_save=self.manual_save,
            on_reset=self.reset_progress,
            on_exit=self.destroy
        )
        self.menu.pack(fill='both', expand=True)

        self.quiz  = QuizFrame(
            self, on_finish=self.finish_sublesson,
            on_back=self.back_to_selection
        )
        self.match = MatchFrame(
            self, on_finish=self.finish_sublesson,
            on_back=self.back_to_selection
        )

    def _show_popup(self, title, message):
        """Custom CTk popup to avoid system sound."""
        dlg = ctk.CTkToplevel(self)
        dlg.title(title)
        dlg.geometry("400x300")
        dlg.resizable(False, False)
        dlg.transient(self)
        dlg.grab_set()

        lbl = ctk.CTkLabel(
            dlg,
            text=message,
            justify="left",
            anchor="nw",
            wraplength=380
        )
        lbl.pack(padx=20, pady=(20,10), fill="both", expand=True)

        btn = ctk.CTkButton(
            dlg,
            text="OK",
            command=dlg.destroy
        )
        btn.pack(pady=(0,20))

    def view_progress(self):
        """Show progress via a CTk popup instead of messagebox beep."""
        lines = []
        for topic in self.topics:
            raw = re.sub(r'^\d+_?', '', topic)
            display = raw.replace('_', ' ').title()
            path = os.path.join(LESSONS_DIR, topic)
            total = len([f for f in os.listdir(path) if f.endswith('.csv')])
            completed = self.topic_progress.get(topic, {}).get('completed', 0)
            lines.append(f"{display}: {completed}/{total} completed")

        self._show_popup("Your Progress", "\n".join(lines))

    def show_lessons(self, topic_idx):
        topic = self.topics[topic_idx]
        path  = os.path.join(LESSONS_DIR, topic)
        files = sorted(f for f in os.listdir(path) if f.endswith('.csv'))

        self.menu.pack_forget()
        self.selection = SelectionFrame(
            self, topic, files,
            on_start=lambda idx: self.start_sublesson(topic_idx, idx),
            on_back=self.back_to_menu
        )
        self.selection.pack(fill='both', expand=True)

        self.current_topic_idx = topic_idx
        self.sublessons = files

    def start_sublesson(self, topic_idx, sub_idx):
        topic = self.topics[topic_idx]
        fn    = self.sublessons[sub_idx]
        full  = os.path.join(LESSONS_DIR, topic, fn)
        display = re.sub(r'^\d+_?', '', topic).replace('_',' ').title()

        self.selection.pack_forget()
        if fn.startswith('match_'):
            self.match.start(MatchingLesson(full), display, sub_idx)
        else:
            self.quiz.start(Lesson(full), display, sub_idx)

    def finish_sublesson(self, sub_idx, score):
        tp = self.topic_progress.setdefault(self.topics[self.current_topic_idx], {})
        tp['completed'] = max(tp.get('completed', 0), sub_idx+1)
        save_progress(self.unlocked_topic, self.topic_progress)
        self.show_lessons(self.current_topic_idx)

    def back_to_menu(self):
        if hasattr(self, 'selection'):
            self.selection.pack_forget()
        self.menu.pack(fill='both', expand=True)

    def back_to_selection(self):
        self.quiz.pack_forget()
        self.match.pack_forget()
        if hasattr(self, 'selection'):
            self.selection.pack(fill='both', expand=True)

    def manual_save(self):
        save_progress(self.unlocked_topic, self.topic_progress)
        # use our silent popup
        self._show_popup("Saved", "Progress saved.")

    def reset_progress(self):
        if ctk.messagebox.askyesno('Reset','Reset all progress?'):
            reset_progress()
            self.topic_progress.clear()
            self.menu.pack(fill='both', expand=True)


if __name__ == '__main__':
    LearnMacedonianApp().mainloop()
