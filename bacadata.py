import csv
from datetime import datetime
import os

def baca_data_tabungan(username):
    filename = "data_tabungan.csv"
    
    if not os.path.exists(filename):
        return 0  

    with open(filename, newline='', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter=';')  
        next(reader, None)  
        saldo = 0
        for row in reader:
            if row[0] == username:  
                saldo = float(row[4]) 
        return saldo  
    
def simpan_data_ke_csv(username, saldo, keterangan, hari):
    filename = "data_tabungan.csv"
    
    mode = 'a' if os.path.exists(filename) else 'w'
    with open(filename, mode, newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=';')
        
        if mode == 'w':  
            writer.writerow(['username', 'tanggal', 'keterangan', 'hari', 'saldo'])
        
        if "Menarik" in keterangan:  
            hari = "-"  

        writer.writerow([
            username,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            keterangan,
            hari,
            saldo
        ])