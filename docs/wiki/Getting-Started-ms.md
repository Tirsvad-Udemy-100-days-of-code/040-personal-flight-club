[English](Getting-Started) · [Dansk](Getting-Started-da) · **Bahasa Malaysia**

# Bermula

## Keperluan

- Python 3.13 atau lebih baharu
- Projek Sheety untuk salinan Google Sheet anda dengan helaian `prices` dan `users` (pengesahan Bearer, PUT dihidupkan pada `prices`)
- Kunci SerpAPI atau kelayakan perkhidmatan penerbangan mock
- Akaun e-mel dengan kata laluan aplikasi untuk menghantar e-mel tawaran
- Pilihan: `pywhatkit`, pelayar dan sesi WhatsApp Web yang telah log masuk

## Pemasangan

Cipta persekitaran maya setempat, naik taraf pip dan pasang projek:

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

```bash
python3.13 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

## Konfigurasi

Salin `.env.example` ke `.env` dan isi nilainya. Jangan sekali-kali commit `.env`. Kekalkan 3 hingga 5 destinasi dalam helaian supaya kekal dalam had percuma, dan cuba program dengan helaian `users` ujian yang hanya mengandungi alamat anda sendiri.

| Pemboleh ubah | Maksud |
| --- | --- |
| `SHEETY_PRICES_ENDPOINT` | Endpoint helaian `prices` |
| `SHEETY_USERS_ENDPOINT` | Endpoint helaian `users` (`firstName`, `lastName`, `email`) |
| `SHEETY_TOKEN` | Token Bearer projek Sheety |
| `FLIGHT_PROVIDER` | `serpapi` atau `mock` |
| `SERPAPI_API_KEY` | Kunci SerpAPI |
| `MOCK_FLIGHTS_APP_ID`, `MOCK_FLIGHTS_APP_KEY` | Kelayakan perkhidmatan penerbangan mock |
| `SMTP_ADDRESS` | Pelayan SMTP pembekal e-mel anda (port 587) |
| `EMAIL_ADDRESS`, `EMAIL_PASSWORD` | Alamat penghantar dan kata laluan aplikasinya |
| `WHATSAPP_NUMBER` | Nombor anda dengan kod negara |

## Jalankan

Mulakan program. Tanpa tetapan SMTP atau nombor WhatsApp, mesej dicetak sebagai ganti.

```bash
python -m flight_club
```

## Ujian

Ujian tidak menggunakan rangkaian, tidak menghantar e-mel dan tidak membaca `.env` anda.

```bash
python -m pytest
```

![Larian ujian](https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/040-personal-flight-club/raw/branch/main/docs/images/tests-run.png)
