
from app import app
import os
import pymysql
from flask import jsonify, Flask


if __name__=="__main__":
    app.run(debug=True, host='0.0.0.0', port=8084)

    