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
    
def mulai_menabung():
    global jumlah_hari, target_tabungan, target_per_hari, hari_ke, tabungan_awal, menabung_aktif
    try:
        target_tabungan = float(entry_target.get().replace('.', '').replace(',', '.'))
        jumlah_hari = int(entry_hari.get())
        if target_tabungan <= 0 or jumlah_hari <= 0:
            raise ValueError

        target_per_hari = target_tabungan / jumlah_hari
        hari_ke = 1
        menabung_aktif = True  # Menandai bahwa proses menabung aktif
        frame_menabung.pack_forget()
        menabung_harian(hari_ke)
    except ValueError:
        messagebox.showerror("Kesalahan Input", "Masukkan nilai yang valid untuk target dan jumlah hari!")

def menabung_harian(hari_ke):
    global tabungan_awal, target_per_hari, menabung_aktif

    def lanjutkan():
        global tabungan_awal, hari_ke, menabung_aktif
        tabungan_awal += target_per_hari
        simpan_data_ke_csv(tabungan_awal, f"Menabung hari ke-{hari_ke}", hari_ke)
        label_saldo.config(text=f"Saldo Tabungan: Rp {format_rupiah(tabungan_awal)}")
        messagebox.showinfo("Berhasil", f"Anda telah menabung di hari ke-{hari_ke}!")
        hari_ke += 1
        if hari_ke > jumlah_hari:
            menabung_aktif = False
            messagebox.showinfo("Selesai", "Anda telah menyelesaikan target menabung!")
        frame_harian.pack_forget()
        frame_menu.pack()

    def lewati():
        global hari_ke, menabung_aktif
        simpan_data_ke_csv(tabungan_awal, f"Tidak menabung hari ke-{hari_ke}", hari_ke)
        messagebox.showinfo("Lewati", f"Anda melewati menabung di hari ke-{hari_ke}.")
        hari_ke += 1
        if hari_ke > jumlah_hari:
            menabung_aktif = False
            messagebox.showinfo("Selesai", "Anda telah menyelesaikan target menabung!")
        frame_harian.pack_forget()
        frame_menu.pack()

    frame_menu.pack_forget()
    for widget in frame_harian.winfo_children():
        widget.destroy()

    frame_harian.pack()
    label_hari = Label(frame_harian, text=f"Hari ke-{hari_ke}/{jumlah_hari}", font=("Arial", 16))
    label_hari.pack(pady=10)

    label_saldo_harian = Label(frame_harian, text=f"Saldo Tabungan: Rp {format_rupiah(tabungan_awal)}", font=("Arial", 12))
    label_saldo_harian.pack(pady=10)

    Button(frame_harian, text="Menabung", command=lanjutkan).pack(pady=5)
    Button(frame_harian, text="Tidak Menabung", command=lewati).pack(pady=5)

def menarik_tabungan():
    global tabungan_awal

    def tarik():
        global tabungan_awal
        try:
            jumlah = float(entry_tarikan.get().replace('.', '').replace(',', '.'))
            if jumlah > tabungan_awal:
                messagebox.showerror("Kesalahan", "Jumlah tarikan melebihi saldo!")
                return
            tabungan_awal -= jumlah
            simpan_data_ke_csv(tabungan_awal, f"Menarik tabungan sebesar Rp {format_rupiah(jumlah)}", hari_ke - 1)
            label_saldo.config(text=f"Saldo Tabungan: Rp {format_rupiah(tabungan_awal)}")
            messagebox.showinfo("Berhasil", f"Anda berhasil menarik Rp {format_rupiah(jumlah)}!")
            frame_menarik.pack_forget()
            frame_menabung.pack()
        except ValueError:
            messagebox.showerror("Kesalahan Input", "Masukkan jumlah yang valid!")

    frame_menu.pack_forget()
    for widget in frame_menarik.winfo_children():
        widget.destroy()

    frame_menarik.pack()
    Label(frame_menarik, text=f"Saldo Tabungan Saat Ini: Rp {format_rupiah(tabungan_awal)}", font=("Arial", 12)).pack(pady=10)
    Label(frame_menarik, text="Masukkan Jumlah yang Akan Ditarik (Rp):", font=("Arial", 12)).pack(pady=5)
    entry_tarikan = Entry(frame_menarik)
    entry_tarikan.pack(pady=5)
    Button(frame_menarik, text="Tarik", command=tarik).pack(pady=10)
    Button(frame_menarik, text="Kembali", command=lambda: [frame_menarik.pack_forget(), frame_menu.pack()]).pack(pady=5)

root = Tk()
root.title("Aplikasi Tabungan Harian")
root.geometry("400x500")

tabungan_awal = baca_data_dari_csv()  # Ambil saldo dari file CSV jika ada
jumlah_hari = 0
target_tabungan = 0
target_per_hari = 0
hari_ke = 1
menabung_aktif = False

frame_login = Frame(root)
frame_login.pack()

Label(frame_login, text="Login", font=("Arial", 16)).pack(pady=10)
Label(frame_login, text="Username:", font=("Arial", 12)).pack(pady=5)
entry_username = Entry(frame_login)
entry_username.pack(pady=5)

Label(frame_login, text="Password:", font=("Arial", 12)).pack(pady=5)
entry_password = Entry(frame_login, show="*")
entry_password.pack(pady=5)

Button(frame_login, text="Login", command=login).pack(pady=10)

Button(frame_login, text="Daftar Akun Baru", command=registrasi).pack(pady=5)  # Tombol registrasi

frame_menu = Frame(root)
label_saldo = Label(frame_menu, text=f"Saldo Tabungan: Rp {format_rupiah(tabungan_awal)}", font=("Arial", 12))
label_saldo.pack(pady=10)

Label(frame_menu, text="Pilih Opsi:", font=("Arial", 16)).pack(pady=10)
Button(frame_menu, text="1. Lanjutkan Menabung", command=lambda: menabung_harian(hari_ke) if menabung_aktif else messagebox.showinfo("Informasi", "Mulai target baru dahulu."), width=25).pack(pady=5)
Button(frame_menu, text="2. Mulai Baru", command=lambda: [frame_menu.pack_forget(), frame_menabung.pack()], width=25).pack(pady=5)
Button(frame_menu, text="3. Menarik Tabungan", command=menarik_tabungan, width=25).pack(pady=5)
Button(frame_menu, text="4. Keluar", command=lambda: [frame_menu.pack_forget(), frame_login.pack()], width=25).pack(pady=5)

frame_menabung = Frame(root)
Label(frame_menabung, text="Masukkan Target Tabungan (Rp):", font=("Arial", 12)).pack(pady=5)
entry_target = Entry(frame_menabung)
entry_target.pack(pady=5)

Label(frame_menabung, text="Masukkan Jumlah Hari:", font=("Arial", 12)).pack(pady=5)
entry_hari = Entry(frame_menabung)
entry_hari.pack(pady=5)

Button(frame_menabung, text="Mulai", command=mulai_menabung).pack(pady=10)
Button(frame_menabung, text="Kembali", command=lambda: [frame_menabung.pack_forget(), frame_menu.pack()]).pack(pady=5)

frame_harian = Frame(root)

frame_menarik = Frame(root)

frame_registrasi = Frame(root)

root.mainloop()
