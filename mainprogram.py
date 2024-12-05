from datetime import datetime, timedelta
from tkinter import Tk, Frame, Label, Entry, Button, messagebox
from bacadata import simpan_data_ke_csv, baca_data_dari_csv
from akunpengguna import baca_data_akun, simpan_data_akun, daftar_akun, login_akun

def format_rupiah(nilai):
    return f"{nilai:,.0f}"

def login():
    username = entry_username.get()
    password = entry_password.get()

    if login_akun(username, password):
        messagebox.showinfo("Berhasil", "Login berhasil!")
        frame_login.pack_forget()
        frame_menu.pack()
    else:
        messagebox.showerror("Gagal", "Username atau password salah!")

# Fungsi untuk registrasi akun baru
def registrasi():
    def simpan_akun():
        username = entry_reg_username.get()
        password = entry_reg_password.get()

        if not username or not password:
            messagebox.showerror("Kesalahan", "Username dan password tidak boleh kosong!")
            return

        data_akun = baca_data_akun()
        if username in data_akun:
            messagebox.showerror("Kesalahan", "Username sudah terdaftar!")
        else:
            daftar_akun(username, password)
            messagebox.showinfo("Berhasil", "Registrasi berhasil! Silakan login.")
            frame_registrasi.pack_forget()
            frame_login.pack()

    frame_login.pack_forget()
    for widget in frame_registrasi.winfo_children():
        widget.destroy()

    frame_registrasi.pack()
    Label(frame_registrasi, text="Registrasi Akun Baru", font=("Arial", 16)).pack(pady=10)
    Label(frame_registrasi, text="Username:", font=("Arial", 12)).pack(pady=5)
    entry_reg_username = Entry(frame_registrasi)
    entry_reg_username.pack(pady=5)

    Label(frame_registrasi, text="Password:", font=("Arial", 12)).pack(pady=5)
    entry_reg_password = Entry(frame_registrasi, show="*")
    entry_reg_password.pack(pady=5)

    Button(frame_registrasi, text="Daftar", command=simpan_akun).pack(pady=10)
    Button(frame_registrasi, text="Kembali", command=lambda: [frame_registrasi.pack_forget(), frame_login.pack()]).pack(pady=5)

global tabungan_awal, hari_ke, jumlah_hari, target_tabungan, target_per_hari, tanggal_mulai, berhasil_menabung, menabung_setiap_hari, tabungan_awal_sebelumnya
data_tabungan = baca_data_dari_csv()
tabungan_awal = float(data_tabungan[-1]['tabungan_akhir']) if data_tabungan else 0.0
hari_ke = 1
jumlah_hari = 0
target_tabungan = 0
target_per_hari = 0
tanggal_mulai = datetime.now()
berhasil_menabung = False
menabung_setiap_hari = True

def mulai_menabung():
    global jumlah_hari, target_tabungan, target_per_hari, hari_ke, tabungan_awal, menabung_aktif
    try:
        target_tabungan = float(input("Masukkan target tabungan (Rp): ").replace('.', '').replace(',', '.'))
        jumlah_hari = int(input("Masukkan jumlah hari: "))

        if target_tabungan <= 0 or jumlah_hari <= 0:
            raise ValueError

        target_per_hari = target_tabungan / jumlah_hari
        hari_ke = 1
        menabung_aktif = True  # Menandai bahwa proses menabung aktif

        print(f"\nTarget tabungan: Rp {format_rupiah(target_tabungan)}")
        print(f"Jumlah hari: {jumlah_hari}")
        print(f"Target tabungan per hari: Rp {format_rupiah(target_per_hari)}\n")
        
        menabung_harian(hari_ke)

    except ValueError:
        print("Kesalahan Input: Masukkan nilai yang valid untuk target dan jumlah hari!")

def menabung_harian(hari_ke):
    global tabungan_awal, target_per_hari, menabung_aktif

    while hari_ke <= jumlah_hari and menabung_aktif:
        print(f"\nHari ke-{hari_ke}/{jumlah_hari}")
        print(f"Saldo Tabungan Saat Ini: Rp {format_rupiah(tabungan_awal)}")
        print(f"Target Hari Ini: Rp {format_rupiah(target_per_hari)}")

        pilihan = input("Pilih aksi: [1] Menabung [2] Lewati: ")
        if pilihan == "1":
            tabungan_awal += target_per_hari
            simpan_data_ke_csv(tabungan_awal, f"Menabung hari ke-{hari_ke}", hari_ke)
            print(f"Berhasil menabung! Saldo saat ini: Rp {format_rupiah(tabungan_awal)}")
        elif pilihan == "2":
            simpan_data_ke_csv(tabungan_awal, f"Tidak menabung hari ke-{hari_ke}", hari_ke)
            print(f"Hari ke-{hari_ke} dilewati.")
        else:
            print("Pilihan tidak valid. Coba lagi.")
            continue

        hari_ke += 1

    if hari_ke > jumlah_hari:
        menabung_aktif = False
        print("\nAnda telah menyelesaikan target menabung! Selamat!")
        
def menarik_tabungan():
    global tabungan_awal

    try:
        print(f"\nSaldo Tabungan Saat Ini: Rp {format_rupiah(tabungan_awal)}")
        jumlah = float(input("Masukkan jumlah yang ingin ditarik (Rp): ").replace('.', '').replace(',', '.'))
        if jumlah > tabungan_awal:
            print("Kesalahan: Jumlah tarikan melebihi saldo!")
            return

        tabungan_awal -= jumlah
        simpan_data_ke_csv(tabungan_awal, f"Menarik tabungan sebesar Rp {format_rupiah(jumlah)}", hari_ke - 1)
        print(f"Berhasil menarik Rp {format_rupiah(jumlah)}! Saldo saat ini: Rp {format_rupiah(tabungan_awal)}")
    except ValueError:
        print("Kesalahan Input: Masukkan jumlah yang valid!")

def menu_utama():
    global tabungan_awal
    tabungan_awal = baca_data_dari_csv()
    while True:
        print("\n=== Aplikasi Tabungan Harian ===")
        print(f"Saldo Tabungan: Rp {format_rupiah(tabungan_awal)}")
        print("1. Lanjutkan Menabung")
        print("2. Mulai Target Baru")
        print("3. Menarik Tabungan")
        print("4. Keluar")

        pilihan = input("Pilih opsi: ")
        if pilihan == "1":
            if menabung_aktif:
                menabung_harian(hari_ke)
            else:
                print("Mulai target baru dahulu.")
        elif pilihan == "2":
            mulai_menabung()
        elif pilihan == "3":
            menarik_tabungan()
        elif pilihan == "4":
            print("Terima kasih telah menggunakan aplikasi. Selamat menabung!")
            break
        else:
            print("Pilihan tidak valid. Coba lagi.")

if __name__ == "__main__":
    menu_utama()