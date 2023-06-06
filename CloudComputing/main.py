#import library
from flask import Flask, request, jsonify, json
import pymysql
import os
import dotenv
import firebase_admin
from firebase_admin import credentials, auth
import requests
from flask_mail import Mail, Message


app = Flask(__name__)

# Konfigurasi koneksi database
connection_name = os.getenv("env_connection_name")
public_ip_address = os.getenv("env_public_ip_address")
db_user = os.getenv("env_db_user")
db_password = os.getenv("env_db_password")
db_name = os.getenv("env_db_name")
db_charset = os.getenv("env_db_charset")


#Firebase
cred = credentials.Certificate("ServiceAccountKey.json")
firebase_admin.initialize_app(cred)

#Konfigurasi email
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = os.getenv("env_email")
app.config['MAIL_PASSWORD'] = os.getenv("env_password")
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

mail = Mail(app)


#Endpoint untuk mengetes routes
@app.route('/', methods = ['GET'])
def tes():
    return("Api telah berjalan dengan baik !")

# Endpoint /register untuk melakukan registrasi user ke Firebase
@app.route('/register', methods=['POST'])
def firebase_register():
    email = request.json['email']
    password = request.json['password']
    try:
        # Membuat user baru kedalam firebase
        user = auth.create_user(
            email=email,
            password=password
        )
        return jsonify({'message': 'Registrasi Anda telah berhasil', 'UserID': user.uid})

    except Exception as e:
        return jsonify({'message': 'Registrasi Anda gagal', 'error': str(e)}), 400


# Endpoint /login untuk melakukan login user
@app.route('/login', methods=['POST'])
def firebase_login():
    email = request.json['email']
    password = request.json['password']
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


# # Endpoint /reset-password untuk melakukan reset password user ke Firebase
# @app.route('/reset-password', methods=['POST'])
# def firebase_reset_password():
#     email = request.json['email']

#     try:
#         # Mengirim link reset password ke email user
#         reset_link = auth.generate_password_reset_link(email)

#         return jsonify({'message': 'Link reset password telah dikirim ke email Anda', 'link':reset_link})

#     except Exception as e:
#         return jsonify({'message': 'Gagal mengirim link reset password', 'error': str(e)}), 400

@app.route('/reset-password', methods=['POST'])
def firebase_reset_password():
    email = request.json['email']

    try:
        # Mengirim link reset password ke email user
        reset_link = auth.generate_password_reset_link(email)

        # Mengirim email reset password
        msg = Message('Smail Reset Password', sender=app.config['MAIL_USERNAME'], recipients=[email])
        msg.body = 'Klik link berikut untuk mereset password Anda: {}'.format(reset_link)
        mail.send(msg)

        return jsonify({'message': 'Link reset password telah dikirim ke email Anda' ,'link':reset_link})

    except Exception as e:
        return jsonify({'message': 'Gagal mengirim link reset password', 'link':reset_link , 'error': str(e)}), 400


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


# Endpoint /barang untuk mendapatkan semua data barang
@app.route('/barang', methods=['GET'])
def get_all_barang():
    try :
        make_connection()
        cursor = conn.cursor()
        sql = "SELECT * FROM data_barang"
        cursor.execute(sql)

        results = cursor.fetchall()

        cursor.close()
        conn.close()

        data_barang = []
        for row in results:
            barang = {
                'id': row['id'],
                'nama_barang': row['nama_barang'],
                'harga': row['harga']
            }
            data_barang.append(barang)

        return jsonify(data_barang)

    except pymysql.Error as e:

         return jsonify({'error': 'Gagal mendapatkan barang', 'message': str(e)}), 500

    


@app.route('/barang/<int:id>', methods=['GET'])
def get_barang_by_id_endpoint(id):
    try:
        make_connection()
        cursor = conn.cursor()
        sql = f"SELECT * FROM data_barang WHERE id = {id}"
        cursor.execute(sql)
        
        
        barang = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        if barang:
            return jsonify(barang)
        else:
            return jsonify({'message': 'Barang tidak ditemukan'}), 404
    
    except pymysql.Error as e:
        print("Error Barang tidak ditemukan:", e)
    
    

if __name__=="__main__":
    app.run(debug=True, host='0.0.0.0', port='8084')

