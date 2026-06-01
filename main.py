import customtkinter as ctk
import downloader

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("580x480")
        self.resizable(False, False)
        self.title("ytbLinks2Mp3")
        self.configure(fg_color="#1A1A1A")
        self.grid_columnconfigure(0, weight=1)

        # title
        self.label_title = ctk.CTkLabel(
            self, text="ytbLinks2Mp3",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color="#FFFFFF"
        )
        self.label_title.grid(row=0, column=0, pady=(40, 4), padx=90, sticky="w")

        self.label_sub = ctk.CTkLabel(
            self, text="YouTube to MP3 converter",
            font=ctk.CTkFont(size=12),
            text_color="#555555"
        )
        self.label_sub.grid(row=1, column=0, pady=(0, 35), padx=90, sticky="w")

        # url input
        self.entry_url = ctk.CTkEntry(
            self, placeholder_text="YouTube link",
            width=400, height=40,
            fg_color="#242424",
            border_color="#333333",
            border_width=1,
            corner_radius=6,
            text_color="#FFFFFF",
            placeholder_text_color="#555555"
        )
        self.entry_url.grid(row=2, column=0, pady=(0, 12))

        # output name input
        self.entry_name = ctk.CTkEntry(
            self, placeholder_text="Output name (optional)",
            width=400, height=40,
            fg_color="#242424",
            border_color="#333333",
            border_width=1,
            corner_radius=6,
            text_color="#FFFFFF",
            placeholder_text_color="#555555"
        )
        self.entry_name.grid(row=3, column=0, pady=(0, 20))

        # convert button
        self.button = ctk.CTkButton(
            self, text="Convert", width=400, height=40,
            fg_color="#2E2E2E",
            hover_color="#3A3A3A",
            text_color="#FFFFFF",
            font=ctk.CTkFont(size=13),
            corner_radius=6,
            command=self.button_click
        )
        self.button.grid(row=4, column=0, pady=(0, 20))

        # status
        self.label_status = ctk.CTkLabel(
            self, text="",
            font=ctk.CTkFont(size=12),
            text_color="#555555"
        )
        self.label_status.grid(row=5, column=0, pady=(0, 8))

        # progress bar
        self.progressbar = ctk.CTkProgressBar(
            self, width=400,
            fg_color="#242424",
            progress_color="#FFFFFF",
            corner_radius=2,
            height=3
        )
        self.progressbar.set(0)
        self.progressbar.grid(row=6, column=0)

    def button_click(self):
        url = self.entry_url.get()
        output_name = self.entry_name.get()

        if not url:
            self.label_status.configure(text="Please insert a YouTube link", text_color="#CC4444")
            return

        self.button.configure(state="disabled")
        self.label_status.configure(text="Downloading...", text_color="#555555")
        self.progressbar.set(0)

        downloader.download(
            url=url,
            output_name=output_name,
            on_progress=self.on_progress,
            on_finish=self.on_finish
        )

    def on_progress(self, percent):
        self.progressbar.set(percent / 100)
        self.label_status.configure(text=f"Downloading...  {int(percent)}%", text_color="#555555")

    def on_finish(self):
        self.progressbar.set(1)
        self.label_status.configure(text="Done", text_color="#FFFFFF")
        self.button.configure(state="normal")

app = App()
app.mainloop()