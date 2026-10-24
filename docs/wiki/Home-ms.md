[English](Home) · [Dansk](Home-da) · **Bahasa Malaysia**

# Personal Flight Club

Kelab penerbangan dari hari ke-40 kursus Udemy 100 Days of Code. Program ini membaca destinasi dan had harga daripada Google Sheet, mencari penerbangan pergi-balik termurah untuk enam bulan akan datang (penerbangan terus dahulu, kemudian dengan persinggahan) dan menghantar e-mel kepada setiap pelanggan dalam helaian kedua apabila harga lebih rendah daripada had.

## Cara ia berfungsi

1. Baca baris (bandar, kod IATA, harga terendah) daripada helaian `prices` melalui Sheety.
2. Cari penerbangan pergi-balik terus yang termurah dari esok hingga enam bulan lagi untuk setiap baris, dengan SerpAPI Google Flights atau perkhidmatan penerbangan olok-olok (mock) kursus.
3. Jika tiada penerbangan terus, cari semula penerbangan dengan sehingga dua persinggahan dan catat bilangan persinggahan.
4. Jika harga lebih rendah daripada harga terendah dalam helaian, kemas kini helaian, hantar mesej WhatsApp dan e-mel kepada setiap pelanggan dalam helaian `users`. Penerbangan dengan persinggahan menyatakan "Flight has 1 stopover." dalam mesej.

## Contoh larian dengan data mock

![Contoh larian dengan data mock](https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/040-personal-flight-club/raw/branch/main/docs/images/sample-run.png)

Seterusnya: [Bermula](Getting-Started-ms)
