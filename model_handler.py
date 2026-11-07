import numpy as np
import torch
import transformers

transformers.logging.set_verbosity_error()
from scipy.io import wavfile
from transformers import pipeline


class ModelHandler:
    """openai/whisper-tiny modelini Apple Silicon (MPS) üzerinde çalıştırır."""

    MODEL_ID = "openai/whisper-tiny"

    def __init__(self):
        if not torch.backends.mps.is_available():
            raise RuntimeError(
                "MPS (Apple Silicon) kullanılabilir değil. macOS 12.3+ ve "
                "MPS destekli bir PyTorch sürümü gerekli."
            )
        self.pipe = pipeline(
            "automatic-speech-recognition",
            model=self.MODEL_ID,
            device="mps",
        )

    def transcribe(self, audio_path: str, language: str = None) -> str:
        """language: 'turkish', 'english' veya None (otomatik algıla)."""
        # ffmpeg bağımlılığından kaçınmak için wav'ı doğrudan okuyoruz (16 kHz mono).
        sr, data = wavfile.read(audio_path)
        if data.dtype == np.int16:
            data = data.astype(np.float32) / 32768.0
        else:
            data = data.astype(np.float32)
        if data.ndim > 1:
            data = data.mean(axis=1)
        kwargs = {"task": "transcribe"}
        if language:
            kwargs["language"] = language
        result = self.pipe(
            {"raw": data, "sampling_rate": sr},
            generate_kwargs=kwargs,
        )
        return result["text"].strip()
