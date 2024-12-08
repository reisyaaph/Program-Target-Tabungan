import csv
from datetime import datetime
import os

def baca_data_tabungan(username):
    filename = "data_tabungan.csv"
    if not os.path.exists(filename):
        return 0  # Saldo awal jika file belum ada
    with open(filename, newline='', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter=';')
        next(reader, None)  # Lewati header
        saldo = 0
        for row in reader:
            if row[0] == username:  # Filter data berdasarkan username
                saldo = float(row[4])  # Ambil saldo terakhir
        return saldo

# Fungsi untuk menyimpan data tabungan
def simpan_data_ke_csv(username, saldo, keterangan, hari):
    filename = "data_tabungan.csv"
    mode = 'a' if os.path.exists(filename) else 'w'
    with open(filename, mode, newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=';')
        if mode == 'w':  # Tulis header hanya jika file baru
            writer.writerow(['username', 'tanggal', 'keterangan', 'hari', 'saldo'])
        writer.writerow([
            username,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            keterangan,
            hari,
            saldo
        ])