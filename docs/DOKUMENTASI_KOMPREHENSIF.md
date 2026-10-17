# Dokumentasi Komprehensif Platform DanaKita

Dokumentasi ini berisi panduan lengkap penggunaan aplikasi **DanaKita** untuk seluruh tingkat pengguna (**Warga**, **Pengurus/Admin Komunitas**, dan **Super Admin**), serta **Panduan Developer & Pengembang** untuk pemeliharaan dan pengembangan sistem.

---

## BAGIAN 1: PANDUAN PENGGUNA (USER MANUAL)

### 1. Panduan Penggunaan Portal Warga

#### A. Langkah Masuk (Login Warga)
1. Buka halaman utama portal di browser (`index.html`).
2. Masukkan **ID Organisasi / Kode Komunitas** (contoh: `DIR-01`) pada layar awal, lalu klik **Verifikasi Organisasi**.
3. Pilih tab **Warga**.
4. Masukkan **Username** (Nomor Rumah / Blok, contoh: `A-01` atau `NO 19`) dan **PIN Keamanan 6-digit** (PIN default awal dari pengurus: `1234`).
5. Pada kunjungan pertama, baca dan setujui **Kebijakan Privasi & Layanan (UU PDP)** dengan mencentang kotak persetujuan lalu klik **Setuju & Lanjutkan**.

#### B. Membayar Tagihan Iuran
1. Masuk ke tab **Tagihan** pada navigasi bawah (*floating nav*).
2. Pilih **Tahun Tagihan** (contoh: `2026`).
3. Centang bulan tagihan iuran yang ingin dibayar. Total tagihan akan terhitung otomatis.
4. Pilih **Metode Pembayaran**:
   - **Transfer Bank**: Nomor rekening tujuan transfer bendahara akan ditampilkan. Unggah foto bukti transfer. Foto akan otomatis dikompres hemat kuota (~100KB).
   - **Titip Tunai (Cash)**: Pilih metode ini jika menyerahkan uang cash langsung ke bendahara.
5. Klik **Kirim Pembayaran**. Status pembayaran akan masuk ke antrean verifikasi pengurus (`MENUNGGU VERIFIKASI`).

#### C. Melihat Riwayat & Cetak Struk
1. Buka tab **Riwayat**.
2. Pembayaran yang telah disetujui pengurus akan berstatus **DISETUJUI** (Hijau).
3. Klik **Buka Struk** untuk menampilkan Tanda Terima Resmi Lunas.
4. Klik **Kirim WA** untuk mengirimkan salinan struk ke WhatsApp, atau **Cetak PDF** untuk mencetak/menyimpan dokumen PDF.

#### D. Mengubah PIN Keamanan
1. Buka tab **Profil**.
2. Pada bagian **Ganti PIN Keamanan**, masukkan **PIN Lama**, **PIN Baru** (minimal 4 digit), dan **Konfirmasi PIN Baru**.
3. Klik **Update PIN**.

---

### 2. Panduan Penggunaan Pengurus / Admin Komunitas

#### A. Dashboard & Ringkasan Keuangan
1. Login via tab **Pengurus** menggunakan Username dan Password Admin.
2. Tab **Beranda** menampilkan:
   - **Total Saldo Kas**: Perhitungan otomatis `(Total Masuk - Total Keluar)`.
   - **Estimasi Piutang**: Total nilai iuran seluruh warga yang belum terbayar.
   - **Progress Pos Kas**: Persentase ketercapaian dana per program/pos.

#### B. Memproses Verifikasi Pembayaran
1. Buka menu **Status Bayar**.
2. **Tab Menunggu**: Menampilkan antrean bukti bayar warga. Klik **Setujui** atau **Tolak**. Nama dan jabatan Anda akan tercatat otomatis sebagai verifikator.
3. **Tab Selesai**: Menampilkan riwayat pembayaran yang disetujui. Gunakan filter tanggal untuk membatasi periode laporan.
4. **Tab Belum Bayar**:
   - Menampilkan daftar warga yang menunggak beserta rincian bulan dan total nominal arrears.
   - Klik **Kirim Tagihan ke WA** untuk mengirimkan pesan pengingat tagihan otomatis via WhatsApp.
   - Klik **Export Belum Bayar (Excel)** untuk mengunduh laporan tunggakan format `.xlsx`.

