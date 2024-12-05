import json
import os

def baca_data_akun():
    try:
        with open("akun.json", "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def simpan_data_akun(data):
    path = "akun.json"
    if not os.path.exists(path):
        with open(path, "w") as file:
            json.dump(data, file, indent=4)
    else:
        with open(path, "r+") as file:
            existing_data = json.load(file)
            existing_data.update(data)
            file.seek(0)
            json.dump(existing_data, file, indent=4)

def daftar_akun(username, password):
    data_akun = baca_data_akun()
    if username in data_akun:
        print("Akun sudah terdaftar!")
    else:
        data_akun[username] = password
        simpan_data_akun(data_akun)
        print("Akun berhasil didaftarkan!")

def login_akun(username, password):
    data_akun = baca_data_akun()
    return username in data_akun and data_akun[username] == password