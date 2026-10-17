# Product Requirement Document (PRD) - DanaKita

## 1. Ringkasan Eksekutif (Executive Summary)
**DanaKita** adalah platform web terpadu pengurusan dan transparansi keuangan kas komunitas (seperti RT/RW, Paguyuban, Kompleks Perumahan, dan Organisasi Nirlaba). Platform ini dirancang untuk berjalan sebagai aplikasi web statis modern (*no-build step*) tanpa dependensi kompilasi Node.js, berbasis HTML5, Tailwind CSS, JS (ES6+), dan backend cloud-native **Supabase**.

Platform DanaKita terdiri dari dua komponen utama:
1. **Portal Klien / Warga & Pengurus (`index.html`)**: Memfasilitasi pembayaran iuran oleh warga, pengecekan tunggakan, penerbitan tanda terima (struk), manajemen master warga, pos iuran, mutasi kas, serta LPJ keuangan bulanan/tahunan.
2. **Console Super Admin (`super-admin.html`)**: Memfasilitasi manajemen multi-tenant (klien/organisasi), pendaftaran paket SaaS, otorisasi tim internal, pengawasan audit log sistem, dan penerbitan invoice berlangganan.

---

## 2. Visi Produk & Sasaran (Vision & Goals)

### 2.1 Visi
Menjadi solusi pengelolaan dana kas komunitas berbasis digital terbaik di Indonesia yang transparan, mudah digunakan oleh warga maupun pengurus dari berbagai kelompok usia, serta patuh terhadap regulasi perlindungan data pribadi (UU PDP No. 27 Tahun 2022).

### 2.2 Tujuan Utama (Key Objectives)
- **Transparansi Keuangan Komunitas**: Warga dapat memantau saldo kas aktif, progress penerimaan pos kas, dan laporan pertanggungjawaban secara real-time.
- **Kemudahan Pembayaran & Verifikasi**: Memudahkan warga membayar iuran via Transfer Bank atau Titip Cash, serta mempercepat pengurus melakukan verifikasi status bayar.
- **Pengelolaan Multi-Tenant Berbasis SaaS**: Super Admin dapat mengelola banyak organisasi/klien dalam satu platform terpusat dengan isolasi data berbasis `organization_id`.
- **Zero-Build Architecture**: Tidak memerlukan proses build/bundling (Vue/React/Angular/Node build step) sehingga mudah di-host di CDN statis manapun (GitHub Pages, Vercel, Netlify) dan dapat dijalankan langsung di browser lokal.

---

## 3. Pengguna & User Persona (Target Users)

| Persona | Peran & Deskripsi | Kebutuhan Utama |
|---|---|---|
| **Warga Komunitas** | Anggota warga/kompleks perumahan yang wajib/sukarela membayar iuran kas bulanan atau sumbangan program. | - Melihat rincian tagihan belum dibayar.<br>- Melakukan pembayaran (Upload bukti transfer/titip cash).<br>- Melihat dan mencetak tanda terima (struk PDF/WA).<br>- Mengubah PIN keamanan akun. |
| **Pengurus / Admin Komunitas** | Pengurus RT/RW, Bendahara, atau Sekretaris yang mengelola kas dan data warga. | - Verifikasi pembayaran masuk.<br>- Verifikasi verifikator & jabatan.<br>- Kelola Master Warga (CRUD & Import CSV).<br>- Terbitkan Pos Iuran (Bulanan, Sekali Bayar, Pos Kas Saja, Targeted Warga).<br>- Pencatatan Pengeluaran & Pemasukan Dana Lain.<br>- Export LPJ Keuangan & Tunggakan ke Excel. |
| **Super Admin / Tim Internal** | Operator pusat DanaKita (Pemilik SaaS, Finance, Customer Success). | - Manajemen pendaftaran klien/komunitas baru.<br>- Pengaturan siklus & masa aktif SaaS.<br>- Pengaturan toggle fitur portal warga.<br>- Pengelolaan tim internal & penetapan Primary Admin.<br>- Pemantauan Audit Log sistem.<br>- Penerbitan Invoice tagihan SaaS Klien. |

---

## 4. Struktur Arsitektur & Antarmuka Layanan

DanaKita terbagi menjadi 2 portal utama:

```
DanaKita Repository
│
├── index.html              --> Portal Klien (Warga & Admin Pengurus)
├── super-admin.html        --> Console Super Admin (Pusat SaaS)
├── logo.png                --> Brand Logo Utama
└── docs/                   --> Dokumentasi Sistem
    ├── PRD.md
    ├── TECH_SPEC_SUPABASE.md
    └── DOKUMENTASI_KOMPREHENSIF.md
```

---

## 5. Rincian Fitur Utama (Product Features)

### 5.1 Portal Klien (`index.html`)

