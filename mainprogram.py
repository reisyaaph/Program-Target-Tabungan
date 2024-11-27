import csv
from datetime import datetime, timedelta
from bacadata import simpan_data_ke_csv, baca_data_dari_csv

def simpan_data_ke_csv(tabungan_akhir, aktivitas):  
    nama_file = 'data_tabungan.csv'
    try:
        data = {
            "tabungan_akhir": tabungan_akhir,
            "aktivitas": aktivitas,
            "tanggal_simpan": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        with open(nama_file, 'a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=["tabungan_akhir", "aktivitas", "tanggal_simpan"])
            if file.tell() == 0:
                writer.writeheader()  
            writer.writerow(data)  
    except IOError as e:
        print(f"Terjadi kesalahan saat menyimpan data: {e}")

def baca_data_dari_csv(nama_file='data_tabungan.csv'):
    try:
        with open(nama_file, 'r', newline='') as file:
            reader = csv.DictReader(file)
            data = list(reader)
        return data
    except FileNotFoundError:
        return []

def format_rupiah(nilai):
    return f"{nilai:,.0f}"

def main():
    data_tabungan = baca_data_dari_csv()
    if data_tabungan:
        tabungan_awal = float(data_tabungan["tabungan_akhir"])
        tabungan_akhir = tabungan_awal
        print("Informasi Tabungan")
        print("Total tabungan anda saat ini: {tabungan_akhir}\n")
    else:
        tabungan_awal = float(input("Masukkan jumlah total tabungan yang Anda miliki saat ini: "))
        tabungan_akhir = tabungan_awal
        print("Informasi Tabungan")
        print("Total tabungan Anda saat ini: {tabungan_awal}\n")

    while True:
        print("Pilihan:")
        print("1. Menabung")
        print("2. Menarik tabungan")
        print("3. Keluar") 
        pilihan_awal = input("Pilih opsi (1/2/3): ")

        if pilihan_awal == "1":
            target_tambahan = float(input("Masukkan jumlah target tabungan tambahan: "))
            jumlah_hari = int(input("Masukkan jumlah hari untuk mencapai target tambahan ini: "))

            tabungan_per_hari = target_tambahan / jumlah_hari

            print("\n--- Program Tabungan Harian ---")
            print(f"Target tambahan yang ingin dicapai:", target_tambahan)
            print(f"Jumlah hari yang ditentukan:", jumlah_hari)
            print(f"Target tabungan per hari: {tabungan_per_hari}\n")
        
        elif pilihan_awal == '2':
            jumlah_tarikan = float(input("Masukkan jumlah tabungan yang ingin Anda tarik: "))
            
            if jumlah_tarikan <= tabungan_akhir:
                tabungan_akhir -= jumlah_tarikan
                print("Anda berhasil menarik tabungan sebesar:", jumlah_tarikan)
                print("Sisa tabungan Anda sekarang: {tabungan_akhir}\n")
                
                jumlah_hari = int(input("Berapa hari Anda ingin menabung untuk mencapai target ini? "))
                tanggal_mulai = input("Masukkan tanggal mulai menabung kembali (format: YYYY-MM-DD): ")
                
                tanggal_mulai = datetime.strptime(tanggal_mulai, "%Y-%m-%d")
                tabungan_per_hari = jumlah_tarikan / jumlah_hari

                print("\n--- Program Tabungan Harian ---")
                print(f"Target yang ingin dicapai:", jumlah_tarikan)
                print(f"Jumlah hari yang ditentukan:", jumlah_hari)
                print(f"Target tabungan per hari:", tabungan_per_hari)
                print(f"Tabungan akan dimulai pada tanggal: {tanggal_mulai.strftime('%Y-%m-%d')}\n")

            else:
                print("Jumlah tarikan melebihi total tabungan yang dimiliki. Tidak dapat melakukan penarikan.")

        elif pilihan_awal == '3':
            break
        
        else:
            print("Pilihan tidak valid. Silakan pilih opsi yang tersedia.")

    print("\n--- Program Selesai ---")
    print("Total tabungan Anda sekarang (tabungan akhir):", tabungan_akhir)

main()
