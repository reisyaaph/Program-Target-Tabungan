import csv
from datetime import datetime, timedelta

def simpan_data_ke_csv(tabungan_akhir, nama_file='data_tabungan.csv'):
    try:
        data = {
            "tabungan_akhir": tabungan_akhir,
            "tanggal_simpan": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # Mengecek apakah file CSV sudah ada untuk menambah data
        try:
            with open(nama_file, 'r', newline='') as file:
                reader = csv.DictReader(file)
                # Mengecek apakah data sudah ada
                if not any(row["tanggal_simpan"] == data["tanggal_simpan"] for row in reader):
                    with open(nama_file, 'a', newline='') as append_file:
                        writer = csv.DictWriter(append_file, fieldnames=["tabungan_akhir", "tanggal_simpan"])
                        writer.writerow(data)
        except FileNotFoundError:
            with open(nama_file, 'w', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=["tabungan_akhir", "tanggal_simpan"])
                writer.writeheader()
                writer.writerow(data)

        print(f"Data berhasil disimpan ke {nama_file}")
    except IOError as e:
        print(f"Terjadi kesalahan saat menyimpan data: {e}")

def baca_data_dari_csv(nama_file='data_tabungan.csv'):
    try:
        with open(nama_file, 'r', newline='') as file:
            reader = csv.DictReader(file)
            data = list(reader)
        if data:
            return data[-1]  # Mengambil data terakhir
        else:
            return None
    except FileNotFoundError:
        print(f"File {nama_file} tidak ditemukan. Data tabungan awal digunakan.")
        return None
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")
        return None

def main():
    # Coba membaca data tabungan yang disimpan sebelumnya
    data_tabungan = baca_data_dari_csv()

    if data_tabungan:
        # Jika data ada, mulai dari tabungan akhir yang tersimpan
        tabungan_awal = float(data_tabungan['tabungan_akhir'])
        tabungan_akhir = tabungan_awal
        print("\n--- Data Tabungan Tersimpan ---")
        print(f"Tabungan Akhir (terakhir kali disimpan): {tabungan_akhir}")
    else:
        tabungan_awal = float(input("Masukkan jumlah total tabungan yang Anda miliki saat ini: "))
        tabungan_akhir = tabungan_awal
        print("\n--- Informasi Tabungan ---")
        print(f"Total tabungan Anda saat ini (tabungan awal): {tabungan_awal}\n")

    while True:
        print("\nPilihan:")
        print("1. Menabung")
        print("2. Menarik tabungan")
        print("3. Keluar")  # Reset tabungan dihapus
        pilihan_awal = input("Pilih opsi (1/2/3): ").lower()

        if pilihan_awal == '1':
            # Input jumlah target tabungan tambahan dan jumlah hari dari pengguna
            target_tambahan = float(input("Masukkan jumlah target tabungan tambahan: "))
            jumlah_hari = int(input("Masukkan jumlah hari untuk mencapai target tambahan ini: "))

            # Hitung jumlah tabungan per hari untuk mencapai target tambahan
            tabungan_per_hari = target_tambahan / jumlah_hari

            print("\n--- Program Tabungan Harian ---")
            print(f"Target tambahan yang ingin dicapai: {target_tambahan}")
            print(f"Jumlah hari yang ditentukan: {jumlah_hari}")
            print(f"Target tabungan per hari: {tabungan_per_hari:.2f}\n")

            hari = 1  # Mulai perhitungan dari hari pertama
            target_tercapai = False  # Flag untuk memeriksa apakah target tercapai

            while hari <= jumlah_hari:
                print(f"Hari {hari} - Target hari ini: {tabungan_per_hari:.2f}")
                menabung = input("Apakah Anda sudah menabung hari ini? (y/n): ")

                if menabung.lower() == 'y':
                    tabungan_akhir += tabungan_per_hari
                    print("Anda berhasil menabung sesuai target hari ini!")

                else:
                    print("Anda belum menabung hari ini. Target tetap sama untuk hari berikutnya.")

                # Tampilkan jumlah total tabungan saat ini
                print(f"Jumlah total tabungan saat ini: {tabungan_akhir:.2f}\n")

                # Cek apakah target tercapai
                if tabungan_akhir - tabungan_awal >= target_tambahan:
                    target_tercapai = True

                hari += 1  # Increment hari untuk melanjutkan ke hari berikutnya

            # Pesan keberhasilan atau kegagalan
            if target_tercapai:
                print("Selamat! Anda berhasil mencapai target tabungan.")
            else:
                print("Sayang sekali, Anda belum mencapai target tabungan.")
                
            # Simpan data terbaru ke CSV
            simpan_data_ke_csv(tabungan_akhir)

            break  # Keluar dari loop setelah selesai menabung
            

        elif pilihan_awal == '2':
            # Jika memilih untuk menarik tabungan
            jumlah_tarikan = float(input("Masukkan jumlah tabungan yang ingin Anda tarik: "))
            
            if jumlah_tarikan <= tabungan_akhir:
                tabungan_akhir -= jumlah_tarikan
                print(f"Anda berhasil menarik tabungan sebesar {jumlah_tarikan}.")
                print(f"Sisa tabungan Anda sekarang: {tabungan_akhir}\n")
                
                # Menanyakan berapa lama dan kapan mulai menabung kembali
                jumlah_hari = int(input("Berapa lama (dalam hari) Anda ingin menabung untuk mencapai target ini? "))
                tanggal_mulai = input("Masukkan tanggal mulai menabung kembali (format: YYYY-MM-DD): ")
                
                # Konversi tanggal mulai dari input pengguna
                tanggal_mulai = datetime.strptime(tanggal_mulai, "%Y-%m-%d")
                tabungan_per_hari = jumlah_tarikan / jumlah_hari

                print("\n--- Program Tabungan Harian (Menabung Kembali) ---")
                print(f"Target yang ingin dicapai: {jumlah_tarikan}")
                print(f"Jumlah hari yang ditentukan: {jumlah_hari}")
                print(f"Target tabungan per hari: {tabungan_per_hari:.2f}")
                print(f"Tabungan akan dimulai pada tanggal: {tanggal_mulai.strftime('%Y-%m-%d')}\n")

                # Loop untuk menabung kembali sesuai jumlah yang ditarik
                hari = 1
                target_tercapai = False  # Flag untuk memeriksa apakah target tercapai

                while hari <= jumlah_hari:
                    tanggal_hari_ini = tanggal_mulai + timedelta(days=hari - 1)
                    print(f"Tanggal: {tanggal_hari_ini.strftime('%Y-%m-%d')} - Target hari ini: {tabungan_per_hari:.2f}")

                    menabung = input("Apakah Anda sudah menabung hari ini? (y/n): ")
                    
                    if menabung.lower() == 'y':
                        tabungan_akhir += tabungan_per_hari
                        print("Anda berhasil menabung sesuai target hari ini!")
                    else:
                        print("Anda belum menabung hari ini. Target tetap sama untuk hari berikutnya.")

                    # Tampilkan jumlah total tabungan saat ini
                    print(f"Jumlah total tabungan saat ini: {tabungan_akhir:.2f}\n")

                    # Cek apakah target tercapai
                    if tabungan_akhir - (tabungan_awal - jumlah_tarikan) >= jumlah_tarikan:
                        target_tercapai = True

                    hari += 1  # Increment hari untuk melanjutkan ke hari berikutnya

                # Pesan keberhasilan atau kegagalan
                if target_tercapai:
                    print("Selamat! Anda berhasil mencapai target tabungan.")
                else:
                    print("Sayang sekali Anda belum dapat mencapai target tabungan.")
                    
                simpan_data_ke_csv(tabungan_akhir)

                break  # Keluar dari loop menabung kembali
            else:
                print("Jumlah tarikan melebihi total tabungan yang dimiliki. Tidak dapat melakukan penarikan.")
                


        elif pilihan_awal == '3':
            break
        
        else:
            print("Pilihan tidak valid. Silakan pilih opsi yang tersedia.")

    print("\n--- Program Selesai ---")
    print(f"Total tabungan Anda sekarang (tabungan akhir): {tabungan_akhir:.2f}")

# Panggil Fungsi Utama
main()