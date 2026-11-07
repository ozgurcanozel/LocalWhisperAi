#!/bin/bash
# LocalWhisper .app oluşturur (PyInstaller, --onedir --windowed).
set -e
cd "$(dirname "$0")"

PY=".venv/bin/python"
[ -x "$PY" ] || PY="python3"

$PY -m pip install pyinstaller

$PY -m PyInstaller main.py \
  --name LocalWhisper \
  --onedir --windowed --noconfirm --clean \
  --osx-bundle-identifier com.localwhisper.app \
  --collect-all customtkinter \
  --collect-all transformers \
  --collect-all tokenizers \
  --collect-all sounddevice \
  --collect-binaries torch \
  --hidden-import scipy.io.wavfile

APP="dist/LocalWhisper.app"

# macOS mikrofon izni için gerekli açıklama
/usr/libexec/PlistBuddy -c "Add :NSMicrophoneUsageDescription string 'Ses kaydı ve metne çevirme için mikrofon gerekli.'" \
  "$APP/Contents/Info.plist" 2>/dev/null || true

# Plist değiştiği için yeniden (ad-hoc) imzala
codesign --force --deep --sign - "$APP"

echo "Hazır: $APP"
