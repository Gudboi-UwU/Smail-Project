#import library
from flask import Flask, request, jsonify, json

#import from another file
from function import get_barang, get_barang_by_id, register, login, reset_password


app = Flask(__name__)



#Endpoint untuk mengetes routes
@app.route('/', methods = ['GET'])
def tes():
    return("Api telah berjalan dengan baik !")

# Endpoint /register untuk melakukan registrasi user ke Firebase
@app.route('/register', methods=['POST'])
def firebase_register():
    email = request.json['email']
    password = request.json['password']
    return register(email, password)

# Endpoint /login untuk melakukan login user
@app.route('/login', methods=['POST'])
def firebase_login():
    email = request.json['email']
    password = request.json['password']
    return login(email, password)

# Endpoint /reset-password untuk melakukan reset password user ke Firebase
@app.route('/reset-password', methods=['POST'])
def firebase_reset_password():
    return reset_password()

# @app.route('/reset-password', methods=['POST'])
# def reset_password_route():
#     return reset_password()



# Endpoint /barang untuk mendapatkan semua data barang
@app.route('/barang', methods=['GET'])

def get_all_barang():
    results = get_barang()
    data_barang = []
    for row in results:
        barang = {
            'id': row['id'],
            'nama_barang': row['nama_barang'],
            'harga': row['harga']
        }
        data_barang.append(barang)

    return jsonify(data_barang)


@app.route('/barang/<int:id>', methods=['GET'])
def get_barang_by_id_endpoint(id):
    barang = get_barang_by_id(id)
    
    if barang:
        return jsonify(barang)
    else:
        return jsonify({'message': 'Barang tidak ditemukan'}), 404


