import pymysql
import os

# Konfigurasi koneksi
connection_name = os.getenv("env_connection_name")
public_ip_address = os.getenv("env_public_ip_address")
db_user = os.getenv("env_db_user")
db_password = os.getenv("env_db_password")
db_name = os.getenv("env_db_name")
db_charset = os.getenv("env_db_charset")

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
