# Technical Specification Supabase - DanaKita

## 1. Arsitektur Backend & Konfigurasi Supabase

Platform **DanaKita** menggunakan Supabase sebagai *Backend-as-a-Service* (BaaS) terpusat. Seluruh komunikasi data dari frontend (*Client Portal* `index.html` dan *Super Admin Console* `super-admin.html`) dilakukan menggunakan client SDK `@supabase/supabase-js` v2 langsung melalui browser.

### 1.1 Kredensial & Klien Supabase
- **Supabase URL**: `https://tgcpyatrllswhlysqfer.supabase.co`
- **Publishable / Anon Key**: `sb_publishable_lwmxiQPF5yUSQnDu4JK12A_mN4tMdWH`
- **Inisialisasi Dynamic Klien**:
  ```javascript
  window.initSupabaseClient = function(token) {
    const options = {};
    if (token && token !== SUPABASE_KEY) {
      options.global = { headers: { Authorization: `Bearer ${token}` } };
    }
    window.dk.db = window.supabase.createClient(SUPABASE_URL, SUPABASE_KEY, options);
  };
  ```
  *Catatan Arsitektur*: Klien diinisialisasi secara langsung dengan *Anon Key* saat aplikasi pertama kali dimuat untuk mencegah *login block* saat validasi awal ID organisasi.

---

## 2. Skema Basis Data (Database Schema)

Basis data DanaKita terdiri dari 12 tabel utama yang saling terelasi secara multi-tenant menggunakan `organization_id`.

```
                    +-------------------+
                    |   organizations   |
                    +---------+---------+
                              |
     +------------------------+------------------------+
     |                        |                        |
+----+----+              +----+----+              +----+----+
|  admin  |              |  warga  |              | project |
+----+----+              +----+----+              +----+----+
     |                        |                        |
     |                        +-----------+------------+
     |                                    |
     |                           +--------+-------+
     |                           |   pembayaran   |
     |                           +--------+-------+
     |                                    |
     |                           +--------+-------+
     |                           |pembayaran_detail|
     |                           +----------------+
     |
     +-------------------------------------------------+
     | (Audit / Transaksi Tambahan)                    |
     +--------------+-------------------+--------------+
                    |                   |
            +-------+-------+   +-------+-------+
            |  pengeluaran  |   |   dana_lain   |
            +---------------+   +---------------+
```

### 2.1 Rincian Tabel Basis Data

#### 1. `organizations`
Menyimpan data master penyewa (tenant/komunitas/RT/RW).
- `id` (uuid/text, Primary Key)
- `client_code` (varchar, Unique, Indexed) - Kode unik organisasi (contoh: `DIR-01`, `KPI-01`)
- `nama` (text) - Nama internal organisasi
- `display_name` (text) - Nama tampilan publik organisasi
- `kontak_wa_admin` (varchar) - Nomor WhatsApp pengurus utama
- `plan_tier` (varchar) - Paket SaaS (`starter`, `pro`, `enterprise`)
- `siklus_tagihan` (varchar) - `Bulanan` atau `Tahunan`
- `validity_start` (timestamp/date) - Tanggal mulai langganan
- `validity_end` (timestamp/date) - Tanggal berakhir langganan
- `is_active` (boolean, default: `true`) - Status aktif/suspend tenant
- `config` (jsonb) - Konfigurasi UI portal warga:
  ```json
  {
    "warga_portal": {
      "show_dashboard_saldo": true,
      "show_pos_kas": true
    }
  }
  ```
- `created_at` (timestamp with time zone, default: `now()`)

#### 2. `admin`
Menyimpan akun pengurus/admin komunitas.
- `id` (uuid/text, Primary Key)
- `organization_id` (uuid/text, Foreign Key -> `organizations.id`)
- `username` (varchar, Unique per org)
- `nama_admin` (text)
- `password_hash` (text)
- `role` (varchar, default: `'admin'`)
- `jabatan` (text, default: `'Pengurus'`)
- `is_primary` (boolean, default: `false`) - Penanda admin utama (Primary Admin)
- `is_agreed_policy` (boolean, default: `false`) - Persetujuan UU PDP
- `must_change_password` (boolean, default: `false`)
- `permissions` (jsonb) - Fallback metadata permissions: `{"jabatan": "Ketua RT", "is_primary": true}`
- `created_at` (timestamp)

#### 3. `warga`
Menyimpan master data warga komunitas.
- `id` (text, Primary Key) - Format: `WRG-{timestamp}-{rand}`
- `organization_id` (uuid/text, Foreign Key -> `organizations.id`)
- `nama` (text)
- `no_rumah` (varchar) - Nomor blok / rumah (contoh: `A-01`, `NO 19`)
- `no_wa` (varchar) - Nomor WhatsApp
- `pin_hash` (text) - Hash PIN keamanan (default: hash dari `'1234'`)
- `status` (varchar, default: `'ACTIVE'`) - `'ACTIVE'` atau `'INACTIVE'` (Soft-delete)
- `is_agreed_policy` (boolean, default: `false`) - Persetujuan UU PDP
- `created_at` (timestamp)

