import csv
from datetime import datetime

def simpan_data_ke_csv(tabungan_akhir, aktivitas, hari_ke, nama_file='data_tabungan.csv'):
    try:
        data = {
            "tabungan_akhir": tabungan_akhir,
            "aktivitas": aktivitas,
            "hari_ke": hari_ke,
            "tanggal_simpan": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        with open(nama_file, 'a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=["tabungan_akhir", "aktivitas", "hari_ke", "tanggal_simpan"])
            if file.tell() == 0:
                writer.writeheader()
            writer.writerow(data)
    except IOError as e:
        print(f"Terjadi kesalahan saat menyimpan data: {e}")

def baca_data_dari_csv(nama_file='data_tabungan.csv'):
    try:
        with open(nama_file, 'r', newline='') as file:
            reader = csv.DictReader(file)
            rows = list(reader)
            if rows:
                return float(rows[-1]['tabungan_akhir'])  # Ambil saldo terakhir
            return 0.0
    except FileNotFoundError:
        return 0.0
