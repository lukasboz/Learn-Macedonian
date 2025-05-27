# FILE: ui/sentence_builder_frame.py

import random
import customtkinter as ctk
import tkinter.messagebox as mb

class SentenceBuilderFrame(ctk.CTkFrame):
    def __init__(self, master, on_finish, on_back):
        super().__init__(master)
        self.on_finish = on_finish
        self.on_back   = on_back

        # English or Macedonian prompt
        self.prompt_label = ctk.CTkLabel(self, font=('Arial', 18, 'bold'))
        self.prompt_label.pack(pady=(10,5))

        # Build area
        self.build_frame = ctk.CTkFrame(self)
        self.build_frame.pack(pady=10)

        # Controls
        ctrl = ctk.CTkFrame(self)
        ctrl.pack(pady=5)
        self.remove_btn = ctk.CTkButton(ctrl, text='Remove Last', command=self.remove_block)
        self.remove_btn.grid(row=0, column=0, padx=8)
        self.submit_btn = ctk.CTkButton(ctrl, text='Submit',       command=self.check_answer)
        self.submit_btn.grid(row=0, column=1, padx=8)
        self.back_btn   = ctk.CTkButton(ctrl, text='Back',         command=self._handle_back)
        self.back_btn.grid(row=0, column=2, padx=8)

        # Block pool
        self.pool_frame = ctk.CTkFrame(self)
        self.pool_frame.pack(pady=(10,20))

        # State
        self.lesson    = None
        self.idx       = 0
        self.built     = []
        self.block_buttons = []
        self.direction = 'en->mk'  # or 'mk->en'

    def start(self, lesson_obj, topic_display, sub_idx, direction):
        """Initialize with a SentenceBuilderLesson and direction."""
        self.lesson    = lesson_obj
        self.idx       = 0
        self.direction = direction  # 'en->mk' or 'mk->en'
        self.built.clear()
        self._show_sentence()
        self.pack(fill='both', expand=True)

    def _handle_back(self):
        self.pack_forget()
        self.on_back()

    def _show_sentence(self):
        eng, mac, mk_blocks, en_blocks = self.lesson.items[self.idx]

        # choose prompt & blocks based on direction
        if self.direction == 'en->mk':
            prompt = eng
            blocks = mk_blocks
        else:
            prompt = mac
            blocks = en_blocks

        self.prompt_label.configure(text=prompt)

        # clear build area
        for w in self.build_frame.winfo_children():
            w.destroy()
        self.built.clear()

        # clear pool
        for b in self.block_buttons:
            b.destroy()
        self.block_buttons.clear()

        # shuffle and display pool
        pool = list(blocks)
        random.shuffle(pool)
        for txt in pool:
            btn = ctk.CTkButton(
                self.pool_frame,
                text=txt,
                width=120,
                command=lambda t=txt: self._add_block(t)
            )
            btn.pack(side='left', padx=5, pady=5)
            self.block_buttons.append(btn)

    def _add_block(self, txt):
        self.built.append(txt)
        ctk.CTkLabel(self.build_frame, text=txt, font=('Arial',14), fg_color='gray80')\
            .pack(side='left', padx=3)
        # disable pool button
        for btn in self.block_buttons:
            if btn.cget('text') == txt and btn.cget('state') != 'disabled':
                btn.configure(state='disabled')
                break

    def remove_block(self):
        if not self.built:
            return
        last = self.built.pop()
        # re-enable its button
        for btn in self.block_buttons:
            if btn.cget('text') == last and btn.cget('state') == 'disabled':
                btn.configure(state='normal')
                break
        # remove last label
        children = self.build_frame.winfo_children()
        if children:
            children[-1].destroy()

    def check_answer(self):
        eng, mac, _, _ = self.lesson.items[self.idx]
        guess = ' '.join(self.built)

        # determine correct target
        correct = mac if self.direction == 'en->mk' else eng

        if guess == correct:
            mb.showinfo('Correct', 'Well done!')
            self.idx += 1
            if self.idx < self.lesson.total:
                self._show_sentence()
            else:
                self.on_finish(self.idx-1, None)
                self.pack_forget()
        else:
            mb.showerror(
                'Incorrect',
                f'Your answer:\n"{guess}"\ndoes not match:\n"{correct}"'
            )
