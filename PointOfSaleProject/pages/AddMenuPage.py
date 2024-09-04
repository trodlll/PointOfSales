import streamlit as st
import pandas as pd
import firebase_admin
from firebase_admin import credentials, db
from st_aggrid import AgGrid,GridOptionsBuilder, GridUpdateMode
from pathlib import Path

def add_data(key, data):
    ref = db.reference(key)
    ref.set(data)

def update_data(key, data):
    ref = db.reference(str(key))
    ref.update(data)

def delete_data(key):
    ref = db.reference(key)
    ref.delete()

def read_data(key):
    ref = db.reference(key)
    id = ref.get()
    return id

def read_all():
    ref = db.reference("/")
    return ref.get()

def GetKeyValue():
    if read_all() != None:
        readAll=[k for k in read_all()]
        r=len(readAll)
        key=[]
        for i in range(r):
            if readAll[i]==None:
                key.append(i)
        key.append(r+1)
        return key
        # readAll=[k for k in read_all()]
        # print(read_all())
        # key= []
        # for i in range(len(readAll)):
        #     if str(readAll[i]).isnumeric():
        #         key.append(int(readAll[i]))
        # key.sort(reverse=True)
        # if len(key)>0:
        #     return int(key[0])+1
        # else:
        #     # return int(key)+1
            
    else:
        return 0
def ReadItem():
    if read_all() != None:
        Item = [v for v in read_all()]
        num = len(Item)
        print(Item)
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
    return l
def checkNone():
    readAll=[k for k in read_all()]
    l = []
    for i in readAll:
        if i == None:
            l.append("none")
    return len(l)

def ReadPrice():
    readAll=[k for k in read_all()]
    l = []
    r = len(readAll)
    for i in range(r):
        try:
            d=read_data(str(i))
            print(d["Nama"])
            l.append(d["Harga"])
        except:
            pass
    return l
def ReadKey():
    readAll=[k for k in read_all()]
    l = []
    r = len(readAll)
    for i in range(r-1):
        try:
            d=read_data(str(i+1))
            print(d["Nama"])
            l.append(d["key"])
        except:
            pass
    

if not firebase_admin._apps:
    # Inisialisasi Firebase Admin SDK
    cred = credentials.Certificate("D:\pyproject\PointOfSaleProject\FireBase.json")
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://website-27a20-default-rtdb.firebaseio.com/'
    })
#MainPage



TF = st.sidebar.selectbox("",{"Tambah", "Delete"})
SHD = st.sidebar.subheader("List Menu:")
Item = RefreshMenu()
print(Item)
Price = ReadPrice()
print(Price)
lst1 = pd.DataFrame(data = {"Barang" : Item, "Harga" : Price})
DF = st.sidebar.dataframe(lst1, width=300, height=580)
ReadItem()

# gb=GridOptionsBuilder.from_dataframe(lst1)
# gb.configure_selection('multiple', use_checkbox=False)
# grid_options=gb.build()

# newData=AgGrid(
#     lst1,
#     gridOptions=grid_options,
#     update_mode=GridUpdateMode.SELECTION_CHANGED
# )

# try:
#     selected_rows=newData['selected_rows']
#     st.write(selected_rows)
#     st.write(selected_rows['Nama'])
# except TypeError:
#     pass

if TF == "Tambah":
    hd = st.header("Tambah Code Barang:")
    NB = st.text_input("Nama Barang:")
    HB = st.number_input("Harga Barang:", step=1000)
    TB = st.selectbox("Tipe Barang", {"Makanan", "Minuman", "Lainnya"})
    BTN = st.button("Tambah Ke Menu Barang")
    key = GetKeyValue()[0]
    if BTN:
        add_data(str(key) , {"Nama": NB, "Harga": HB, "Tipe": TB})
if TF == "Delete":
    hd = st.header("Delete Barang di Menu: ")
    NB = st.selectbox("Pilih Barang", Item)
    print("A",NB)
    for i in range(len(Item)):
        if Item[i] == NB:
            st.number_input("harga barang: ", value=Price[i])
            Key=i+checkNone()
            print(Key)
            break
    BTN = st.button("Delete dari menu.")
    if BTN:
        delete_data(str(Key))

        
#SidePage
