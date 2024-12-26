from tkinter import Tk, Frame, Label, Entry, Button, messagebox, Canvas, ttk
from datetime import datetime
from akunpengguna import baca_data_akun, simpan_data_akun, login_akun
from bacadata import baca_data_tabungan, simpan_data_ke_csv
from PIL import Image, ImageTk
import csv
import os


def format_rupiah(nilai):
    return f"{nilai:,.0f}".replace(",", ".")

def kosongkan_input_registrasi():
    entry_reg_username.delete(0, 'end')
    entry_reg_password.delete(0, 'end')

def login():
    global logged_in_user, tabungan_awal

    username = entry_username.get().strip()
    password = entry_password.get().strip()

    if not username or not password:
        messagebox.showerror("Kesalahan", "Username dan password tidak boleh kosong!")
        return

    # Proses login
    if login_akun(username, password):  
        logged_in_user = username  
        tabungan_awal = baca_data_tabungan(logged_in_user)  
        
        messagebox.showinfo("Berhasil", f"Selamat datang, {username}!")
        
        if label_saldo:
            label_saldo.config(text=f"Saldo Tabungan: Rp {format_rupiah(tabungan_awal)}")

        frame_login.pack_forget()
        frame_menu.pack()
    else:
        messagebox.showerror("Gagal", "Username atau password salah!")

def create_login_frame():
    global entry_username, entry_password

    canvas = Canvas(frame_login, width=1280, height=720)
    canvas.pack(fill="both", expand=True)

    bg_image = Image.open("background_login.jpg")  
    bg_image = bg_image.resize((1280, 720), Image.Resampling.LANCZOS)
    bg_photo = ImageTk.PhotoImage(bg_image)
    canvas.create_image(0, 0, image=bg_photo, anchor="nw")
    frame_login.bg_photo = bg_photo 

    canvas.create_text(942, 120, text="Login", font=("Belanosima", 35), fill="black")

    canvas.create_text(942, 230, text="Username", font=("Belanosima", 12), fill="black")
    entry_username = Entry(frame_login, bg='#D9D9D9', font=("Belanosima", 20))
    canvas.create_window(949, 265, window=entry_username, width=300)

    canvas.create_text(942, 325, text="Password", font=("Belanosima", 12), fill="black")
    entry_password = Entry(frame_login, show="*", bg='#D9D9D9', font=("Belanosima", 20))
    canvas.create_window(949, 360, window=entry_password, width=300)

    login_button = Button(frame_login, text="Login", command=login, bg='#D9D9D9')
    canvas.create_window(949, 425, window=login_button, width=100)

    register_button = Button(frame_login, text="Daftar Akun Baru", command=registrasi, bg='#D9D9D9')
    canvas.create_window(949, 479, window=register_button, width=150)

    frame_login.pack()

def registrasi():
    global entry_reg_username, entry_reg_password

    frame_login.pack_forget()
    for widget in frame_registrasi.winfo_children():
        widget.destroy()

    canvas_registrasi = Canvas(frame_registrasi, width=1280, height=720)
    canvas_registrasi.pack(fill="both", expand=True)

    bg_image = Image.open("background_registrasi.jpg")  
    bg_image = bg_image.resize((1280, 720), Image.Resampling.LANCZOS) 
    bg_photo = ImageTk.PhotoImage(bg_image)
    canvas_registrasi.create_image(0, 0, image=bg_photo, anchor="nw")  
    frame_registrasi.bg_photo = bg_photo

    canvas_registrasi.create_text(942, 120, text="Registrasi Akun Baru", font=("Belanosima", 35), fill="black")
    canvas_registrasi.create_text(942, 230, text="Username", font=("Belanosima", 12), fill="black")
    entry_reg_username = Entry(frame_registrasi, bg='#D9D9D9', font=("Belanosima", 20))
    canvas_registrasi.create_window(949, 265, window=entry_reg_username, width=300)

    canvas_registrasi.create_text(942, 325, text="Password", font=("Belanosima", 12), fill="black")
    entry_reg_password = Entry(frame_registrasi, show="*", bg='#D9D9D9', font=("Belanosima", 20))
    canvas_registrasi.create_window(949, 360, window=entry_reg_password, width=300)

    def simpan_akun():
        username = entry_reg_username.get()
        password = entry_reg_password.get()
        
        if not username or not password:
            messagebox.showerror("Kesalahan", "Username dan password tidak boleh kosong!")
            return
    
        akun_data = baca_data_akun()
        if username in akun_data:
            messagebox.showerror("Kesalahan", "Username sudah terdaftar!")
        else:
            simpan_data_akun(username, password)
            messagebox.showinfo("Berhasil", "Registrasi berhasil! Silakan login.")

        entry_username.delete(0, 'end')
        entry_password.delete(0, 'end')

        frame_registrasi.pack_forget()
        frame_login.pack()

    daftar_button = Button(frame_registrasi, text="Daftar", command=simpan_akun, bg='#D9D9D9')
    canvas_registrasi.create_window(949, 425, window=daftar_button, width=100)

    kembali_button = Button(frame_registrasi, text="Kembali", command=lambda: [frame_registrasi.pack_forget(), frame_login.pack()], bg='#D9D9D9')
    canvas_registrasi.create_window(949, 479, window=kembali_button, width=100)

    frame_registrasi.pack()