#### A. Autentikasi & Gerbang Privasi
1. **Verifikasi Kode Organisasi (`fnValidateKode`)**:
   - Pengguna menginput ID Organisasi / Kode Komunitas (contoh: `DIR-01`).
   - Penanganan toleransi kesalahan (*resilience*): Otomatis fallback jika kolom opsional pada Supabase belum diatur.
   - Menyimpan sesi organisasi di `localStorage` (`dk_org`).
2. **Login Portal Warga (`rpc_login_warga`)**:
   - Memasukkan Username (Blok/No Rumah) dan PIN 6-digit.
   - Switcher tab login modern antara "Warga" dan "Pengurus" (`switchLoginTab`).
3. **Login Pengurus/Admin (`rpc_login_admin`)**:
   - Memasukkan Username Admin dan Password.
   - Menyimpan kredensial sesi terenkripsi sementara di `localStorage` (`dk_session`).
4. **Gerbang Kepatuhan Privasi (UU PDP No. 27/2022)**:
   - Menampilkan modal Kebijakan Privasi eksplisit sebelum masuk ke antarmuka aplikasi.
   - Pengecekan status `is_agreed_policy` pada tabel `warga` / `admin`.
   - Super Admin diberikan bypass kebijakan privasi.

#### B. Fitur Portal Warga
1. **Beranda & Ringkasan Kas**:
   - Kartu Saldo Kas Aktif, Total Masuk, dan Total Keluar (dapat disembunyikan via konfigurasi organisasi).
   - Widget Tagihan Belum Dibayar (Arrears Accordion) dengan navigasi langsung ke tab bayar.
   - Progress Bar pencapaian Pos Kas/Proyek Iuran.
2. **Tagihan & Pembayaran Iuran**:
   - Pemilihan tahun tagihan (contoh: 2025, 2026, 2027).
   - Penandaan iuran bulanan yang sudah lunas vs belum bayar.
   - Metode Pembayaran: **Transfer Bank** (dengan daftar rekening pengurus dari tabel `bank_accounts`) dan **Titip Cash**.
   - Kompresi Gambar Otomatis (Native HTML5 Canvas Compression) untuk foto bukti transfer (~100KB - 150KB) sebelum diunggah ke Supabase Storage (`bukti_transfer`).
3. **Riwayat & Tanda Terima (Struk)**:
   - Daftar riwayat transaksi pembayaran dengan status: `MENUNGGU VERIFIKASI`, `DISETUJUI`, `DITOLAK`.
   - Modal Struk Pembayaran Lunas dengan opsi Cetak PDF (`window.print`) dan Kirim Bukti via WhatsApp API (`https://wa.me/...`).
4. **Profil & Keamanan**:
   - Informasi data diri (Nama, No. Rumah, WhatsApp).
   - Fitur Ubah PIN Keamanan Warga (Verifikasi PIN lama + PIN baru).

#### C. Fitur Admin Pengurus Komunitas
1. **Dashboard Admin**:
   - Monitoring Saldo Kas Utama, Total Masuk, Total Keluar, dan Estimasi Piutang (Belum Bayar).
   - Breakdown Progress Pos Kas & rincian sumber dana (Iuran Warga vs Donasi/Sumbangan Luar).
2. **Status Bayar & Verifikasi Pembayaran**:
   - **Tab Menunggu (Pending)**: Menampilkan antrean pembayaran warga yang membutuhkan verifikasi.
   - **Tab Selesai (Processed)**: Riwayat pembayaran yang disetujui, dilengkapi filter tanggal (Dari Tgl - Sampai Tgl) dan pengurutan terbaru.
   - **Tab Belum Bayar (Unpaid)**: Daftar warga yang menunggak tagihan diurutkan berdasarkan nominal terbesar, dilengkapi tombol "Kirim Tagihan ke WA" dan "Export Belum Bayar (Excel)".
   - **Modal Verifikasi**: Menetapkan verifikator, nama verifikator, dan jabatan otomatis berdasarkan sesi login.
3. **Master Data & Pengaturan**:
   - **Rekening Pembayaran**: CRUD akun bank pengurus pada tabel `bank_accounts`.
   - **Data Warga**:
     - Tambah manual & Edit Data Warga (Ganti Blok, No. WA, Reset PIN).
     - Import Data Warga Sekaligus via File CSV (`PapaParse`).
     - Hapus Data Warga (Soft-delete: mengubah status menjadi `INACTIVE`).
     - Kirim Info Akses Login Warga via WhatsApp.
     - Paginasi 5-item per halaman yang responsif terhadap pencarian Nama/Blok.
   - **Manajemen Tim Admin**:
     - Tambah / Edit / Hapus tim pengurus.
     - Penandaan status **Primary Admin** (Lencana ORANGE & Ikon Mahkota).
     - Pembatasan hak akses: Admin biasa hanya bisa mengedit profil diri sendiri, sedangkan Primary Admin / Super Admin dapat mengelola seluruh pengurus.
   - **Pos Iuran / Kas**:
     - Jenis Pos: Bulanan, Sekali Bayar, Pos Kas Saja (Non-Iuran).
     - Fitur **Targeted Billing** (`target_warga`): Penentuan spesifik warga penerima tagihan pos kas.
     - Penanganan keandalan runtime schema jika kolom `target_warga` belum ada pada basis data.
