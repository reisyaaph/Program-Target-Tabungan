from tkinter import Tk, Frame, Label, Entry, Button, messagebox, Canvas
from datetime import datetime
from akunpengguna import baca_data_akun, simpan_data_akun, login_akun
from bacadata import baca_data_tabungan, simpan_data_ke_csv
from PIL import Image, ImageTk


def format_rupiah(nilai):
    return f"{nilai:,.0f}".replace(",", ".")

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

# Mulai menabung
def mulai_menabung():
    global jumlah_hari, target_tabungan, target_per_hari, hari_ke, tabungan_awal, menabung_aktif, label_saldo
    try:
        target_tabungan = float(entry_target.get().replace('.', '').replace(',', '.'))
        jumlah_hari = int(entry_hari.get())
        if target_tabungan <= 0 or jumlah_hari <= 0:
            raise ValueError

        target_per_hari = target_tabungan / jumlah_hari
        hari_ke = 1
        menabung_aktif = True
        frame_menabung.pack_forget()
        menabung_harian(hari_ke)
    except ValueError:
        messagebox.showerror("Kesalahan Input", "Masukkan nilai yang valid untuk target dan jumlah hari!")

def create_menabung_frame():
    global entry_target, entry_hari

    # Buat Canvas untuk menampilkan gambar latar belakang
    canvas_menabung = Canvas(frame_menabung, width=1280, height=720)
    canvas_menabung.pack(fill="both", expand=True)

    # Muat gambar latar belakang
    bg_image = Image.open("background_menabung.jpg")  # Ganti dengan nama file gambar Anda
    bg_image = bg_image.resize((1280, 720), Image.Resampling.LANCZOS)  # Ganti dengan Image.Resampling.LANCZOS
    bg_photo = ImageTk.PhotoImage(bg_image)
    canvas_menabung.create_image(0, 0, image=bg_photo, anchor="nw")

    # Simpan referensi gambar agar tidak hilang saat garbage collection
    frame_menabung.bg_photo = bg_photo

    # Tambahkan elemen UI ke Canvas
    canvas_menabung.create_text(640, 52, text="Mulai Menabung", font=("Belanosima", 30), fill="black")

    # Form untuk memasukkan target tabungan
    canvas_menabung.create_text(640, 173, text="Masukkan Target Tabungan (Rp):", font=("Belanosima", 20), fill="black")
    entry_target = Entry(frame_menabung, bg='#D9D9D9', font=("Belanosima", 20))
    canvas_menabung.create_window(640, 228, window=entry_target, width=300)

    # Form untuk memasukkan jumlah hari
    canvas_menabung.create_text(640, 307, text="Masukkan Jumlah Hari:", font=("Belanosima", 20), fill="black")
    entry_hari = Entry(frame_menabung, bg='#D9D9D9', font=("Belanosima", 20))
    canvas_menabung.create_window(640, 360, window=entry_hari, width=300)

    # Tombol untuk memulai menabung
    tombol_mulai = Button(frame_menabung, text="Mulai", command=mulai_menabung, width=25)
    canvas_menabung.create_window(780, 620, window=tombol_mulai, width=700)

    # Tombol untuk kembali ke menu
    tombol_kembali = Button(frame_menabung, text="Kembali", command=lambda: [frame_menabung.pack_forget(), frame_menu.pack()], width=25)
    canvas_menabung.create_window(198, 620, window=tombol_kembali, width=100)

# Menabung harian
def menabung_harian(hari_ke):
    global tabungan_awal, target_per_hari, menabung_aktif, label_saldo

    def lanjutkan():
        global tabungan_awal, hari_ke, menabung_aktif
        tabungan_awal += target_per_hari
        simpan_data_ke_csv(logged_in_user, tabungan_awal, f"Menabung hari ke-{hari_ke}", hari_ke)
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
        simpan_data_ke_csv(logged_in_user, tabungan_awal, f"Tidak menabung hari ke-{hari_ke}", hari_ke)
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

    # Buat Canvas untuk menampilkan gambar latar belakang
    canvas_harian = Canvas(frame_harian, width=1280, height=720)
    canvas_harian.pack(fill="both", expand=True)

    # Muat gambar latar belakang
    bg_image = Image.open("background_harian.jpg")  # Ganti dengan nama file gambar Anda
    bg_image = bg_image.resize((1280, 720), Image.Resampling.LANCZOS)  # Ganti dengan Image.Resampling.LANCZOS
    bg_photo = ImageTk.PhotoImage(bg_image)
    canvas_harian.create_image(0, 0, image=bg_photo, anchor="nw")  # Tambahkan gambar ke canvas

    # Simpan referensi gambar agar tidak hilang saat garbage collection
    frame_harian.bg_photo = bg_photo

    # Tambahkan elemen UI ke Canvas
    canvas_harian.create_text(640, 50, text=f"Hari ke-{hari_ke}/{jumlah_hari}", font=("Belanosima", 35), fill="black")
    canvas_harian.create_text(640, 120, text=f"Saldo Tabungan: Rp {format_rupiah(tabungan_awal)}", font=("Belanosima", 25), fill="black")

    # Tambahkan tombol ke dalam canvas
    tombol_menabung = Button(frame_harian, text="Menabung", command=lanjutkan)
    tombol_lewati = Button(frame_harian, text="Tidak Menabung", command=lewati)
    
    # Letakkan tombol di dalam canvas dengan create_window
    canvas_harian.create_window(640, 318, window=tombol_menabung)  # Menabung di posisi (640, 200)
    canvas_harian.create_window(640, 402, window=tombol_lewati)  # Tidak Menabung di posisi (640, 250)

    frame_harian.pack()  # Tampilkan frame_harian