def mulai_menabung():
    global jumlah_hari, target_tabungan, target_per_hari, hari_ke, tabungan_awal, menabung_aktif, jumlah_menabung, target_harian, total_tabungan, sisa_target

    tabungan_awal = baca_data_tabungan(logged_in_user)
    total_tabungan = 0 

    try:
        target_tabungan = float(entry_target.get().replace('.', '').replace(',', '.'))
        jumlah_hari = int(entry_hari.get())
        if target_tabungan <= 0 or jumlah_hari <= 0:
            raise ValueError

        target_per_hari = round((target_tabungan / jumlah_hari) / 1000) * 1000

        total_target_bulanan = target_per_hari * jumlah_hari

        sisa_pembulanan = target_tabungan - total_target_bulanan

        target_harian = [target_per_hari] * jumlah_hari

        target_harian[0] += sisa_pembulanan

        target_tabungan = sum(target_harian)

        sisa_target = target_tabungan - total_tabungan

        jumlah_hari = jumlah_hari

        hari_ke = 1
        jumlah_menabung = 0
        menabung_aktif = True

        label_saldo.config(text=f"Saldo Tabungan: Rp {format_rupiah(tabungan_awal)}")

        frame_menabung.pack_forget()
        menabung_harian(hari_ke)

    except ValueError:
        messagebox.showerror("Kesalahan Input", "Masukkan nilai yang valid untuk target dan jumlah hari!")

def create_menabung_frame():
    global entry_target, entry_hari

    canvas_menabung = Canvas(frame_menabung, width=1280, height=720)
    canvas_menabung.pack(fill="both", expand=True)

    bg_image = Image.open("background_menabung.jpg")  
    bg_image = bg_image.resize((1280, 720), Image.Resampling.LANCZOS)  
    bg_photo = ImageTk.PhotoImage(bg_image)
    canvas_menabung.create_image(0, 0, image=bg_photo, anchor="nw")  
    frame_menabung.bg_photo = bg_photo

    canvas_menabung.create_text(640, 52, text="Mulai Menabung", font=("Belanosima", 30), fill="black")

    canvas_menabung.create_text(640, 173, text="Masukkan Target Tabungan (Rp):", font=("Belanosima", 20), fill="black")
    entry_target = Entry(frame_menabung, bg='#D9D9D9', font=("Belanosima", 20))
    canvas_menabung.create_window(640, 228, window=entry_target, width=300)

    canvas_menabung.create_text(640, 307, text="Masukkan Jumlah Hari:", font=("Belanosima", 20), fill="black")
    entry_hari = Entry(frame_menabung, bg='#D9D9D9', font=("Belanosima", 20))
    canvas_menabung.create_window(640, 360, window=entry_hari, width=300)

    tombol_mulai = Button(frame_menabung, text="Mulai", command=mulai_menabung, width=25)
    canvas_menabung.create_window(740, 540, window=tombol_mulai, width=700)

    tombol_kembali = Button(frame_menabung, text="Kembali", command=lambda: [frame_menabung.pack_forget(), frame_menu.pack()], width=25)
    canvas_menabung.create_window(315, 540, window=tombol_kembali, width=100)

