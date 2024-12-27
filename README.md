# Kelas B Kelompok 2 Anggota:
1. Reisya Anjani Prawidya Hapsari I0324062 @reisyaaph
2. RIDHO ROFAN SUYANTO I0324064 @rofancy
3. I Made Dewa Kusuma Ardana I0324082 @Dewa-82

# Program-Target-Tabungan
Program "Aplikasi Target Tabungan" adalah aplikasi berbasis Python yang membantu pengguna dalam mengatur tabungannya sehingga memenuhi target yang diinginkan. Program ini memuat data tabungan pengguna (CSV) dan menampilkan tabungan sekarang. Pengguna dapat mengatur jumlah target tabungan dan jumlah hari dalam menabungnya. 

# Fitur-fitur aplikasi
1. Lanjutkan Menabung
2. Mulai Baru
3. Menarik Tabungan
4. Cek Riwayat
5. Keluar

# Diagram Alir
![Tabungan drawio (1)](https://github.com/user-attachments/assets/03b078bf-8e5f-4390-b695-069f8af377c1)

# Diagram Alir Revisi
![Flowchart Program Target Tabungan-Main Program drawio](https://github.com/user-attachments/assets/aa5c6a9f-97c9-4dbc-871f-869a025cca40)

![Flowchart Program Target Tabungan-Login drawio](https://github.com/user-attachments/assets/3ea3c380-eb84-4dd6-b3c6-c96232e2cb3c)

![Flowchart Program Target Tabungan-Lanjutkan Menabung drawio](https://github.com/user-attachments/assets/263bcac6-762a-41c1-9127-070439ea9ee8)

![Flowchart Program Target Tabungan-Mulai Baru drawio](https://github.com/user-attachments/assets/53f7b959-b20f-49f1-8fef-2e0dadde84a0)

![Flowchart Program Target Tabungan-Menarik Tabungan drawio](https://github.com/user-attachments/assets/3d26d1bb-1f97-45c4-9a36-1be59a09e20a)

# Diagram Alir Final
![Flowchart Program Target Tabungan-Main Program drawio](https://github.com/user-attachments/assets/7d119ab8-5dc4-44d9-87fe-9a62df1e7d69)

![Flowchart Program Target Tabungan-Login drawio](https://github.com/user-attachments/assets/87ee67cd-e3f1-4a84-9fe4-95ee9424fcc2)

![Flowchart Program Target Tabungan-Lanjutkan Menabung drawio](https://github.com/user-attachments/assets/bde50485-97db-4147-ab65-a72d32aa2267)

![Flowchart Program Target Tabungan-Mulai Baru drawio](https://github.com/user-attachments/assets/5a2c8c38-3000-4484-8379-2f77db1b3aca)

![Flowchart Program Target Tabungan-Menarik Tabungan drawio](https://github.com/user-attachments/assets/c9739134-fdd4-4cfc-ba82-0e2b44f6f6bb)

![Flowchart Program Target Tabungan-Cek Riwayat drawio](https://github.com/user-attachments/assets/b2028087-b08d-49c4-8585-037ec15a633c)

Diagram alir tersebut menggambarkan proses aplikasi yang memungkinkan pengguna mengatur target tabungan mereka. Proses dimulai dengan pengguna memilih untuk melakukan login atau daftar akun baru. Jika pengguna sudah memiliki akun, pengguna dapat langsung memasukkan username dan password kemudian menekan tombol Login. Apabila belum, pengguna dapat memilih Daftar Akun Baru. Selanjutnya, pengguna dapat memasukkan username dan password yang diinginkan kemudian menekan tombol daftar. Kemudian pengguna dapat memasukkan username dan password yang sesuai di halaman login. Data akun pengguna akan disimpan ke file json. Setelah login berhasil, pengguna akan diarahkan ke halaman menu utama di mana pengguna dapat memilih fitur mana yang akan digunakan, 1. Lanjutkan Menabung, 2. Mulai Baru, 3. Menarik Tabungan, dan 4. Cek Riwayat, dan 5. Keluar. Jika pengguna sudah memulai target tabungan sebelumnya, pengguna dapat memilih fitur Lanjutkan Menabung. Pengguna akan disajikan tampilan hari ke-berapa pengguna menabung dan pengguna akan diminta memilih, jika pengguna sudah menabung hari itu, maka pengguna dapat memilih opsi menabung dan apabila pengguna melewati menabung hari itu, pengguna dapat memilih opsi tidak menabung. Apabila periode hari untuk menabung sudah mencapai hari terakhir namun target tabungan belum tercapai, maka pengguna dapat memperpanjang periode menabung untuk mencapai target. Pada halaman perpanjang target menabung, pengguna dapat menginput target tambahan hari untuk menabung sisa dari target sebelumnya yang belum terpenuhi. Data yang sudah ditabung akan masuk ke file data tabungan pengguna (CSV) dan menambahkan dengan tabungan sebelumnya. Jika pengguna belum memiliki target tabungan sebelumnya, namun memilih fitur Lanjutkan Menabung, pengguna akan diminta untuk memilih fitur Mulai Baru. Di fitur Mulai Baru, pengguna akan diminta memasukkan berapa target tabungan dalam rupiah dan akan menabung untuk berapa hari. Selanjutnya, jika pengguna memilih fitur Menarik Tabungan, pengguna dapat memasukkan nominal tabungan yang akan ditarik.Setelah memilih tombol tarik, pengguna akan diarahkan ke halaman fitur Mulai Baru, di mana pengguna diminta untuk memasukkan nominal target tabungan dan jumlah hari pengguna akan menabung. Apabila pengguna memilih fitur Cek Riwayat maka pengguna akan ditampilkan halaman dengan riwayat aktivitas menabung dan menarik tabungan di akun pengguna. Riwayat meliputi tanggal dilakukannya aktivitas, keterangan aktivitas, pada hari ke-berapa dalam periode menabung aktivitas itu dilakukan, dan saldonya. Kemudian, apabila pada halaman menu utama pengguna memilih fitur Keluar, maka pengguna akan diarahkan ke halaman login kembali. 

# Sitemap
![Sitemap Program Target Tabungan drawio](https://github.com/user-attachments/assets/5d7e1771-c73e-4566-ab29-85da021f83ab)

# Sitemap Final
![Sitemap 2B Program Target Tabungan drawio](https://github.com/user-attachments/assets/54989c4a-2477-4f4b-8734-8fe370aa6207)

# Library yang digunakan
1. tkinter
2. pillow
3. datetime
4. csv
5. json
6. os



