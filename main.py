import json
import os
from babel.numbers import format_currency
import random
import string
from datetime import datetime, timedelta
import signal
import sys
import pandas as pd
from collections import Counter


keranjang = []


def signal_handler(sig, frame):
    print("\nYou pressed Ctrl+C! Exiting gracefully...")
    # Additional cleanup or exit code can be added here
    sys.exit(0)


def tambah_waktu(tanggal_sekarang, days=0, hours=0, minutes=0, seconds=0):
    interval_waktu = timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds)
    tanggal_hasil = tanggal_sekarang + interval_waktu
    return tanggal_hasil.strftime('%Y-%m-%d %H:%M:%S')


def get_random_string(length):
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return(result_str)

def clear_screen():
    os.system('clear')
def format_rupiah(amount):
    return format_currency(amount, 'Rp. ', locale='id_ID')

def jsonParser(file_path):
    try:
        with open(file_path, "r") as json_file:
            return json.load(json_file)
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON in {file_path}. Details: {e}")


def show():
    plist = jsonParser("product.json")['products']
    # print(plist)
    # print(jsonParser)
    jlist = ""
    x = 1
    for i in plist:
        jlist += str(x) + ". "+i['nama_products']+" -> "+ format_rupiah(i['harga']) + " \n"
        x = x+1
  
    let = f"""

    Daftar Nama Menu di toko ALEKUN:

{jlist}
    """
    return(print(f"{let}"))

def sumAllMenu(data,format = True):
    plist = jsonParser("product.json")['products']
    jumlah = 0
    for i in data:
        jumlah = jumlah + int(plist[i]['harga'])
    return format_rupiah(jumlah) if format else jumlah

def troli(product):
    plist = jsonParser("product.json")['products']
    if(product > len(plist)):
        print("Pilihan salah silahkan pilih lagi !")
        return menu()
    keranjang.append(product)
    question = input("apakah ingin memesan lagi? Y/N : ")
    question = question.lower()
    # print("Keranjang sekarang : "+ str(keranjang))
    if(question == 'y'):
        return menu()
    elif(question == 'n'):
        print(sumAllMenu(keranjang))
        return kasir()
def removeItemsFromKeranjang(items):
    keranjang.pop(items)
    return menu()

def tipePembayaran():
    tipe = jsonParser("type_pembayaran.json")['tipe_pembayaran']
    x = 1
    jlist = ""
    for i in tipe:
        jlist += str(x) + ". "+i['nama']+" \n"
        x = x+1
    return jlist

def writeJson(path,isNullKey = 'laporan'):
    try:
        with open(path, "r") as json_file:
            existing_data = json.load(json_file)
            return existing_data
    except FileNotFoundError:
        # Jika file tidak ditemukan, inisialisasi dengan list kosong
        existing_data = {isNullKey: []}
        return existing_data

def showStruk(data = {}):
    if (data):
        laporan = {
            "no_transaksi": get_random_string(8),
            "jumlah_pembayaran": data.get('jumlah_pembayaran'),
            "jumlah_belanja": data.get('jumlah_belanja'),
            "item_belanja": keranjang,
            "type_pembayaran": data.get('type_pembayaran'),
            "status": data.get('status'),
            "tanggal_transaksi": f"{datetime.now()}"
        }
        existing_data = writeJson('penjualan.json')
        existing_data['laporan'].append(laporan)
        # Tulis kembali dictionary ke dalam file JSON
        with open("penjualan.json", "w") as json_file:
            json.dump(existing_data, json_file, indent=2)
        show = f"""
    Total Belanja : {format_rupiah(int(data.get('jumlah_belanja'))) } 
    Total Bayar : {format_rupiah(int(data.get('jumlah_pembayaran')))}

    ======
    Kembalian : {format_rupiah(int(data.get('jumlah_belanja')) - int(data.get('jumlah_pembayaran')))}


        """
        print(show)
        keranjang.clear()
        
    question = input("Apakah ingin melakukan Transaksi lagi ? Y/N : " )
    question = question.lower()

    if(question == 'y'):
        menu()
    elif(question == 'n'):
        exit()
    else:
        return showStruk()
    


def kasir():
    clear_screen()
    data = {}
    show = f"""
Jumlah yang harus dibayarkan :
{sumAllMenu(keranjang)}
"""
    print(show)
    tipe = f"""
Tipe Pembayaran :
{tipePembayaran()}
    """
    print(tipe)
    type =  int(input("Masukan Pilihan anda : "))
    data.update({'type_pembayaran':type})
    data.update({'jumlah_belanja' : sumAllMenu(keranjang,False)})
    
    if(int(type) > len(tipePembayaran()) ):
        clear_screen()
        print("Anda Salah memasukan angka!")
        return kasir()
    if(type == 1):
        nominal = input("Masukan jumlah uang yang dibayarkan : ")
        data.update({'jumlah_pembayaran':int(nominal)})
        data.update({'status': 'Success'})
        showStruk(data)
    
    
       
def settings():
    show = """
90. Melihat Data
    """

    return(print(show))


def showKeranjang():
    plist = jsonParser("product.json")['products']
    jlist = ""
    x = 1
    for i in keranjang:
        jlist += str(x) + ". "+plist[i]['nama_products']+" -> "+ format_rupiah(plist[i]['harga']) + " \n"
        x = x+1
    show = f"""
Keranjang saat ini :
{jlist}


Total Saat ini: {sumAllMenu(keranjang)}
    """
    # print("Keranjang ::" + show)
    return print(show)

def SettingShow(data):
    df = pd.DataFrame(data)
    return(print(df['item_belanja']))
    

def menu():
    clear_screen()
    show()
    settings()
    if(len(keranjang) > 0):
        showKeranjang()
    cmd = input("Masukan Pilihan Menu: ")
    if(int(cmd) == 90):
        SettingShow(jsonParser('penjualan.json')['laporan'])
    if(cmd[0] == '-'):
        cmd = cmd.split('-')
        cmd = cmd[-1]
        removeItemsFromKeranjang(int(cmd) - 1 )
    else:
        troli(int(cmd) - 1)
    

# showStruk()
# Set the signal handler for Ctrl+C
signal.signal(signal.SIGINT, signal_handler)

try:
    # Your main program logic goes here
    while True:
        # Do some work or wait for user input
        menu()

        

except KeyboardInterrupt:
    # This block will be executed if Ctrl+C is pressed
    print("\nCtrl+C detected! Exiting gracefully...")
    # Additional cleanup or exit code can be added here
    sys.exit(0)

# SettingShow(jsonParser('penjualan.json')['laporan'])
# Load JSON data from file
# with open('penjualan.json') as f:
#     data = json.load(f)

# # Normalize JSON data into a DataFrame
# df = pd.json_normalize(data['laporan'])

# # Combine all lists in 'item_belanja' into one list
# all_items = [item for sublist in df['item_belanja'] for item in sublist]

# # Use Counter to count the frequency of each item
# item_counts = Counter(all_items)

# # Convert Counter result to a DataFrame
# df_item_counts = pd.DataFrame.from_dict(item_counts, orient='index', columns=['Jumlah']).reset_index()
# df_item_counts = df_item_counts.rename(columns={'index': 'Item'})

# # Display the most sold item
# item_terbanyak = df_item_counts.sort_values(by='Jumlah', ascending=False).head(1)
# print("Item yang paling banyak dijual:")
# print(item_terbanyak)