def menabung_harian(hari_ke):
    global tabungan_awal, target_harian, menabung_aktif, label_saldo, jumlah_menabung, total_tabungan, target_tabungan, jumlah_hari, sisa_target

    sisa_target = target_tabungan - total_tabungan

    def lanjutkan():
        global tabungan_awal, hari_ke, menabung_aktif, jumlah_menabung, total_tabungan, target_tabungan, sisa_target

        tabungan_awal += target_harian[hari_ke - 1]
        total_tabungan += target_harian[hari_ke - 1]
        simpan_data_ke_csv(logged_in_user, tabungan_awal, f"Menabung hari ke-{hari_ke}", hari_ke)
        label_saldo.config(text=f"Saldo Tabungan: Rp {format_rupiah(tabungan_awal)}")
        messagebox.showinfo("Berhasil", f"Anda telah menabung di hari ke-{hari_ke}!")

        hari_ke += 1
        jumlah_menabung += 1

        sisa_target = target_tabungan - total_tabungan 

        if hari_ke <= jumlah_hari:
            frame_harian.pack_forget()
            frame_menu.pack()
        else:
            if sisa_target > 0:
                messagebox.showinfo("Selesai", 
                    f"Target masih kurang Rp {format_rupiah(sisa_target)}.\n" +
                    "Anda bisa memperpanjang periode menabung untuk mencapai target.")
                tambah_hari(sisa_target) 
            else:
                messagebox.showinfo("Selesai", "Selamat! Anda telah menyelesaikan target menabung.")
            frame_harian.pack_forget()
            frame_menu.pack()

    def lewati():
        global hari_ke, menabung_aktif, jumlah_menabung, total_tabungan, sisa_target
        simpan_data_ke_csv(logged_in_user, tabungan_awal, f"Tidak menabung hari ke-{hari_ke}", hari_ke)
        messagebox.showinfo("Lewati", f"Anda melewati menabung di hari ke-{hari_ke}.")
        hari_ke += 1

        sisa_target = target_tabungan - total_tabungan

        if hari_ke <= jumlah_hari:
            frame_harian.pack_forget()
            frame_menu.pack()
        else:
            if sisa_target > 0:
                messagebox.showinfo("Selesai", 
                    f"Target masih kurang Rp {format_rupiah(sisa_target)}.\n" +
                    "Anda bisa memperpanjang periode menabung untuk mencapai target.")
                tambah_hari(sisa_target) 
            else:
                messagebox.showinfo("Selesai", "Selamat! Anda telah menyelesaikan target menabung.")
            frame_harian.pack_forget()
            frame_menu.pack()

    if hari_ke > jumlah_hari:
        messagebox.showinfo("Selesai", "Proses menabung selesai.")
        return

    frame_menu.pack_forget()
    for widget in frame_harian.winfo_children():
        widget.destroy()

    canvas_harian = Canvas(frame_harian, width=1280, height=720)
    canvas_harian.pack(fill="both", expand=True)

    bg_image = Image.open("background_harian.jpg")  
    bg_image = bg_image.resize((1280, 720), Image.Resampling.LANCZOS)  
    bg_photo = ImageTk.PhotoImage(bg_image)
    canvas_harian.create_image(0, 0, image=bg_photo, anchor="nw")  
    frame_harian.bg_photo = bg_photo

    if hari_ke == 1:
        teks_target_hari_ini = f"Target Hari Pertama: Rp {format_rupiah(target_harian[hari_ke - 1])}"
    else:
        teks_target_hari_ini = f"Target Hari Ini: Rp {format_rupiah(target_harian[hari_ke - 1])}"

    sisa_target = target_tabungan - total_tabungan

    canvas_harian.create_text(640, 180, text=f"Hari ke-{hari_ke}/{jumlah_hari}", font=("Belanosima", 25), fill="black")
    canvas_harian.create_text(640, 280, text=f"Saldo Tabungan: Rp {format_rupiah(tabungan_awal)}", font=("Belanosima", 25), fill="black")
    canvas_harian.create_text(640, 230, text=f"Total Target: Rp {format_rupiah(target_tabungan)}   |   {teks_target_hari_ini}", font=("Belanosima", 25), fill="black")
    
    tombol_menabung = Button(frame_harian, text="Menabung", command=lanjutkan, font=("Belanosima", 13))
    tombol_lewati = Button(frame_harian, text="Tidak Menabung", command=lewati, font=("Belanosima", 13))
    
    canvas_harian.create_window(640, 380, window=tombol_menabung)  
    canvas_harian.create_window(640, 430, window=tombol_lewati)  

    frame_harian.pack()

