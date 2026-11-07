import threading

import numpy as np
import sounddevice as sd
from scipy.io import wavfile


class AudioRecorder:
    """Mikrofondan 16 kHz mono kayıt yapar; ayrı bir thread'de çalışır."""

    SAMPLE_RATE = 16000
    OUTPUT_FILE = "temp_audio.wav"

    def __init__(self):
        self._frames = []
        self._stop_event = threading.Event()
        self._thread = None
        self._error = None

    def _record(self):
        try:
            with sd.InputStream(
                samplerate=self.SAMPLE_RATE,
                channels=1,
                dtype="int16",
                callback=lambda indata, frames, t, status: self._frames.append(indata.copy()),
            ):
                self._stop_event.wait()
        except Exception as e:  # mikrofon izni/cihaz hataları
            self._error = e

    def start(self):
        if self._thread and self._thread.is_alive():
            return
        self._frames = []
        self._error = None
        self._stop_event.clear()
        self._thread = threading.Thread(target=self._record, daemon=True)
        self._thread.start()

    def stop(self):
        """Kaydı durdurur, temp_audio.wav olarak kaydeder ve yolunu döndürür."""
        self._stop_event.set()
        if self._thread:
            self._thread.join()
        if self._error:
            raise RuntimeError(f"Kayıt hatası: {self._error}")
        if not self._frames:
            raise RuntimeError("Hiç ses kaydedilmedi.")
        audio = np.concatenate(self._frames, axis=0)
        wavfile.write(self.OUTPUT_FILE, self.SAMPLE_RATE, audio)
        return self.OUTPUT_FILE
