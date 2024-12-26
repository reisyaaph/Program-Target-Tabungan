import json
import os

def baca_data_akun():
    akun_data = {}
    
    if os.path.exists("akun.json"):
        with open("akun.json", "r", encoding='utf-8') as file:
            akun_data = json.load(file)
    return akun_data

def simpan_data_akun(username, password):
    akun_data = baca_data_akun()
    akun_data[username] = password

    with open("akun.json", "w", encoding='utf-8') as file:
        json.dump(akun_data, file, ensure_ascii=False, indent=4)

def login_akun(username, password):
    akun_data = baca_data_akun()
    return akun_data.get(username) == password