#### C. Kelola Master Data (`Master`)
1. **Rekening Pembayaran**: Tambah, edit, atau hapus nomor rekening bank tempat warga mentransfer iuran.
2. **Data Warga**:
   - **Manual**: Tambah warga baru satu per satu.
   - **Import Excel (CSV)**: Unduh template CSV, isi data warga, lalu unggah file untuk import sekaligus.
   - **Fitur Tambahan**: Klik **Kirim Info Login** untuk mengirimkan format SMS/WA info ID Organisasi & PIN default ke warga.
3. **Tim Pengurus / Admin**:
   - Primary Admin / Super Admin dapat menambah anggota pengurus baru dan menetapkan jabatan (Bendahara, Sekretaris, dll).
4. **Pos Iuran / Kas**:
   - Buat pos iuran baru: Tipe Bulanan, Sekali Bayar, atau Pos Kas Saja.
   - **Target Warga**: Pilih warga spesifik jika pos tersebut tidak berlaku untuk seluruh warga.

#### D. Pencatatan Mutasi Kas (`Kas`)
1. **Pengeluaran**: Tambahkan rincian barang belanjaan (multi-item), pilih pos kas pengambil dana, lalu simpan.
2. **Pemasukan Tambahan**: Catat donasi, sumbangan, atau dana hibah luar.
3. **Edit/Hapus Mutasi**: Transaksi kas salah input dapat diubah atau dihapus dengan penyesuaian saldo otomatis.

#### E. Laporan Pertanggungjawaban (`Laporan`)
1. Buka menu **Laporan**.
2. Tentukan **Tgl Mulai** dan **Tgl Selesai**.
3. Sistem akan menghitung **Saldo Awal**, **Kas Masuk**, **Kas Keluar**, dan **Saldo Akhir**.
4. Klik tombol **Excel** untuk mendownload Laporan LPJ Keuangan terformat rapi.

---

### 3. Panduan Penggunaan Console Super Admin

#### A. Login Console
1. Akses halaman `super-admin.html`.
2. Masukkan Username dan Password Super Admin.

#### B. Kelola Klien SaaS
1. **Pendaftaran Klien Baru**: Klik **Klien Baru**, isi Nama Organisasi, Client Code (contoh: `KPI-01`), Kontak WA, Paket SaaS, Masa Berakhir, dan detail Admin Pertama.
2. **Pengaturan Fitur Client**: Buka drawer **Kelola** pada klien terkait untuk mengaktifkan/nonaktifkan tampilan Saldo atau Pos Kas di portal warga.
3. **Suspend / Aktifkan**: Klik tombol **Suspend** untuk membekukan akses organisasi yang terlambat membayar biaya langganan SaaS.
4. **Cetak Invoice**: Klik **Download Invoice** di drawer klien untuk mencetak Invoice tagihan langganan resmi (format PDF dengan kalkulasi PPN 11%).

#### C. Monitoring Audit Log
1. Buka tab **Audit Log**.
2. Gunakan filter berdasarkan Klien, Aktor (Superadmin, Admin, Warga), dan Rentang Tanggal.
3. Klik **Export** untuk mengunduh log aktivitas dalam file CSV.

---

## BAGIAN 2: PANDUAN DEVELOPER & PENGEMBANG (DEVELOPER GUIDE)

### 1. Arsitektur Tanpa Build-Step (Zero Build-Step Architecture)

DanaKita dibangun dengan filosofi *Keep It Simple & Native*. Aplikasi tidak memerlukan Node.js, Webpack, Vite, Tailwind CLI, atau pustaka bundling lainnya.

