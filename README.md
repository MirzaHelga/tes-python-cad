Furniture & Room CAD Generator

PROProgram berbasis Python untuk menghasilkan gambar kerja teknik secara otomatis dalam format AutoCAD (DXF) dan model 3D (STL). Alat ini dirancang untuk mempermudah desainer dan arsitek dalam membuat visualisasi cepat furnitur (kursi) dan denah ruangan berdasarkan input dimensi mentah. 
Fitur Utama
Dual Mode Generator: Mendukung pembuatan objek furnitur mendetail (Kursi) dan struktur arsitektur (Ruangan).
Dynamic Denah System: Menghasilkan denah (Tampak Atas) dengan garis dinding ganda dan simbol bukaan (pintu/jendela) berwarna.
Smart Isometric Alignment: Isometrik ditarik secara otomatis ke posisi terbawah menggunakan perhitungan trigonometri agar sejajar dengan Tampak Depan.
3D STL with Openings: Model 3D ruangan tidak lagi berupa balok solid, melainkan memiliki lubang pintu dan jendela yang akurat.
Zero Frame Policy: Menghasilkan file bersih tanpa bingkai/kop untuk kemudahan import ke software CAD profesional.

Asumsi & Simplifikasi Teknis
Karena input pengguna bersifat minimalis, program menggunakan asumsi standar berikut untuk menjamin validitas geometri:
Dimensi Dinding: Tebal dinding dipatok 15 cm (standar dinding bata finish).
Detail Kursi: Tebal kaki, sandaran, dan dudukan adalah 5 cm. Kaki belakang dibuat tinggi sebagai sandaran, sementara kaki depan setinggi dudukan.
Standar Bukaan:Pintu: Lebar 90 cm, tinggi 210 cm, tanpa ambang bawah.
Jendela: Lebar 120 cm X tinggi 100 cm
Tinggi ambang (parapet) : 100 cm.
Logika Isometrik: Menggunakan proyeksi isometrik 30° standar. 
Titik referensi $Y$ diturunkan sejauh $L \times \sin(30^\circ)$ agar visualisasi tidak melayang menabrak teks.
Struktur STL: Lubang pada model 3D dibuat menggunakan teknik segmentasi balok (bukan boolean subtraction) untuk memastikan file manifold (siap cetak 3D).

Instalasi
Program ini memerlukan Python 3.x dan beberapa pustaka tambahan:Bashpip install ezdxf trimesh numpy
Cara PenggunaanJalankan file utama: python main.py.
Pilih objek: 1 untuk Kursi, 2 untuk Ruangan.
Masukkan dimensi (Lebar, Panjang, Tinggi) dalam satuan cm.Jika memilih ruangan, tentukan sisi pintu dan jendela (utara/selatan/barat/timur/n).
Dapatkan file .dxf dan .stl secara instan.

Kode Warna CAD
Warna dan Representasi Visual
Merah (1)Struktur Utama / Dinding / Denah
Kuning (2)Elemen Jendela
Biru (3)Elemen Pintu
Cyan (4)Garis Isometrik
Biru Tua (5)Tampak Depan
Abu-abu (8)Elemen Lantai

Pengembangan Masa Depan
Penambahan furnitur lain (meja, lemari).
Simbol pintu dengan garis lengkung (swing door).
Fitur auto-dimension (pemberian ukuran otomatis).
