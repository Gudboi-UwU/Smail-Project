#import library
from flask import Flask, request, jsonify, json
from firebase_admin import credentials, auth, firestore

#import from another file
from function import get_barang, get_barang_by_id


app = Flask(__name__)



#Endpoint untuk mengetes routes
@app.route('/', methods = ['GET'])
def welcome():
    return("Response bener!")


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


