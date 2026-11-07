# LocalWhisperAi

Apple Silicon (M1/M2/M3) için tamamen yerel çalışan sesli asistan masaüstü uygulaması.
Hugging Face [`openai/whisper-tiny`](https://huggingface.co/openai/whisper-tiny) modelini MPS (Metal) hızlandırmasıyla çalıştırır. Türkçe ve İngilizce desteklenir; ses cihazınızdan çıkmaz.

## Özellikler
- Tek tuşla kayıt başlat/durdur (16 kHz, ayrı thread, arayüz donmaz)
- Dil seçimi: Otomatik / Türkçe / English
- Koyu temalı CustomTkinter arayüzü
- İnternet sadece ilk açılışta modeli indirmek için gerekir

## Gereksinimler
- Apple Silicon Mac, macOS 12.3+
- Python 3.10+

## Kaynaktan çalıştırma
```bash
git clone https://github.com/<kullanici-adi>/LocalWhisperAi.git
cd LocalWhisperAi
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python main.py
```

## .app olarak derleme
```bash
./build_app.sh
open dist/LocalWhisper.app
```
Betik PyInstaller ile `--onedir --windowed` uygulama üretir, mikrofon izni açıklamasını ekler ve ad-hoc imzalar.

> Uygulama Apple Developer ile imzalı/notarize edilmediği için başka bir Mac'te ilk açılışta
> **sağ tık → Aç** demeniz gerekebilir. Model ilk açılışta indirilir (~150 MB).

## Dosyalar
| Dosya | Görev |
|---|---|
| `main.py` | Arayüz |
| `model_handler.py` | Whisper modeli (MPS) |
| `audio_recorder.py` | Mikrofon kaydı |
| `build_app.sh` | `.app` derleme betiği |

## Lisans
MIT
