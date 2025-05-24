import threading
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

import customtkinter as ctk

from ..model.video import Video
from ..services.extract_audio_service import ExtractAudioService
from ..services.generate_subtitle_service import GenerateSubtitleService
from ..services.load_video_file_service import LoadVideoFileService
from ..services.transcrib_audio_service import TranscribAudioService


class UI:
    def __init__(self):

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        self.window = tk.Tk()

        self.file_path = tk.StringVar()
        self.status = tk.StringVar(value="Aguardado arquivo...")

        self.video: Video = None
        self.audio = None
        self.transcription = None

        self.whisper_model = tk.StringVar(value="base")
        self.models = ["tiny", "base", "small", "medium", "large", "turbo"]

        # Define o destino padrão como a pasta de Downloads
        self.output_path = tk.StringVar(value=str(Path.home() / "Downloads"))

        self.window.title("EchoSub")

        width = 600
        height = 500

        largura_tela = self.window.winfo_screenwidth()
        altura_tela = self.window.winfo_screenheight()

        # Calcula posição X e Y para centralizar
        x = (largura_tela // 2) - (width // 2)
        y = (altura_tela // 2) - (height // 2)

        # Define o tamanho + posição
        self.window.geometry(f"{width}x{height}+{x}+{y}")

    def __precess_subtitle(self, path: str):
        print("whisper model", self.whisper_model.get())

        self.status.set("Carregando arquivo de video...")
        self.video = LoadVideoFileService().execute(path)
        self.status.set("Video carregado com sucesso!")

        self.status.set("Extraindo audio do video...")
        self.audio = ExtractAudioService.execute(self.video)
        self.status.set("Audio extraido com sucesso!")

        self.status.set("Gerando transcrição...")
        self.transcription = TranscribAudioService.execute(
            self.audio, self.whisper_model.get()
        )
        self.status.set("Transcrição gerada com sucesso!")

        GenerateSubtitleService().execute(
            video=self.video,
            transcript=self.transcription,
            subtitle_path=self.output_path.get(),
        )

        self.status.set("Legenda gerada com sucesso!")
        messagebox.showinfo("Sucesso", "Legenda gerada com sucesso!")

    def select_file(self):
        path = filedialog.askopenfilename(
            title="Selecione um arquivo de vídeo",
            filetypes=[
                ("Arquivos de vídeo", "*.mp4 *.avi *.mkv *.mov"),
                ("Todos os arquivos", "*.*"),
            ],
        )

        if path:
            self.file_path.set(path)
            print("Path", path)

    def select_output_path(self):
        path = filedialog.askdirectory(title="Selecione a pasta de destino da legenda")

        if path:
            self.output_path.set(path)
            print("Output path", path)

    def generate_subtitle(self):
        path = self.file_path.get()

        if not path:
            messagebox.showwarning(
                "Aviso", "Por favor, selecione um arquivo de vídeo primeiro."
            )
            return

        self.status.set("Processando...")

        thread = threading.Thread(
            target=self.__precess_subtitle, args=(self.file_path.get(),)
        )
        thread.start()

    def update(self):
        frame = tk.LabelFrame(
            self.window,
            text="Configurações de Entrada",
            padx=10,
            pady=10,
            relief="groove",
            bd=2,
        )
        frame.pack(pady=20)

        input = tk.Entry(frame, textvariable=self.file_path, width=40)
        input.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        file_button = tk.Button(
            frame, text="Selecionar Arquivo", command=self.select_file
        )
        file_button.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        model_frame = tk.LabelFrame(
            frame,
            text="Configurações do Modelo",
            padx=10,
            pady=10,
            relief="groove",
            bd=2,
        )
        model_frame.grid(row=1, column=0, columnspan=2, sticky="w")

        model_label = tk.Label(model_frame, text="Modelo:")
        model_label.pack(side=tk.LEFT, padx=(0, 5))  # Espaço só do label para o combo

        model_select = ttk.Combobox(
            model_frame,
            textvariable=self.whisper_model,
            values=self.models,
            width=10,
            state="readonly",
        )
        model_select.pack(side=tk.LEFT)
        model_select.current(1)

        output_frame = tk.LabelFrame(
            self.window,
            text="Configurações de Saída",
            padx=10,
            pady=10,
            relief="groove",
            bd=2,
        )
        output_frame.pack(pady=20)

        output_path = tk.Entry(output_frame, textvariable=self.output_path, width=40)
        output_path.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        output_button = tk.Button(
            output_frame, text="Selecionar Destino", command=self.select_output_path
        )
        output_button.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        process_button = tk.Button(
            self.window, text="Gerar Legenda", command=self.generate_subtitle
        )
        process_button.pack(pady=10)

        status_frame = tk.LabelFrame(
            self.window, text="Logs", padx=10, pady=10, relief="groove", bd=2
        )
        status_frame.pack(pady=20)

        status_label = tk.Label(status_frame, text="Status: ")
        status_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        status_text = tk.Label(status_frame, textvariable=self.status)
        status_text.grid(row=0, column=1, padx=5, pady=5, sticky="w")

    def run(self):
        self.update()
        self.window.mainloop()
