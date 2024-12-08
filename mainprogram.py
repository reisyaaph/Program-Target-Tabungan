from datetime import datetime, timedelta
from tkinter import Tk, Frame, Label, Entry, Button, messagebox, Canvas
from bacadata import simpan_data_ke_csv, baca_data_dari_csv
from akunpengguna import baca_data_akun, simpan_data_akun, daftar_akun, login_akun
from PIL import Image, ImageTk

def format_rupiah(nilai):
    return f"{nilai:,.0f}"

def kosongkan_input_registrasi():
    entry_reg_username.delete(0, 'end')
    entry_reg_password.delete(0, 'end')

def login():
    global logged_in_user, tabungan_awal
    username = entry_username.get()
    password = entry_password.get()

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

    canvas.create_text(942, 150, text="Login", font=("Belanosima", 25), fill="black")
    canvas.create_text(942, 210, text="Username", font=("Belanosima", 12), fill="black")
    entry_username = Entry(frame_login, bg='#D9D9D9', font=("Belanosima", 20))
    canvas.create_window(949, 265, window=entry_username, width=300)

    canvas.create_text(942, 310, text="Password", font=("Belanosima", 12), fill="black")
    entry_password = Entry(frame_login, show="*", bg='#D9D9D9', font=("Belanosima", 20))
    canvas.create_window(949, 360, window=entry_password, width=300)

    login_button = Button(frame_login, text="Login", command=login, bg='#D9D9D9')
    canvas.create_window(949, 495, window=login_button, width=100,)

    register_button = Button(frame_login, text="Daftar Akun Baru", command=registrasi, bg='#D9D9D9')
    canvas.create_window(949,559, window=register_button, width=150)

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

    canvas_registrasi.create_text(942, 150, text="Registrasi Akun Baru", font=("Belanosima", 24), fill="black")
    canvas_registrasi.create_text(942, 210, text="Username", font=("Belanosima", 12), fill="black")
    entry_reg_username = Entry(frame_registrasi, bg='#D9D9D9', font=("Belanosima", 20))
    canvas_registrasi.create_window(949, 265, window=entry_reg_username, width=300)

    canvas_registrasi.create_text(942, 310, text="Password", font=("Belanosima", 12), fill="black")
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
    canvas_registrasi.create_window(949, 495, window=daftar_button, width=100)

    kembali_button = Button(frame_registrasi, text="Kembali", command=lambda: [frame_registrasi.pack_forget(), frame_login.pack()], bg='#D9D9D9')
    canvas_registrasi.create_window(949,559, window=kembali_button, width=100)

    frame_registrasi.pack()

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
        menabung_aktif = True  
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

def create_menu_frame():
    global label_saldo  

    canvas_menu = Canvas(frame_menu, width=1280, height=720)
    canvas_menu.pack(fill="both", expand=True)

    bg_image = Image.open("background_menu.jpg")  
    bg_image = bg_image.resize((1280, 720), Image.Resampling.LANCZOS)  
    bg_photo = ImageTk.PhotoImage(bg_image)
    canvas_menu.create_image(0, 0, image=bg_photo, anchor="nw")  

    frame_menu.bg_photo = bg_photo

    label_saldo = Label(frame_menu, text=f"Saldo Tabungan: Rp {format_rupiah(tabungan_awal)}", font=("Belanosima", 20), bg='white')
    label_saldo.place(relx=0.5, rely=0.372, anchor="center")
    
    Button(frame_menu, text="1. Lanjutkan Menabung", command=lambda: menabung_harian(hari_ke) if menabung_aktif else messagebox.showinfo("Informasi", "Mulai target baru dahulu."), width=25, bg='white').place(relx=0.5, rely=0.52, anchor="center")
    Button(frame_menu, text="2. Mulai Baru", command=lambda: [frame_menu.pack_forget(), frame_menabung.pack()], width=25, bg='white').place(relx=0.5, rely=0.63, anchor="center")
    Button(frame_menu, text="3. Menarik Tabungan", command=menarik_tabungan, width=25, bg='white').place(relx=0.5, rely=0.74, anchor="center")
    Button(frame_menu, text="4. Keluar", command=lambda: [frame_menu.pack_forget(), frame_login.pack(), entry_username.delete(0, 'end'), entry_password.delete(0, 'end')], width=25, bg='white').place(relx=0.5, rely=0.85, anchor="center")


frame_login = Frame(root)
frame_menu = Frame(root)
frame_registrasi = Frame(root)
frame_menabung = Frame(root)
frame_harian = Frame(root)
frame_menarik = Frame(root)

create_login_frame()
create_menu_frame()
create_menabung_frame()

root.mainloop()