#### 4. `project`
Menyimpan pos iuran kas atau program pembangunan.
- `id` (text, Primary Key) - Format: `PRJ-{timestamp}-{rand}`
- `organization_id` (uuid/text, Foreign Key -> `organizations.id`)
- `nama_project` (text) - Nama pos (contoh: `Kas RT`, `Iuran Kebersihan`)
- `tipe` (varchar) - `'bulanan'`, `'sekali'`, atau `'non_iuran'` (Pos Kas Saja)
- `start_periode` (varchar) - Format: `'YYYY-MM'` (contoh: `'2024-01'`)
- `nominal_default` (numeric) - Nominal iuran
- `target` (numeric) - Target dana terkumpul
- `target_warga` (jsonb/array) - Array ID warga penerima tagihan khusus: `["WRG-1", "WRG-2"]`
- `status` (varchar, default: `'ACTIVE'`) - `'ACTIVE'` atau `'INACTIVE'`
- `created_at` (timestamp)

#### 5. `pembayaran`
Menyimpan header transaksi pembayaran iuran oleh warga.
- `id` (text, Primary Key) - Format: `PAY-{timestamp}-{rand}`
- `organization_id` (uuid/text, Foreign Key -> `organizations.id`)
- `warga_id` (text, Foreign Key -> `warga.id`)
- `tanggal` (timestamp with time zone)
- `total_nominal` (numeric)
- `metode` (varchar) - `'TRANSFER'` atau `'CASH'`
- `bukti_url` (text) - Relative path di Supabase Storage (`{org_id}/{pay_id}_{timestamp}.jpg`)
- `status` (varchar) - `'MENUNGGU VERIFIKASI'`, `'DISETUJUI'`, `'DITOLAK'`
- `verified_by` (text) - Nama verifikator
- `verifier_role` (text) - Jabatan verifikator saat menyetujui
- `verified_at` (timestamp)
- `created_at` (timestamp)

#### 6. `pembayaran_detail`
Menyimpan rincian alokasi pos dan periode pembayaran.
- `id` (text, Primary Key) - Format: `DET-{timestamp}-{rand}`
- `organization_id` (uuid/text, Foreign Key -> `organizations.id`)
- `pembayaran_id` (text, Foreign Key -> `pembayaran.id`)
- `project_id` (text, Foreign Key -> `project.id`)
- `periode` (varchar) - Format: `'YYYY-MM'` atau `'SEKALI'`
- `nominal` (numeric)

#### 7. `pengeluaran`
Menyimpan transaksi kas keluar (belanja pengurus).
- `id` (text, Primary Key) - Format: `OUT-{timestamp}-{rand}`
- `organization_id` (uuid/text, Foreign Key -> `organizations.id`)
- `kategori_project` (text, Foreign Key -> `project.id`, Nullable) - Pos terkait jika ada
- `keterangan` (text) - Rincian belanja (Multi-line)
- `nominal` (numeric)
- `tanggal` (timestamp)

#### 8. `dana_lain`
Menyimpan transaksi kas masuk tambahan (Donasi, Hibah, Bunga Kas).
- `id` (text, Primary Key) - Format: `DON-{timestamp}-{rand}`
- `organization_id` (uuid/text, Foreign Key -> `organizations.id`)
- `sumber` (text) - Nama donatur / sumber dana
- `kategori_project` (text, Foreign Key -> `project.id`, Nullable)
- `keterangan` (text)
- `nominal` (numeric)
- `tanggal` (timestamp)

#### 9. `bank_accounts`
Menyimpan data rekening bank bendahara komunitas.
- `id` (text, Primary Key) - Format: `BAK-{timestamp}-{rand}`
- `organization_id` (uuid/text, Foreign Key -> `organizations.id`)
- `nama_bank` (varchar) - Contoh: `BCA`, `Mandiri`
- `no_rek` (varchar) - Nomor rekening
- `atas_nama` (text) - Nama pemilik rekening

#### 10. `super_admins`
Menyimpan akun pengelola console Super Admin / Pusat SaaS.
- `id` (uuid/text, Primary Key)
- `username` (varchar, Unique)
- `nama` (text)
- `password_hash` (text)
- `role` (varchar) - `'super_admin'` atau `'finance'`
- `jabatan` (text) - Contoh: `'CEO'`, `'Finance Specialist'`
- `permissions` (jsonb)

#### 11. `billing_settings`
Menyimpan pengaturan biaya langganan SaaS per tenant.
- `id` (uuid/text, Primary Key)
- `organization_id` (uuid/text, Foreign Key -> `organizations.id`)
- `nominal_gross` (numeric) - Total tagihan bruto
- `ppn_percentage` (numeric, default: `11`) - Persentase PPN (%)

#### 12. `audit_logs`
Menyimpan jejak audit (*audit trail*) seluruh aktivitas sistem.
- `id` (bigint/uuid, Primary Key)
- `organization_id` (uuid/text, Nullable)
- `actor_type` (varchar) - `'superadmin'`, `'admin'`, atau `'warga'`
- `actor_name` (text)
- `action` (text) - Jenis aktivitas (contoh: `VERIFY_PAYMENT_DISETUJUI_PAY-123`)
- `created_at` (timestamp with time zone, default: `now()`)

