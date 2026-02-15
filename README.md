# 🤖 ChatBot Sederhana Python (Versi Bahasa Indonesia)

Chatbot berbasis konsol sederhana yang dibuat dengan Python yang bisa melakukan percakapan dalam bahasa Indonesia.

## Fitur

- Merespons salam dalam bahasa Indonesia (halo, hai, selamat pagi, dll)
- Merespons salam dalam bahasa Inggris (hello, hi, hey, dll)
- Menjawab pertanyaan tentang dirinya sendiri
- Menangani alur percakapan dasar
- Pencocokan pola menggunakan ekspresi reguler
- Seleksi respon acak untuk variasi
- Keluar yang bersih dengan 'quit', 'exit', atau 'bye'

## Cara Menjalankan

1. Pastikan Anda telah menginstal Python (Python 3.6 atau lebih tinggi)
2. Navigasi ke direktori proyek
3. Jalankan chatbot:

```bash
python chatbot.py
```

## Cara Menggunakan

- Ketik pesan apa pun untuk mengobrol dengan bot
- Coba katakan: "halo", "apa kabar", "siapa namamu", "bantu saya"
- Ketik "quit", "exit", atau "bye" untuk keluar dari chat

## Contoh Percakapan

```
🤖 ChatBot Sederhana
==============================
Halo! Saya adalah chatbot sederhana. Ketik 'quit' untuk keluar.

Anda: halo
ChatBot: Hai! Ada yang bisa saya bantu?

Anda: apa kabar?
ChatBot: Saya baik-baik saja, terima kasih sudah bertanya!

Anda: siapa namamu?
ChatBot: Anda bisa memanggil saya ChatBot!

Anda: bye
ChatBot: Selamat tinggal! Terima kasih sudah mengobrol!
```

## Struktur Kode

- Kelas `SimpleChatbot` berisi semua logika chatbot
- Pencocokan pola menggunakan ekspresi reguler
- Kamus respon untuk kategori yang berbeda
- Loop chat utama dalam metode `chat()`

## Kustomisasi

Anda dapat dengan mudah memperluas chatbot dengan:
1. Menambahkan kategori respon baru ke `self.responses`
2. Menambahkan pola baru ke `self.patterns`
3. Memodifikasi pesan respon
4. Menambahkan logika pencocokan yang lebih canggih

## Persyaratan

- Python 3.6+
- Tidak ada dependensi eksternal (menggunakan hanya modul bawaan)