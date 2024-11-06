def main():
    # Input jumlah total tabungan yang dimiliki pengguna
    total_tabungan_saat_ini = int(input("Masukkan jumlah total tabungan yang Anda miliki saat ini: "))
    
    # Menampilkan jumlah tabungan yang dimiliki
    print("\n--- Informasi Tabungan ---")
    print(f"Total tabungan Anda saat ini: {total_tabungan_saat_ini}\n")
    
    # Menanyakan apakah pengguna ingin menambah atau menarik tabungan
    while True:
        pilihan_awal = input("Apakah Anda ingin (t) menabung atau (n) menarik tabungan? (t/n): ").lower()
        
        if pilihan_awal == 't':
            # Input jumlah target tabungan tambahan dan jumlah hari dari pengguna
            target_tambahan = int(input("Masukkan jumlah target tabungan tambahan: "))
            jumlah_hari = int(input("Masukkan jumlah hari untuk mencapai target tambahan ini: "))