def tambah_hari(sisa_target=0):
    def perpanjang():
        global jumlah_hari, target_tabungan, target_per_hari, hari_ke, tabungan_awal, menabung_aktif, jumlah_menabung, target_harian, total_tabungan, sisa_target
        try:
            tambahan_hari = int(entry_tambahan_hari.get())
            if tambahan_hari <= 0:
                raise ValueError

            tambahan_target = sisa_target if sisa_target > 0 else float(entry_tambahan_target.get().replace('.', '').replace(',', '.'))
            if tambahan_target <= 0:
                raise ValueError

            previous_total = total_tabungan

            target_per_hari = round((tambahan_target / tambahan_hari) / 1000) * 1000

            total_target_bulanan = target_per_hari * tambahan_hari

            sisa_pembulanan = tambahan_target - total_target_bulanan

            target_harian = [target_per_hari] * tambahan_hari

            target_harian[0] += sisa_pembulanan

            target_tabungan = sum(target_harian)

            sisa_target = target_tabungan 

            jumlah_hari = tambahan_hari

            hari_ke = 1
            jumlah_menabung = 0
            menabung_aktif = True
            total_tabungan = 0 

            label_saldo.config(text=f"Saldo Tabungan: Rp {format_rupiah(tabungan_awal)}")

            frame_tambah_hari.pack_forget()
            frame_menu.pack()

            menabung_harian(hari_ke)

        except ValueError:
            messagebox.showerror("Kesalahan Input", "Masukkan nilai yang valid untuk target dan jumlah hari tambahan!")

    frame_menu.pack_forget()
    for widget in frame_tambah_hari.winfo_children():
        widget.destroy()

    canvas_tambah_hari = Canvas(frame_tambah_hari, width=1280, height=720)
    canvas_tambah_hari.pack(fill="both", expand=True)

    bg_image = Image.open("background_tambah_hari.jpg")
    bg_image = bg_image.resize((1280, 720), Image.Resampling.LANCZOS)
    bg_photo = ImageTk.PhotoImage(bg_image)
    canvas_tambah_hari.create_image(0, 0, image=bg_photo, anchor="nw")

    frame_tambah_hari.bg_photo = bg_photo

    canvas_tambah_hari.create_text(640, 50, text="Perpanjang Target Menabung", font=("Belanosima", 30), fill="black")

    canvas_tambah_hari.create_text(640, 150, text="Tambahan Hari", font=("Belanosima", 20), fill="black")
    entry_tambahan_hari = Entry(frame_tambah_hari, font=("Belanosima", 15), bg="#D9D9D9")
    canvas_tambah_hari.create_window(640, 200, window=entry_tambahan_hari, width=300)

    if sisa_target > 0:
        tambahan_target_text = f"Sisa target: Rp {format_rupiah(sisa_target)}"
    else:
        tambahan_target_text = "Tambahan Target Tabungan"

    canvas_tambah_hari.create_text(640, 250, text=tambahan_target_text, font=("Belanosima", 20), fill="black")
    entry_tambahan_target = Entry(frame_tambah_hari, font=("Belanosima", 15), bg="#D9D9D9", state="normal")
    if sisa_target > 0:
        entry_tambahan_target.insert(0, format_rupiah(sisa_target))
        entry_tambahan_target.config(state="readonly")
    canvas_tambah_hari.create_window(640, 300, window=entry_tambahan_target, width=300)

    perpanjang_button = Button(frame_tambah_hari, text="Perpanjang", command=perpanjang, bg="#D9D9D9")
    canvas_tambah_hari.create_window(640, 400, window=perpanjang_button, width=150)

    frame_tambah_hari.pack()

