import streamlit as st
import firebase_admin
from firebase_admin import credentials, db

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

if not firebase_admin._apps:
    # Inisialisasi Firebase Admin SDK
    cred = credentials.Certificate("D:\pyproject\PointOfSaleProject\FireBase.json")
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://website-27a20-default-rtdb.firebaseio.com/'
    })


