import threading
import time
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox

import customtkinter as ctk

from ..model.video import Video
from ..services.extract_audio_service import ExtractAudioService
from ..services.generate_subtitle_service import GenerateSubtitleService
from ..services.load_video_file_service import LoadVideoFileService
from ..services.transcrib_audio_service import TranscribAudioService


def format_seconds_to_hms(total_seconds: float) -> str:
    total_seconds = int(total_seconds)

    minutes, seconds = divmod(total_seconds, 60)
    hours, minutes = divmod(minutes, 60)

    parts = []

    if hours > 0:
        parts.append(f"{hours}h")
    if minutes > 0:
        parts.append(f"{minutes}m")
    if seconds > 0 or not parts:
        parts.append(f"{seconds}s")

    return " ".join(parts) if parts else "0s"


class UI:
    def __init__(self):

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("./src/ui/themes/lavender.json")

        self.window = ctk.CTk()

        self.file_path = tk.StringVar()
        self.status = tk.StringVar(value="Aguardando arquivo...")

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

    def __show_custom_info(self, title: str, message: str):
        dialog = ctk.CTkToplevel(self.window)
        dialog.title(title)

        width = 400
        height = 200
        x = self.window.winfo_x() + (self.window.winfo_width() // 2) - (width // 2)
        y = self.window.winfo_y() + (self.window.winfo_height() // 2) - (height // 2)
        dialog.geometry(f"{width}x{height}+{x}+{y}")

        dialog.transient(self.window)
        dialog.update_idletasks()
        dialog.grab_set()

        label = ctk.CTkLabel(
            dialog, text=message, font=ctk.CTkFont(size=14), wraplength=width - 40
        )
        label.pack(pady=20, padx=20, expand=True, fill="both")

        button = ctk.CTkButton(
            dialog, text="OK", command=dialog.destroy, width=100, cursor="hand2"
        )
        button.pack(pady=(0, 20))

        dialog.wait_window()

    def __process_subtitle(self, path: str):
        start_total_time = time.perf_counter()

        print("whisper model", self.whisper_model.get())

        self.status.set("Carregando arquivo de video...")
        self.video = LoadVideoFileService().execute(path)
        self.status.set("Video carregado com sucesso!")

        self.status.set("Extraindo audio do video...")
        start_extract_time = time.perf_counter()
        self.audio = ExtractAudioService.execute(self.video)
        end_extract_time = time.perf_counter()
        self.status.set("Audio extraido com sucesso!")

        self.status.set("Gerando transcrição...")
        start_transcribe_time = time.perf_counter()
        self.transcription = TranscribAudioService.execute(
            self.audio, self.whisper_model.get()
        )
        end_transcribe_time = time.perf_counter()
        self.status.set("Transcrição gerada com sucesso!")

        GenerateSubtitleService().execute(
            video=self.video,
            transcript=self.transcription,
            subtitle_path=self.output_path.get(),
        )

        self.status.set("Legenda gerada com sucesso!")
        end_total_time = time.perf_counter()

        extract_time = end_extract_time - start_extract_time
        transcribe_time = end_transcribe_time - start_transcribe_time
        total_time = end_total_time - start_total_time
        rtf = transcribe_time / self.video.duration if self.video.duration > 0 else 0
        # minutes, seconds = divmod(self.video.duration, 60)
        # formated_duration = f"{int(minutes)}m {int(seconds)}s"

        # metrics_summary = {
        #     'duration': formated_duration,
        #     ''
        # }

        metrics_summary = (
            f"Legenda gerada com sucesso!\n\n"
            f"Duração do Vídeo: {format_seconds_to_hms(self.video.duration)}\n"
            f"Tempo de Extração: {format_seconds_to_hms(extract_time)}\n"
            f"Tempo de Transcrição: {format_seconds_to_hms(transcribe_time)}\n"
            f"Tempo Total: {format_seconds_to_hms(total_time)}\n"
            f"Real-Time Factor (RTF): {rtf:.2f}"
        )

        # messagebox.showinfo("Sucesso", metrics_summary)
        self.__show_custom_info("Sucesso", metrics_summary)

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
            self.__show_custom_info(
                "Aviso", "⚠️ Por favor, selecione um arquivo de vídeo primeiro."
            )
            return

        self.status.set("Processando...")

        thread = threading.Thread(
            target=self.__process_subtitle, args=(self.file_path.get(),)
        )
        thread.start()

    def update(self):

        frame = ctk.CTkFrame(self.window, corner_radius=10)
        frame.pack(pady=20)

        title_input_label = ctk.CTkLabel(frame, text="Configurações de Entrada")
        title_input_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        input = ctk.CTkEntry(
            master=frame,
            textvariable=self.file_path,
            corner_radius=8,
            width=350,
            height=30,
        )
        input.grid(row=1, column=0, padx=5, pady=5, sticky="w")

        file_button = ctk.CTkButton(
            frame,
            text="Selecionar Arquivo",
            command=self.select_file,
            height=30,
            cursor="hand2",
        )
        file_button.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        model_frame = ctk.CTkFrame(frame, corner_radius=10)
        model_frame.grid(row=2, column=0, pady=10, padx=5, columnspan=2, sticky="w")

        title_model_label = ctk.CTkLabel(
            model_frame, text="Configuração do Whisper Model"
        )
        title_model_label.pack(padx=10)

        model_label = ctk.CTkLabel(model_frame, text="Modelo:")
        model_label.pack(side=tk.LEFT, padx=10)  # Espaço só do label para o combo

        model_select = ctk.CTkOptionMenu(
            model_frame,
            values=self.models,
            width=100,
            state="readonly",
            cursor="hand2",
        )
        model_select.pack(side=tk.LEFT, pady=10)
        model_select.set("base")

        output_frame = ctk.CTkFrame(self.window, corner_radius=10)
        output_frame.pack(pady=20)

        title_output_label = ctk.CTkLabel(output_frame, text="Configurações de Saída")
        title_output_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        output_path = ctk.CTkEntry(
            output_frame,
            textvariable=self.output_path,
            width=350,
            height=30,
            corner_radius=8,
        )
        output_path.grid(row=1, column=0, padx=5, pady=5, sticky="w")

        output_button = ctk.CTkButton(
            output_frame,
            text="Selecionar Destino",
            command=self.select_output_path,
            height=30,
            cursor="hand2",
        )
        output_button.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        process_button = ctk.CTkButton(
            master=self.window,
            text="Gerar Legenda",
            command=self.generate_subtitle,
            height=30,
            cursor="hand2",
        )
        process_button.pack(pady=10)

        status_frame = ctk.CTkFrame(self.window, corner_radius=10)
        status_frame.pack(pady=20, padx=20)

        status_label = ctk.CTkLabel(status_frame, text="Status: ")
        status_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        status_text = ctk.CTkLabel(status_frame, textvariable=self.status)
        status_text.grid(row=0, column=1, padx=5, pady=5, sticky="w")

    def run(self):
        self.update()
        self.window.mainloop()