#### Pustaka CDN yang Digunakan:
- **Tailwind CSS**: `https://cdn.tailwindcss.com` (Utility-first CSS)
- **Supabase JS v2**: `https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2`
- **Phosphor Icons**: `https://unpkg.com/@phosphor-icons/web@2.1.1`
- **PapaParse**: `https://cdnjs.cloudflare.com/ajax/libs/PapaParse/5.4.1/papaparse.min.js` (CSV Parser)
- **xlsx-js-style**: `https://cdn.jsdelivr.net/npm/xlsx-js-style@1.2.0/dist/xlsx.bundle.js` (Styled Excel Generator)
- **html2pdf.js**: `https://cdnjs.cloudflare.com/ajax/libs/html2pdf.js/0.10.1/html2pdf.bundle.min.js` (PDF Generator)

---

### 2. Struktur File Repository

```
/ (Root Repository)
├── index.html              # Frontend Portal Warga & Pengurus Komunitas (Single File App)
├── super-admin.html        # Console Super Admin & Pengelola SaaS
├── logo.png                # Asset Logo Utama DanaKita
└── docs/                   # Dokumentasi Proyek
    ├── PRD.md              # Product Requirement Document
    ├── TECH_SPEC_SUPABASE.md # Spesifikasi Teknis Backend Supabase
    └── DOKUMENTASI_KOMPREHENSIF.md # Dokumentasi Lengkap Pengguna & Pengembang
```

---

### 3. Konvensi Kode & Best Practices

1. **Pengelolaan State Global**:
   Seluruh state runtime disimpan di objek `window.dk.state`:
   ```javascript
   window.dk.state = {
     orgId: null,
     orgCode: '',
     user: null,
     token: null,
     data: { warga: [], project: [], pembayaran: [], detail: [], pengeluaran: [], danaLain: [] },
     bank_accounts: [],
     selectedCart: {},
     expenseItems: [{ ket: '', nom: '' }],
     wargaPage: 1,
     hasTargetWargaColumn: true
   };
   ```

2. **Gaya Penulisan Kode Safe Attribute**:
   Hindari meletakkan objek kompleks atau string unescaped dalam atribut HTML `onclick`. Gunakan ID-based lookup atau pengescapan karakter petik:
   ```javascript
   // REKOMENDASI:
   `<button onclick="fnEditById('${p.id}')">Edit</button>`
   `<button onclick="viewBuktiTransfer('${p.bukti_url.replace(/'/g, "\\'")}')">Bukti</button>`
   ```

3. **Inisialisasi Supabase Instant**:
   Supabase client wajib diinisialisasi segera menggunakan Anon Key agar validasi awal organisasi tidak terhambat:
   ```javascript
   window.initSupabaseClient();
   ```

4. **Eksekusi Async Safe dengan UI Loader**:
   Seluruh panggilan API asinkron harus dibungkus dalam blok `try-catch-finally` untuk memastikannya selalu menutup UI spinner loader:
   ```javascript
   showLoader(true);
   try {
     // Operations...
   } catch(e) {
     console.error(e);
     alert('Error: ' + e.message);
   } finally {
     showLoader(false);
   }
   ```

---

### 4. Panduan Deployment & Hosting

Karena DanaKita merupakan aplikasi web statis murni, aplikasi dapat disebar (*deploy*) ke penyedia hosting statis manapun tanpa server backend Node.js.

#### A. Deployment via GitHub Pages
1. Push repositori ke GitHub.
2. Buka **Settings** repositori -> **Pages**.
3. Pilih branch `main` dan folder `/ (root)`.
4. Klik **Save**. Aplikasi akan langsung aktif di URL `https://<username>.github.io/<repo-name>/`.

#### B. Deployment via Vercel / Netlify
1. Hubungkan repositori GitHub ke Vercel/Netlify.
2. Set **Build Command** menjadi kosong (blank) dan **Output Directory** menjadi `.` (root).
3. Klik **Deploy**.

#### C. Pengujian Lokal (Local Testing)
Aplikasi dapat dijalankan tanpa web server lokal:
1. Double click file `index.html` atau `super-admin.html` langsung dari File Explorer (menggunakan protokol `file://`).
2. Atau gunakan ekstensi VS Code **Live Server** untuk pengalaman pengembangan yang lebih nyaman.