---

## 3. Stored Procedures & Functions (RPCs)

Autentikasi kustom dan utilitas kriptografi dikelola menggunakan PostgreSQL Stored Procedures (RPC):

### 3.1 `rpc_login_warga`
```sql
CREATE OR REPLACE FUNCTION rpc_login_warga(
  p_no_rumah text,
  p_pin text,
  p_org_id uuid
) RETURNS json AS $$
DECLARE
  v_warga warga%ROWTYPE;
BEGIN
  SELECT * INTO v_warga FROM warga
  WHERE organization_id = p_org_id
    AND UPPER(no_rumah) = UPPER(p_no_rumah)
    AND status = 'ACTIVE';

  IF NOT FOUND THEN
    RETURN json_build_object('success', false, 'msg', 'Nomor Rumah / Blok tidak ditemukan!');
  END IF;

  IF v_warga.pin_hash = crypt(p_pin, v_warga.pin_hash) THEN
    RETURN json_build_object(
      'success', true,
      'token', 'JWT_OR_SESSION_TOKEN',
      'data', json_build_object(
        'id', v_warga.id,
        'nama', v_warga.nama,
        'no_rumah', v_warga.no_rumah,
        'no_wa', v_warga.no_wa,
        'is_agreed_policy', v_warga.is_agreed_policy
      )
    );
  ELSE
    RETURN json_build_object('success', false, 'msg', 'PIN Keamanan salah!');
  END IF;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;
```

### 3.2 `rpc_login_admin`
Prosedur login untuk Admin Pengurus Komunitas yang memverifikasi kredensial, menentukan status `is_primary`, dan mengekstrak jabatan dari kolom atau metadata `permissions`.

### 3.3 `rpc_login_super_admin`
Prosedur login terpusat untuk operator Console Super Admin (`super-admin.html`).

### 3.4 `hash_password`
Fungsi pembantu enkripsi password/PIN menggunakan algoritma `pgcrypto` (`crypt(raw_pass, gen_salt('bf'))`).

### 3.5 `super_admin_add_super_admin`
Prosedur pembuatan anggota tim internal Super Admin baru.

---

## 4. Row-Level Security (RLS) & Kebijakan Akses

Seluruh tabel utama menerapkan kebijakan Row-Level Security (RLS) untuk menjamin isolasi data antar tenant (`organization_id`).

### 4.1 Kebijakan RLS Utama
1. **Isolasi Organization**:
   ```sql
   CREATE POLICY "Tenant Isolation Policy" ON pembayaran
   FOR ALL USING (organization_id = current_setting('app.current_org_id', true)::uuid);
   ```
2. **Izin Operasi Pengurus (Admin)**:
   - Tabel `admin` dan `pembayaran` mengizinkan `INSERT` dan `UPDATE` bagi pengguna terautentikasi dengan token valid.
3. **Bypass Super Admin**:
   - Operator dengan role `super_admin` memiliki bypass penuh untuk membaca dan mengelola seluruh record di semua tenant.

---

## 5. Storage Buckets & Manajemen Media

- **Bucket Name**: `bukti_transfer`
- **Aksesibilitas**: Private Bucket dengan URL berdurasi (Signed URL 60 detik) via `db().storage.from('bukti_transfer').createSignedUrl(path, 60)`.
- **Struktur Folder**: `{organization_id}/{pembayaran_id}_{timestamp}.{ext}`
- **Kebijakan Masa Simpan (Retention Policy)**: Foto bukti transfer dihapus otomatis dari storage setelah 1 (satu) tahun sesuai Kebijakan Privasi UU PDP.

---

## 6. Strategi Resiliensi Query & Fallback Logic

Untuk menjamin aplikasi tetap dapat berjalan secara mulus di berbagai lingkungan database Supabase (termasuk jika skema database belum melakukan migrasi kolom terbaru), kode JavaScript pada frontend menerapkan pola **Graceful Query Fallback**:

1. **Fallback Status 406 / Missing Column Detection**:
   Jika query Supabase mengembalikan error terkait kolom opsional (`target_warga`, `config`, `jabatan`, `is_primary`), aplikasi menangkap error tersebut (`error.code === 'PGRST204'` atau status `406`) dan melakukan retry otomatis dengan sekumpulan kolom dasar.
2. **Toleransi `target_warga` pada Pos Kas**:
   Aplikasi secara runtime mendeteksi keberadaan kolom `target_warga`. Jika kolom belum ada di Supabase, fitur Targeted Billing disembunyikan secara elegan tanpa menghentikan fungsi pos iuran lainnya.
3. **Penyatuan Metadata Permissions**:
   Apabila kolom `is_primary` atau `jabatan` belum ada secara native pada tabel `admin`, fungsi JavaScript akan membaca dan mereset nilai tersebut melalui JSONB column `permissions` secara otomatis.
