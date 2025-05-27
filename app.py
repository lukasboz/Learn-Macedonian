import os
from tkinter import PhotoImage
import customtkinter as ctk
import tkinter.messagebox as mb

from constants import BASE_DIR, LESSONS_DIR
from lesson import Lesson
from matching import MatchingLesson
from sentence_builder import SentenceBuilderLesson
from progress_manager import load_progress, save_progress, reset_progress

from ui.menu_frame import MenuFrame
from ui.selection_frame import SelectionFrame
from ui.quiz_frame import QuizFrame
from ui.match_frame import MatchFrame
from ui.sentence_builder_frame import SentenceBuilderFrame

class LearnMacedonianApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        icon_path = os.path.join(BASE_DIR, 'mk_flag.png')
        if os.path.exists(icon_path):
            try:
                flag_img = PhotoImage(file=icon_path)
                self.iconphoto(True, flag_img)
            except Exception:
                pass

        # Set window size and center it
        self.title('Learn Macedonian')
        self.geometry('960x540')
        self.resizable(False, False)
        self.update_idletasks()
        width = 960
        height = 540
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')

        self._load_data()
        self._create_frames()

    def _load_data(self):
        self.topics = sorted(
            d for d in os.listdir(LESSONS_DIR)
            if os.path.isdir(os.path.join(LESSONS_DIR, d))
        )
        self.unlocked_topic, self.topic_progress = load_progress()

    def _create_frames(self):
        # Initialize menu without filling entire window
        self.menu = MenuFrame(
            master=self,
            topics=self.topics,
            on_select=self.show_lessons,
            on_view_progress=self.view_progress,
            on_save=self.manual_save,
            on_reset=self.reset_progress,
            on_exit=self.destroy
        )
        # Pack menu with padding and center it
        self.menu.pack(padx=50, pady=50)

        # Prepare other frames
        self.quiz = QuizFrame(master=self, on_finish=self.finish_sublesson, on_back=self.back_to_selection)
        self.match = MatchFrame(master=self, on_finish=self.finish_sublesson, on_back=self.back_to_selection)
        self.sentence_builder = SentenceBuilderFrame(
            master=self, on_finish=self.finish_sublesson, on_back=self.back_to_selection
        )

    def view_progress(self):
        lines = []
        for topic, data in self.topic_progress.items():
            name = topic.split('_', 1)[1].replace('_', ' ').title()
            completed = data.get('completed', 0)
            path = os.path.join(LESSONS_DIR, topic)
            total = len([f for f in os.listdir(path) if f.endswith('.csv')])
            lines.append(f"{name}: {completed}/{total}")
        msg = "\n".join(lines) if lines else "No progress to show yet."

        popup = ctk.CTkToplevel(self)
        popup.title("Your Progress")
        popup.geometry("320x200")
        popup.resizable(False, False)

        ctk.CTkLabel(popup, text="Your Progress", font=('Arial', 16, 'bold')).pack(pady=(10, 5))
        ctk.CTkLabel(
            popup,
            text=msg,
            font=('Arial', 12),
            justify='left',
            wraplength=300
        ).pack(padx=10, pady=(0, 10))
        ctk.CTkButton(popup, text="OK", command=popup.destroy).pack(pady=(0, 10))

    def show_lessons(self, topic_idx):
        topic = self.topics[topic_idx]
        display = topic.split('_', 1)[1].replace('_', ' ').title()
        path = os.path.join(LESSONS_DIR, topic)
        files = sorted(f for f in os.listdir(path) if f.endswith('.csv'))

        self.menu.pack_forget()
        self.selection = SelectionFrame(
            self, topic, files,
            lambda idx: self.start_sublesson(topic_idx, idx),
            self.back_to_menu
        )
        self.selection.pack(fill='both', expand=True)

        self.current_topic_idx = topic_idx
        self.sublessons = files

    def start_sublesson(self, topic_idx, sub_idx):
        topic = self.topics[topic_idx]
        display = topic.split('_', 1)[1].replace('_', ' ').title()
        fn = self.sublessons[sub_idx]
        filepath = os.path.join(LESSONS_DIR, topic, fn)

        if fn.startswith('match_'):
            obj = MatchingLesson(filepath)
            self.selection.pack_forget()
            self.match.start(obj, display, sub_idx)
            return

        if fn.startswith('sentence_'):
            parts = fn[:-4].split('_')
            if len(parts) >= 4 and parts[-2] in ('en', 'mk') and parts[-1] in ('en', 'mk'):
                direction = f"{parts[-2]}->{parts[-1]}"
            else:
                direction = 'en->mk'
            obj = SentenceBuilderLesson(filepath)
            self.selection.pack_forget()
            self.sentence_builder.start(obj, display, sub_idx, direction)
            return

        obj = Lesson(filepath)
        self.selection.pack_forget()
        self.quiz.start(obj, display, sub_idx)

    def finish_sublesson(self, sub_idx, score):
        tp = self.topic_progress.setdefault(self.topics[self.current_topic_idx], {})
        tp['completed'] = max(tp.get('completed', 0), sub_idx + 1)
        if tp['completed'] >= len(self.sublessons) and self.current_topic_idx == self.unlocked_topic:
            self.unlocked_topic += 1
        save_progress(self.unlocked_topic, self.topic_progress)
        self.show_lessons(self.current_topic_idx)

    def back_to_menu(self):
        if hasattr(self, 'selection'):
            self.selection.pack_forget()
        # Re-pack menu with padding
        self.menu.pack(padx=50, pady=50)

    def back_to_selection(self):
        self.quiz.pack_forget()
        self.match.pack_forget()
        self.sentence_builder.pack_forget()
        if hasattr(self, 'selection'):
            self.selection.pack(fill='both', expand=True)

    def manual_save(self):
        save_progress(self.unlocked_topic, self.topic_progress)
        mb.showinfo('Saved', 'Progress saved.')

    def reset_progress(self):
        if mb.askyesno('Reset', 'Reset all progress?'):
            reset_progress()
            self.unlocked_topic = 0
            self.topic_progress = {}
            self.back_to_menu()

if __name__ == '__main__':
    LearnMacedonianApp().mainloop()
