from flask import Flask, url_for, request, redirect, session, jsonify, make_response
import requests
import json
from urllib.request import urlopen
import os




app = Flask(__name__)
PREFIX_URL_= ''
DB_URL = ''
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.config['SECRET_KEY'] = ''
#db = SQLAlchemy(app)



@app.route("/",methods=['GET'])
def hello():
    return 'BackendService'


if __name__ == '__main__':
    app.run(host='0.0.0.0')

