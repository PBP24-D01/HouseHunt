
# Tugas Kelompok D-01

## HouseHunt

### Anggota Kelompok
- Tristan Agra Yudhistira (2306245112)
- Daffa Naufal Rahadian (2306213003) 
- Siti Shofi Nadhifa (2306152172)
- Favian Zhafif Rizqullah Permana (2306274996)
- Muhammad Fayyed As Shidqi (2306230395)
- M. Alvin Rheinaldy G. Z. (2306275866)

### Deskripsi Aplikasi
Aplikasi ini bernama HouseHunt. Aplikasi ini bertujuan membantu masyarakat, baik penduduk lokal maupun pendatang, untuk menemukan informasi seputar rumah yang dijual di Bekasi. Ketika seseorang pindah atau berencana membeli rumah di Bekasi, sering kali mereka kesulitan mendapatkan informasi lengkap tentang harga, lokasi, dan detail properti dari berbagai sumber yang terpecah-pecah. Dengan HouseHunt, pengguna dapat mengakses database lengkap yang berisi daftar harga rumah di berbagai wilayah Bekasi beserta detail seperti luas bangunan, tipe rumah, jumlah kamar, dan harga.

Aplikasi ini memberikan keuntungan dengan menyediakan semua informasi dalam satu tempat yang mudah diakses, membantu pengguna membuat keputusan yang lebih baik tentang pembelian rumah. Selain itu, aplikasi ini mendukung pencarian berdasarkan kriteria spesifik seperti harga maksimal, luas tanah, atau lokasi, sehingga pengguna dapat dengan mudah menemukan rumah sesuai dengan kebutuhan mereka.

Fitur - fitur yang akan ada di HouseHunt:
- Menampilkan daftar rumah dan filter
- Menampilkan detail spesifikasi rumah
- Wishlist menu yang berisi rumah - rumah yang ingin dibeli
- Melakukan pemesanan rumah secara online
- Melakukan appointment untuk bertemu dengan penjual
- Mempromosikan rumah dengan iklan

### Daftar Modul

#### Rumah
##### Dikerjakan oleh: M. Alvin Rheinaldy G. Z. (2306275866)
Modul ini berfungsi untuk menampilkan rumah - rumah yang akan dijual. User juga dapat melakukan filter dan search sesuai yang diinginkan.
Pembeli|Penjual
-|-
Pembeli dapat memesan dan melihat rumah yang sedang dijual | CRUD rumah untuk dijual

#### Wishlist
##### Dikerjakan oleh: Siti Shofi Nadhifa (2306152172)
Modul ini berfungsi untuk user dapat menambahkan wishlist rumah yang ingin dibeli dan dapat menampilkan rumah - rumah yang ada di wishlist user.
Pembeli | Penjual
-|-
Pembeli dapat menambahkan wishlist dan melihat rumah apa saja yang sudah ada di wishlist | -

#### Diskusi
##### Dikerjakan oleh: Muhammad Fayyed As Shidqi (2306230395)
Modul ini berfungsi untuk pembeli dapat menanyakan pertanyaan kepada penjual
Pembeli | Penjual
-|-
Mengepost diskusi pada halaman detail rumah | Membalas diskusi pada halaman detail rumah

#### Cek Rumah
##### Dikerjakan oleh: Daffa Naufal Rahadian (2306213003) 
Modul ini berfungsi untuk membuat appointment antara pembeli dan penjual untuk melakukan pengecekan secara offline. Nantinya pembeli dapat memilih tanggal sesuai yang sudah penjual sediakan. Pembeli dan penjual juga dapat membatalkan dan mengedit tanggal appointment yang diinginkan.
Pembeli | Penjual
-|-
Memilih appointment dan membuat appointment | Membuat kapan saja appointment dapat dilakukan dan menyetujui appointment yang dibuat oleh pembeli

#### Iklan
##### Dikerjakan oleh: Favian Zhafif Rizqullah Permana (2306274996)
Modul ini berfungsi untuk seller memasang iklan di halaman web. Nantinya seller dapat memilih rumah mana yang mau diiklankan di halaman web. Iklan akan lebih dipertontonkan dibandingkan rumah yang tidak diiklankan. Seller dapat mengedit rumah mana yang diiklankan kapan saja dan seller dapat meng-upload banner untuk kebutuhan iklan.
Pembeli | Penjual
-|-
Melihat iklan | Membuat, mengedit, menghapus iklan

#### Authentifikasi
##### Dikerjakan oleh: Tristan Agra Yudhistira (2306245112)
Modul ini berfungsi untuk user dapat register dan login. Nantinya akan ada super user yang diberi role sabagai penjual untuk dapat menambahkan rumah, meng-update status pesanan, serta membalas diskusi pembeli.


### Sumber Dataset Rumah di Bekasi
https://www.kaggle.com/datasets/nafisbarizki/daftar-harga-rumah-jabodetabek 

### Role User
Terdapat dua role, yaitu pembeli dan penjual.