4. **Mutasi Kas & Pengeluaran**:
   - **Pengeluaran Kas**: Multi-item belanja dalam satu transaksi pengeluaran.
   - **Pemasukan Tambahan / Dana Lain**: Donasi, sumbangan, atau dana hibah.
   - Log mutasi kas dengan filter rentang tanggal dan tombol Edit/Hapus Mutasi.
5. **LPJ Keuangan & Export Report**:
   - Perhitungan Saldo Awal, Kas Masuk, Kas Keluar, dan Saldo Akhir sesuai periode tanggal.
   - Export Laporan LPJ Keuangan ke format Excel (`xlsx-js-style`) dengan tata letak rapi & header bercetak tebal.

---

### 5.2 Console Super Admin (`super-admin.html`)

#### A. Autentikasi & Sesi
- Login khusus Super Admin / Finance via RPC `rpc_login_super_admin`.
- Penyimpanan sesi `sa_session` termasuk role (`super_admin` atau `finance`) dan `jabatan`.

#### B. Manajemen Klien (Multi-Tenant SaaS)
- Registrasi Klien / Organisasi Baru:
  - Input Kode Client, Display Name, WA Pengurus, Paket SaaS (Starter, Pro, Enterprise), Siklus Tagihan, Nominal, PPN (%), dan Tanggal Validity.
  - Otomatis membuatkan akun **Primary Admin** pertama untuk organisasi tersebut.
  - Konfigurasi Tampilan Portal Warga (`show_dashboard_saldo`, `show_pos_kas`).
- Pengaturan Suspend / Aktifkan Organisasi (`is_active`).
- Drawer Detail Klien: Edit profil, masa aktif, toggle fitur portal, serta manajemen akun admin organisasi (termasuk promosi/demosi Primary Admin).
- Generator Invoice Langganan PDF (`html2pdf.js`) otomatis menghitung DPP dan PPN.

#### C. Tim Internal & Audit Log
- **Tim Internal**: Tambah/Hapus tim pusat dengan role `super_admin` (Akses Penuh) atau `finance` (Akses Billing/Read-only).
- **Audit Log Terpusat**:
  - Mencatat seluruh aktivitas penting di seluruh organisasi (Login, Verifikasi Bayar, Mutasi Kas, Tambah Admin, Edit Profile).
  - Filter log berdasarkan Klien, Aktor (Superadmin, Admin, Warga), dan Rentang Tanggal.
  - Export Audit Log ke file CSV.

---

## 6. Persyaratan Non-Fungsional (Non-Functional Requirements)

1. **Performa & Ukuran Bundle**:
   - Dijalankan langsung melalui CDN tanpa proses kompilasi (*Zero-Build Step*).
   - Waktu muat awal (*Initial Page Load*) < 2 detik pada koneksi 3G/4G.
   - Gambar bukti transfer otomatis dikompresi di sisi klien menjadi < 150 KB.
2. **Keandalan & Resiliensi (Resilience & Fallbacks)**:
   - Seluruh pemanggilan asinkron Supabase dibungkus dalam blok `try-catch-finally` untuk menjamin Spinner Loader selalu ditutup.
   - Skema database yang belum memiliki kolom opsional (`target_warga`, `config`, `jabatan`, `is_primary`) tidak boleh menyebabkan aplikasi crash (*graceful degradation*).
3. **Keamanan & Akses Data**:
   - Password dan PIN disimpan dalam bentuk hash terenskripsi (`pin_hash`, `password_hash`).
   - Menerapkan Row-Level Security (RLS) di Supabase untuk mengisolasi data antar-organisasi.
   - Penyensoran nomor telepon WhatsApp (masking `62812****789`) pada tampilan antarmuka publik kecuali untuk Super Admin.
4. **Kompatibilitas Lintas Platform**:
   - Responsif penuh di perangkat Mobile (320px+), Tablet, dan Desktop.
   - Dapat diakses langsung melalui protokol `file://` di lingkungan kantor/terbatas tanpa local web server Node.js.
5. **Kepatuhan Regulasi PDP**:
   - Mendukung UU PDP No. 27/2022 (Persetujuan eksplisit, hak pencabutan, masa retensi foto bukti transfer 1 tahun auto-delete, dan kontak DPO).
