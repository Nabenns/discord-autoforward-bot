# Discord Auto-Forward Bot

Bot Discord sederhana yang dapat melakukan auto-forward pesan dari satu server ke server lainnya.

## Fitur

- Auto-forward pesan antar server Discord
- Mendukung forward teks, gambar, dan file
- Konfigurasi channel sumber dan tujuan yang mudah
- Logging untuk monitoring aktivitas bot

## Persyaratan

- Python 3.8 atau lebih tinggi
- Token Bot Discord
- Izin yang sesuai di server Discord

## Instalasi

1. Clone repository ini:
```bash
git clone https://github.com/Nabenns/discord-autoforward-bot.git
cd discord-autoforward-bot
```

2. Buat virtual environment dan aktifkan:
```bash
python -m venv venv
# Windows
venv\\Scripts\\activate
# Linux/Mac
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Salin `.env.example` ke `.env` dan isi dengan token bot dan konfigurasi channel:
```bash
cp .env.example .env
```

## Konfigurasi

Edit file `.env` dan isi dengan informasi yang diperlukan:

```env
DISCORD_TOKEN=your_bot_token_here
SOURCE_CHANNEL_ID=source_channel_id
TARGET_CHANNEL_ID=target_channel_id
```

## Penggunaan

Jalankan bot dengan perintah:
```bash
python bot.py
```

## Lisensi

MIT License

## Kontribusi

Kontribusi selalu diterima. Silakan buat pull request atau issue untuk perbaikan atau saran fitur baru.