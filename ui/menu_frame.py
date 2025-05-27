import customtkinter as ctk

DISPLAY_OVERRIDES = {
    'basicverbs': 'Basic Verbs',
}

class MenuFrame(ctk.CTkFrame):
    def __init__(self, master, topics,
                 on_select, on_view_progress,
                 on_save, on_reset, on_exit):
        super().__init__(master)
        self.topics = topics
        self._on_select = on_select
        self._on_view_progress = on_view_progress
        self._on_save = on_save
        self._on_reset = on_reset
        self._on_exit = on_exit

        container = ctk.CTkFrame(self)
        container.pack(expand=True)

        ctk.CTkLabel(container, text='Choose a Topic', font=('Arial', 24, 'bold')).pack(pady=20)

        self.topic_scroll = ctk.CTkScrollableFrame(container, width=600, height=300)
        self.topic_scroll.pack(pady=10)
        self._build_topic_buttons()

        btnf = ctk.CTkFrame(container)
        btnf.pack(pady=10)

        btnf.columnconfigure((0, 1, 2), weight=1)
        ctk.CTkButton(btnf, text='View Progress', command=self._on_view_progress).grid(row=0, column=0, padx=5, pady=5)
        ctk.CTkButton(btnf, text='Save Progress', command=self._on_save).grid(row=0, column=1, padx=5, pady=5)
        ctk.CTkButton(btnf, text='Reset Progress', command=self._on_reset).grid(row=0, column=2, padx=5, pady=5)

        ctk.CTkButton(container, text='Exit', command=self._on_exit).pack(pady=(10, 0), padx=50)

    def _build_topic_buttons(self):
        for child in self.topic_scroll.winfo_children():
            child.destroy()

        for idx, topic in enumerate(self.topics):
            display = DISPLAY_OVERRIDES.get(topic, topic.replace('_', ' ').title())
            ctk.CTkButton(
                self.topic_scroll,
                text=display,
                command=lambda i=idx: self._on_select(i)
            ).pack(fill='x', pady=5, padx=10)
