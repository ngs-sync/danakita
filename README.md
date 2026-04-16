# DanaKita - Portal Keuangan Komunitas

Aplikasi pengelolaan kas komunitas (RT/RW/Organisasi) yang mudah digunakan, aman, dan transparan.

## 🚀 Cara Menjalankan Aplikasi

### Opsi 1: Melalui GitHub Pages (Direkomendasikan)
Aplikasi ini sudah dikonfigurasi untuk dideploy otomatis menggunakan **GitHub Actions**.

1. **Atur Secrets di GitHub:**
   - Buka Repositori Anda di GitHub.
   - Pergi ke **Settings** > **Secrets and variables** > **Actions**.
   - Tambahkan **New repository secret**:
     - `VITE_SUPABASE_URL`: (Isi dengan URL Supabase Anda)
     - `VITE_SUPABASE_ANON_KEY`: (Isi dengan Anon Key Supabase Anda)
2. **Deploy:**
   - Setiap kali Anda melakukan `git push` ke branch `main`, GitHub akan otomatis membangun dan merilis versi terbaru ke GitHub Pages.

### Opsi 2: Menjalankan Lokal Tanpa Instalasi (Laptop Kantor)
Jika Anda tidak bisa menginstal Node.js/NPM di komputer:
1. Buka file `index.html` dan `super-admin.html` menggunakan editor teks (Notepad/VS Code).
2. Cari dan ganti teks berikut secara manual:
   - Ganti `"VITE_SUPABASE_URL_PLACEHOLDER"` dengan URL Supabase Anda.
   - Ganti `"VITE_SUPABASE_KEY_PLACEHOLDER"` dengan Anon Key Supabase Anda.
3. Simpan file dan buka langsung di browser.

### Opsi 3: Menjalankan Lokal dengan Node.js (Development)
1. Instal dependensi: `npm install`
2. Buat file `.env` dan isi dengan kredensial Supabase.
3. Jalankan server dev: `npm run dev`

## 🛠 Teknologi yang Digunakan
- **Vite:** Sistem build dan development.
- **Tailwind CSS:** Styling UI yang responsif dan modern.
- **Supabase:** Database, Auth, dan Storage (Bukti Transfer).
- **Phosphor Icons:** Set ikon yang elegan.
- **GitHub Actions:** Otomasi build dan deployment.

## 🔒 Keamanan
Aplikasi ini menggunakan sistem **Environment Variables** untuk menyembunyikan kunci API Anda dari kode sumber publik di GitHub. Pastikan untuk tidak pernah memasukkan file `.env` ke dalam commit git (sudah otomatis diabaikan oleh `.gitignore`).
