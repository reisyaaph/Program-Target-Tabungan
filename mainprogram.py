import csv
from datetime import datetime, timedelta
from bacadata import simpan_data_ke_csv, baca_data_dari_csv

def format_rupiah(nilai):
    return f"{nilai:,.0f}"

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