# Menarik tabungan
def menarik_tabungan():
    global tabungan_awal, entry_tarikan, label_saldo, entry_target  # Tambahkan entry_tarikan sebagai variabel global

    def tarik():
        global tabungan_awal, jumlah_terakhir_ditarik
        try:
            jumlah = float(entry_tarikan.get().replace('.', '').replace(',', '.'))
            if jumlah > tabungan_awal:
                messagebox.showerror("Kesalahan", "Jumlah tarikan melebihi saldo!")
                return
            tabungan_awal -= jumlah
            jumlah_terakhir_ditarik = jumlah  # Simpan jumlah yang ditarik
            simpan_data_ke_csv(logged_in_user, tabungan_awal, f"Menarik tabungan sebesar Rp {format_rupiah(jumlah)}", hari_ke - 1)
            label_saldo.config(text=f"Saldo Tabungan: Rp {format_rupiah(tabungan_awal)}")
            messagebox.showinfo("Berhasil", f"Anda berhasil menarik Rp {format_rupiah(jumlah)}!")
            frame_menarik.pack_forget()
            frame_menabung.pack()
            # Isi otomatis input target tabungan
            entry_target.delete(0, 'end')
            entry_target.insert(0, format_rupiah(jumlah_terakhir_ditarik))
        except ValueError:
            messagebox.showerror("Kesalahan Input", "Masukkan jumlah yang valid!")

    frame_menu.pack_forget()
    for widget in frame_menarik.winfo_children():
        widget.destroy()

    # Buat Canvas untuk menampilkan gambar latar belakang
    canvas_menarik = Canvas(frame_menarik, width=1280, height=720)
    canvas_menarik.pack(fill="both", expand=True)

    # Muat gambar latar belakang
    bg_image = Image.open("background_menarik.jpg")  # Ganti dengan nama file gambar Anda
    bg_image = bg_image.resize((1280, 720), Image.Resampling.LANCZOS)  # Ganti dengan Image.Resampling.LANCZOS
    bg_photo = ImageTk.PhotoImage(bg_image)
    canvas_menarik.create_image(0, 0, image=bg_photo, anchor="nw")  # Tambahkan gambar ke canvas

    # Simpan referensi gambar agar tidak hilang saat garbage collection
    frame_menarik.bg_photo = bg_photo

    # Tambahkan elemen UI ke Canvas
    canvas_menarik.create_text(640, 50, text="Menarik Tabungan", font=("Belanosima", 35), fill="black")
    canvas_menarik.create_text(640, 120, text=f"Saldo Tabungan: Rp {format_rupiah(tabungan_awal)}", font=("Belanosima", 25), fill="black")
    canvas_menarik.create_text(640, 300, text="Masukkan Jumlah yang Akan Ditarik (Rp):", font=("Belanosima", 20), fill="black")

    # Input untuk jumlah yang akan ditarik
    entry_tarikan = Entry(frame_menarik, bg='#D9D9D9', font=("Belanosima", 20))
    canvas_menarik.create_window(640, 360, window=entry_tarikan, width=300)

    # Tombol tarik
    tombol_tarikan = Button(frame_menarik, text="Tarik", command=tarik)
    canvas_menarik.create_window(780, 620, window=tombol_tarikan, width=700)

    # Tombol kembali ke menu
    tombol_kembali = Button(frame_menarik, text="Kembali", command=lambda: [frame_menarik.pack_forget(), frame_menu.pack()])
    canvas_menarik.create_window(193, 620, window=tombol_kembali, width=100)

    frame_menarik.pack()  # Tampilkan frame_menarik


# Setup UI
root = Tk()
root.title("Aplikasi Tabungan Harian")
root.geometry("1280x720")

# Variabel Global
logged_in_user = None
tabungan_awal = baca_data_tabungan(logged_in_user)  # Panggil dengan username yang sedang login
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

def create_menu_frame():
    global label_saldo  # Pastikan label_saldo adalah variabel global

    # Buat Canvas untuk menampilkan gambar latar belakang
    canvas_menu = Canvas(frame_menu, width=1280, height=720)
    canvas_menu.pack(fill="both", expand=True)

    # Muat gambar latar belakang
    bg_image = Image.open("background_menu.jpg")  # Ganti dengan nama file gambar Anda
    bg_image = bg_image.resize((1280, 720), Image.Resampling.LANCZOS)  # Ganti dengan Image.Resampling.LANCZOS
    bg_photo = ImageTk.PhotoImage(bg_image)
    canvas_menu.create_image(0, 0, image=bg_photo, anchor="nw")  # Tambahkan gambar ke canvas

    # Simpan referensi gambar agar tidak hilang saat garbage collection
    frame_menu.bg_photo = bg_photo

    # Pastikan label_saldo dibuat di sini dan ditampilkan dengan format
    label_saldo = Label(frame_menu, text=f"Saldo Tabungan: Rp {format_rupiah(tabungan_awal)}", font=("Belanosima", 20), bg='white')
    label_saldo.place(relx=0.5, rely=0.372, anchor="center")  # Letakkan label di tengah-tengah
    
    # Pastikan tombol muncul dengan jelas
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

# Create Frames
create_login_frame()
create_menu_frame()
create_menabung_frame()

root.mainloop()