from flask import jsonify, request
import pymysql
import os
import dotenv
import firebase_admin
import requests
from firebase_admin import credentials, auth, firestore, exceptions


# Konfigurasi koneksi database
connection_name = os.getenv("env_connection_name")
public_ip_address = os.getenv("env_public_ip_address")
db_user = os.getenv("env_db_user")
db_password = os.getenv("env_db_password")
db_name = os.getenv("env_db_name")
db_charset = os.getenv("env_db_charset")


#Firebase
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)


# Fungsi untuk register ke Firebase
def register(email, password):
    try:
        # Membuat user baru kedalam firebase
        user = auth.create_user(
            email=email,
            password=password
        )
        return jsonify({'message': 'Registrasi Anda telah berhasil', 'UserID': user.uid})

    except Exception as e:
        return jsonify({'message': 'Registrasi Anda gagal', 'error': str(e)}), 400
    

# Fungsi untuk melakukan login ke Firebase
def login(email, password):
    try:
        user = auth.get_user_by_email(email)
        if user:
            dotenv.load_dotenv()
            firebase_api_key = os.getenv("env_firebase_web_api_key")
            login_url = "https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={}".format(firebase_api_key)
            json_request = {"email": email, "password": password}
            login_firebase = requests.post(login_url, json=json_request)
            return jsonify({'message': 'Anda berhasil login, Selamat datang !', "data": login_firebase.json()})
        else:
            return jsonify({'message': 'Anda gagal melakukan login', 'error': 'User tidak ditemukan'}), 401

    except Exception as e:
        return jsonify({'message': 'Anda gagal melakukan login', 'error': str(e)}), 401


# Fungsi untuk melakukan reset password
def reset_password():
    email = request.json['email']

    try:
        # Mengirim link reset password ke email user
        reset_link = auth.generate_password_reset_link(email)

        return jsonify({'message': 'Link reset password telah dikirim ke email Anda', 'link':reset_link})

    except Exception as e:
        return jsonify({'message': 'Gagal mengirim link reset password', 'error': str(e)}), 400



#Fungsi untuk test koneksi DB
def test_db_connection():
    try:
        connection = pymysql.connect(
            host=public_ip_address,
            user=db_user,
            password=db_password,
            database=db_name,
            charset=db_charset,
            cursorclass=pymysql.cursors.DictCursor

        )
        print("Koneksi ke database berhasil!")
        connection.close()
        return ("Koneksi ke database berhasil!")
    except pymysql.Error as e:
        print("Koneksi ke database gagal:", str(e))



# Fungsi untuk menghubungkan ke Cloud SQL
def make_connection():
    global conn;
    conn = pymysql.connect(
        host=public_ip_address,
        user=db_user,
        password=db_password,
        db=db_name,
        charset=db_charset,
        cursorclass=pymysql.cursors.DictCursor
    )
    return conn


# Fungsi untuk mendapatkan semua data barang dari tabel
def get_barang():
    try :
        make_connection()
        cursor = conn.cursor()
        sql = "SELECT * FROM data_barang"
        cursor.execute(sql)

        results = cursor.fetchall()

        cursor.close()
        conn.close()

        return results
    except pymysql.Error as e:

        print("Error Tidak ada barang :", e)


# Fungsi untuk mendapatkan barang tertentu berdasarkan id 
def get_barang_by_id(id_barang):
    try:
        make_connection()
        cursor = conn.cursor()
        sql = f"SELECT * FROM data_barang WHERE id = {id_barang}"
        cursor.execute(sql)
        
        
        barang = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        return barang
    
    except pymysql.Error as e:
        print("Error Barang tidak ditemukan:", e)
