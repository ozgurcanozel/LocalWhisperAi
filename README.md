# 🎙️ LocalWhisperAi

Apple Silicon Mac'ler için **tamamen yerel** çalışan sesli asistan / konuşma-metin uygulaması.
Hugging Face [`openai/whisper-tiny`](https://huggingface.co/openai/whisper-tiny) modelini **MPS (Metal)** hızlandırmasıyla çalıştırır. Sesiniz cihazınızdan çıkmaz.

![Platform](https://img.shields.io/badge/platform-macOS%20(Apple%20Silicon)-black)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

## ✨ Özellikler

- 🔴 Tek tuşla kayıt başlat / durdur (16 kHz, ayrı thread, arayüz donmaz)
- 🌍 Dil seçimi: **Otomatik / Türkçe / English**
- 🌙 Modern, koyu temalı arayüz (CustomTkinter)
- ⚡ Apple Silicon GPU (MPS) ile hızlı çeviri
- 🔒 %100 yerel: kayıtlar ve metinler internete gönderilmez

## 📥 Hızlı Kurulum (Önerilen): Hazır Uygulamayı İndir

Python veya terminal bilgisi gerekmez.

1. [**Releases**](../../releases/latest) sayfasına gidin.
2. `LocalWhisper-macOS-arm64.zip` dosyasını indirip açın.
3. `LocalWhisper.app` dosyasını **Uygulamalar** klasörüne taşıyın.
4. **İlk açılışta:** uygulamaya **sağ tık → Aç** deyin ve çıkan uyarıda tekrar **Aç**'a basın.
   (Uygulama Apple tarafından imzalanmadığı için macOS bir kez uyarı verir.)
5. Mikrofon izni istendiğinde **İzin Ver**'e basın.

> [!NOTE]
> - Sadece **Apple Silicon (M1/M2/M3/M4)** Mac'lerde çalışır, Intel Mac'lerde çalışmaz.
> - **İlk açılışta model (~150 MB) internetten indirilir**, bu yüzden internet bağlantısı gerekir. Sonrasında çevrimdışı çalışır.
> - Uygulama ~700 MB yer kaplar.

Uygulama "hasarlı" diyerek açılmazsa Terminal'de şunu çalıştırın:
```bash
xattr -cr /Applications/LocalWhisper.app
```

## 🧑‍💻 Kaynaktan Çalıştırma

Gereksinimler: Apple Silicon Mac, macOS 12.3+, Python 3.10+

```bash
git clone https://github.com/<kullanici-adi>/LocalWhisperAi.git
cd LocalWhisperAi
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python main.py
```

## 🛠️ Kendi `.app` Dosyanızı Derleme

```bash
./build_app.sh
open dist/LocalWhisper.app
```

Betik PyInstaller ile `--onedir --windowed` uygulama üretir, mikrofon izni açıklamasını ekler ve ad-hoc imzalar.

## 🎯 Kullanım

1. Buton **"🎙 Kaydı Başlat"** olana kadar bekleyin (model yükleniyor).
2. İsterseniz dili seçin: Otomatik, Türkçe veya English.
3. Butona basıp konuşun. Buton kırmızıya döner.
4. Tekrar basınca kayıt durur ve metin alttaki kutuya yazılır.

## 📁 Proje Yapısı

| Dosya | Görev |
|---|---|
| `main.py` | Arayüz (CustomTkinter) |
| `model_handler.py` | Whisper modeli (MPS) |
| `audio_recorder.py` | Mikrofon kaydı |
| `build_app.sh` | `.app` derleme betiği |
| `requirements.txt` | Python bağımlılıkları |

## ❓ Sık Karşılaşılan Sorunlar

| Sorun | Çözüm |
|---|---|
| Ses kaydedilmiyor | Sistem Ayarları → Gizlilik ve Güvenlik → Mikrofon'dan uygulamaya izin verin |
| Uygulama açılmıyor | Sağ tık → Aç, ya da `xattr -cr` komutunu kullanın |
| Türkçe sonuç zayıf | Dili menüden "Türkçe" yapın; `model_handler.py` içinde `whisper-small` modelini deneyin |
| İlk açılış yavaş | Model indiriliyor, bir kez olur |

## 🤝 Katkıda Bulunma

Pull request ve issue'lar açıktır.

## 📄 Lisans

[MIT](LICENSE)
