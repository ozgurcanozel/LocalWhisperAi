import threading

import customtkinter as ctk

from audio_recorder import AudioRecorder
from model_handler import ModelHandler

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Local Whisper Sesli Asistan")
        self.geometry("700x560")

        self.recorder = AudioRecorder()
        self.model = None
        self.recording = False
        self.busy = True

        self.button = ctk.CTkButton(
            self, text="Model yükleniyor...", height=70, width=280,
            font=ctk.CTkFont(size=22, weight="bold"), corner_radius=35,
            state="disabled", command=self.toggle,
        )
        self.button.pack(pady=(40, 10))

        self.status = ctk.CTkLabel(self, text="Lütfen bekleyin", text_color="gray")
        self.status.pack(pady=(0, 15))

        self.lang_var = ctk.StringVar(value="Otomatik")
        self.lang_menu = ctk.CTkOptionMenu(
            self, values=["Otomatik", "Türkçe", "English"], variable=self.lang_var)
        self.lang_menu.pack(pady=(0, 15))

        self.textbox = ctk.CTkTextbox(self, font=ctk.CTkFont(size=16), wrap="word", corner_radius=12)
        self.textbox.pack(fill="both", expand=True, padx=30, pady=(0, 30))

        threading.Thread(target=self._load_model, daemon=True).start()

    def _load_model(self):
        try:
            self.model = ModelHandler()
            self.after(0, self._set_idle, "Hazır")
        except Exception as e:
            self.after(0, self._show_error, f"Model yüklenemedi: {e}")

    def _set_idle(self, msg="Hazır"):
        self.busy = False
        self.button.configure(text="🎙  Kaydı Başlat", fg_color="#1f6aa5",
                              hover_color="#144870", state="normal")
        self.status.configure(text=msg)

    def _show_error(self, msg):
        self.status.configure(text=msg, text_color="#ff6b6b")
        self.button.configure(text="Hata", state="disabled")

    def toggle(self):
        if self.busy:
            return
        if not self.recording:
            self.recorder.start()
            self.recording = True
            self.button.configure(text="⏹  Kaydı Durdur", fg_color="#c0392b", hover_color="#922b21")
            self.status.configure(text="Kayıt yapılıyor...", text_color="#ff6b6b")
        else:
            self.recording = False
            self.busy = True
            self.button.configure(text="Çevriliyor...", state="disabled", fg_color="gray")
            self.status.configure(text="Metne çevriliyor...", text_color="gray")
            lang = {"Türkçe": "turkish", "English": "english"}.get(self.lang_var.get())
            threading.Thread(target=self._process, args=(lang,), daemon=True).start()

    def _process(self, lang):
        try:
            path = self.recorder.stop()
            text = self.model.transcribe(path, language=lang)
            self.after(0, self._show_text, text)
        except Exception as e:
            self.after(0, self._set_idle, f"Hata: {e}")

    def _show_text(self, text):
        self.textbox.insert("end", (text or "(ses algılanamadı)") + "\n\n")
        self.textbox.see("end")
        self.status.configure(text_color="gray")
        self._set_idle("Hazır")


if __name__ == "__main__":
    App().mainloop()
