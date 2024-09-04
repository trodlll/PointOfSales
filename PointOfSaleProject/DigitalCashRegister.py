import streamlit as st
import pandas as pd
import firebase_admin
from firebase_admin import credentials, db
from pathlib import Path

def add_data(key, data):
    ref = db.reference(key)
    ref.set(data)

def update_data(key, data):
    ref = db.reference(key)
    ref.update(data)

def delete_data(key):
    ref = db.reference(key)
    ref.delete()

def read_data(key):
    ref = db.reference(key)
    return ref.get()

def read_all():
    ref = db.reference("/")
    return ref.get()

if not firebase_admin._apps:
    # Inisialisasi Firebase Admin SDK
    cred = credentials.Certificate("D:\pyproject\PointOfSaleProject\FireBase.json")
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://website-27a20-default-rtdb.firebaseio.com/'
    })

def RefreshMenu():
    readAll=[k for k in read_all()]
    l = []
    r = len(readAll)
    for i in range(r):
        try:
            d=read_data(str(i))
            print(d["Nama"])
            l.append(d["Nama"])
        except:
            pass
        print(l)
    return l

def AddItem(n):
    readAll=[k for k in read_all()]
    l = []
    r = len(readAll)
    for i in range(r):
        try:
            d=read_data(str(i))
            if d["Nama"] == n:
               return d["Harga"]
        except:
            pass

session_state = st.session_state
if 'Item' not in session_state:
    session_state.Item=[]
if 'JMLH' not in session_state:
    session_state.JMLH=[]
if 'Price' not in session_state:
    session_state.Price=[]
if 'price' not in session_state:
    session_state.price=[]
LOM = RefreshMenu()
print(LOM)

#Side Bar

col1, col2 = st.columns(2)
Hd1 = col1.subheader("Barang yang akan di beli:")
option = col1.selectbox('SearchBar', LOM)
jmlh = col1.number_input("masukan Jumlah barang", step=1, min_value=1, max_value=10)
lbl=col2.subheader("Barang yang dibeli:")

column = ["Barang", "Harga", "Jumlah"]
col3, col4 = col1.columns(2)
Btn = col3.button("tambah")
Btn2 = col4.button("delete")
Btn3 = col3.button("refresh")
Btn4 = col4.button("reset")
def refresh():
    global wrt
    rg = len(st.session_state.Item)
    lst1 = pd.DataFrame(data = {"Barang" : st.session_state.Item ,"Jumlah" : st.session_state.JMLH , "TotalHarga" : st.session_state.Price})
    wrt = col2.dataframe(lst1, width = 400, height = 500)
    Btn5 = col2.button("cetak")
    if Btn5:
        file_path = Path("receipt.txt")
        with file_path.open('w') as file:
            TH=0
            file.writelines("T e a N t e a R e s t a u r a n t\r")
            file.writelines("Dari: TeaNtea Restaurant\r")
            file.writelines("Alamat: Jawa tengah, Tegal \r")
            file.writelines("- - - - - - - - - - - - - - - - -\r")
            file.writelines("Belanjaan Anda: \r")
            
            for i in range(rg):
                file.writelines(f"Nama: {st.session_state.Item[i]}\r")
                file.writelines(f"  Jumlah Pembelian: {st.session_state.JMLH[i]}\r")
                file.writelines(f"  Harga: {st.session_state.price[i]}\r")
                file.writelines(f"  Total Harga: {st.session_state.Price[i]}\r")
                file.writelines("_ _ _\r")
                TH+=st.session_state.Price[i]
            file.writelines(f"Total Harga: {TH}\r")
            file.writelines("- - - - - - - - - - - - - - - - -\r")
            file.writelines("Terima kasih sudah membeli")

            
        print(f"File '{file_path}' created successfully.")

if Btn2:
    d = AddItem(option)
    session_state.Item.remove(option)
    session_state.JMLH.remove(jmlh)
    session_state.Price.remove(d*jmlh)
    session_state.price.remove(d)

if Btn:
    d = AddItem(option)
    st.session_state.JMLH.append(jmlh)
    st.session_state.Price.append(d*jmlh)
    st.session_state.Item.append(option)
    st.session_state.price.append(d)

if Btn3:
    print("refresh")

if Btn4:
    session_state.Item=[]
    session_state.JMLH=[]
    session_state.Price=[]
    session_state.price=[]

refresh()