def menarik_tabungan():
    global tabungan_awal, entry_tarikan, label_saldo, entry_target 

    def tarik():
        global tabungan_awal, jumlah_terakhir_ditarik
        try:
            jumlah = float(entry_tarikan.get().replace('.', '').replace(',', '.'))
            if jumlah > tabungan_awal:
                messagebox.showerror("Kesalahan", "Jumlah tarikan melebihi saldo!")
                return
            tabungan_awal -= jumlah
            jumlah_terakhir_ditarik = jumlah  
            simpan_data_ke_csv(logged_in_user, tabungan_awal, f"Menarik tabungan sebesar Rp {format_rupiah(jumlah)}", hari_ke - 1)
            label_saldo.config(text=f"Saldo Tabungan: Rp {format_rupiah(tabungan_awal)}")
            messagebox.showinfo("Berhasil", f"Anda berhasil menarik Rp {format_rupiah(jumlah)}!")
            frame_menarik.pack_forget()
            frame_menabung.pack()
            entry_target.delete(0, 'end')
            entry_target.insert(0, format_rupiah(jumlah_terakhir_ditarik))
        except ValueError:
            messagebox.showerror("Kesalahan Input", "Masukkan jumlah yang valid!")

    frame_menu.pack_forget()
    for widget in frame_menarik.winfo_children():
        widget.destroy()

    canvas_menarik = Canvas(frame_menarik, width=1280, height=720)
    canvas_menarik.pack(fill="both", expand=True)

    bg_image = Image.open("background_menarik.jpg") 
    bg_image = bg_image.resize((1280, 720), Image.Resampling.LANCZOS)  
    bg_photo = ImageTk.PhotoImage(bg_image)
    canvas_menarik.create_image(0, 0, image=bg_photo, anchor="nw")  
    
    frame_menarik.bg_photo = bg_photo

    canvas_menarik.create_text(640, 50, text="Menarik Tabungan", font=("Belanosima", 30), fill="black")
    canvas_menarik.create_text(640, 180, text=f"Saldo Tabungan: Rp {format_rupiah(tabungan_awal)}", font=("Belanosima", 25), fill="black")
    canvas_menarik.create_text(640, 250, text="Masukkan Jumlah yang Akan Ditarik (Rp):", font=("Belanosima", 20), fill="black")

    entry_tarikan = Entry(frame_menarik, bg='#D9D9D9', font=("Belanosima", 20))
    canvas_menarik.create_window(640, 320, window=entry_tarikan, width=300)

    tombol_tarikan = Button(frame_menarik, text="Tarik", command=tarik)
    canvas_menarik.create_window(740, 540, window=tombol_tarikan, width=700)

    tombol_kembali = Button(frame_menarik, text="Kembali", command=lambda: [frame_menarik.pack_forget(), frame_menu.pack()])
    canvas_menarik.create_window(315, 540, window=tombol_kembali, width=100)

    frame_menarik.pack()  

def cek_riwayat():
    global frame_riwayat, logged_in_user

    if not os.path.exists("data_tabungan.csv"):
        messagebox.showerror("Error", "File data_tabungan.csv tidak ditemukan!")
        return

    data = []
    try:
        with open("data_tabungan.csv", mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file, delimiter=';') 
            data = [row for row in reader if row.get("username") == logged_in_user]
    except Exception as e:
        messagebox.showerror("Error", f"Terjadi kesalahan saat membaca file: {e}")
        return

    if not data:
        messagebox.showinfo("Info", "Tidak ada riwayat untuk pengguna ini.")
        return

    frame_menu.pack_forget()
    for widget in frame_riwayat.winfo_children():
        widget.destroy()

    canvas_riwayat = Canvas(frame_riwayat, width=1280, height=720)
    canvas_riwayat.pack(fill="both", expand=True)

    bg_image = Image.open("background_riwayat.jpg")
    bg_image = bg_image.resize((1280, 720), Image.Resampling.LANCZOS)
    bg_photo = ImageTk.PhotoImage(bg_image)
    canvas_riwayat.create_image(0, 0, image=bg_photo, anchor="nw")
    frame_riwayat.bg_photo = bg_photo

    canvas_riwayat.create_text(640, 50, text="Riwayat Tabungan", font=("Belanosima", 30), fill="black")

    columns = ("tanggal", "keterangan", "hari", "saldo")
    tree = ttk.Treeview(frame_riwayat, columns=columns, show="headings", height=20)

    tree.heading("tanggal", text="Tanggal")
    tree.heading("keterangan", text="Keterangan")
    tree.heading("hari", text="Hari")
    tree.heading("saldo", text="Saldo")
    for col in columns:
        tree.column(col, width=200, anchor="center")

    for row in data:
        tree.insert("", "end", values=(row["tanggal"], row["keterangan"], row["hari"], row["saldo"]))

    tree.place(relx=0.5, rely=0.5, anchor="center")

    Button(
        frame_riwayat,
        text="Kembali",
        command=lambda: [frame_riwayat.pack_forget(), frame_menu.pack()], font=("Belanosima", 11),
        width=20
    ).place(relx=0.5, rely=0.92, anchor="center")

    frame_riwayat.pack()

def create_menu_frame():
    global label_saldo

    canvas_menu = Canvas(frame_menu, width=1280, height=720)
    canvas_menu.pack(fill="both", expand=True)

    bg_image = Image.open("background_menu.jpg")
    bg_image = bg_image.resize((1280, 720), Image.Resampling.LANCZOS)
    bg_photo = ImageTk.PhotoImage(bg_image)
    canvas_menu.create_image(0, 0, image=bg_photo, anchor="nw")

    frame_menu.bg_photo = bg_photo

    label_saldo = Label(frame_menu, text=f"Saldo Tabungan: Rp {format_rupiah(tabungan_awal)}", font=("Belanosima", 30), bg='white')
    label_saldo.place(relx=0.5, rely=0.150, anchor="center")
    
    Button(frame_menu, text="1. Lanjutkan Menabung", font=("Belanosima", 12), command=lambda: menabung_harian(hari_ke) if menabung_aktif else messagebox.showinfo("Informasi", "Mulai target baru dahulu."), width=25, bg='white').place(relx=0.5, rely=0.32, anchor="center")
    Button(frame_menu, text="2. Mulai Baru", font=("Belanosima", 12), command=lambda: [frame_menu.pack_forget(), frame_menabung.pack()], width=25, bg='white').place(relx=0.5, rely=0.41, anchor="center")
    Button(frame_menu, text="3. Menarik Tabungan", font=("Belanosima", 12), command=menarik_tabungan, width=25, bg='white').place(relx=0.5, rely=0.50, anchor="center")
    Button(frame_menu, text="4. Cek Riwayat", font=("Belanosima", 12), command=cek_riwayat, width=25, bg='white').place(relx=0.5, rely=0.59, anchor="center")
    Button(frame_menu, text="5. Keluar", font=("Belanosima", 12), command=lambda: [frame_menu.pack_forget(), frame_login.pack(), entry_username.delete(0, 'end'), entry_password.delete(0, 'end')], width=25, bg='white').place(relx=0.5, rely=0.68, anchor="center")

root = Tk()
root.title("Aplikasi Tabungan Harian")
root.geometry("1280x720")

frame_login = Frame(root)
frame_menu = Frame(root)
frame_registrasi = Frame(root)
frame_menabung = Frame(root)
frame_harian = Frame(root)
frame_menarik = Frame(root)
frame_tambah_hari = Frame(root)
frame_riwayat = Frame(root)

logged_in_user = None
tabungan_awal = baca_data_tabungan(logged_in_user)  
jumlah_hari = 0
target_tabungan = 0
target_per_hari = 0
hari_ke = 1
menabung_aktif = False
tabungan_awal = 0
jumlah_terakhir_ditarik = 0
label_saldo = None
entry_target = None
entry_hari = None 
total_tabungan = 0
sisa_target = 0


create_login_frame()
create_menu_frame()
create_menabung_frame()

root.mainloop()