from flask import Flask, url_for, request, redirect, session, jsonify, make_response
import requests
import json
from urllib.request import urlopen
import os
from flask_sqlalchemy import SQLAlchemy
import pymysql



app = Flask(__name__)
PREFIX_URL_= '/apollo'
DB_URL = 'mysql+pymysql://admin:admin123@apollodb.ctyvhbgiz98o.us-east-2.rds.amazonaws.com/apollo_db'
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.config['SECRET_KEY'] = ''
db = SQLAlchemy(app)


class Patient(db.Model):
    __tablename__ = 'apollo_patient_info'
    id = db.Column(db.Integer, primary_key=True)
    patient_name = db.Column(db.String(45),unique=True)
    patient_dob  = db.Column(db.Date())
    patient_phone_number = db.Column(db.String(15))
    patient_weight = db.Column(db.Float())
    patient_height = db.Column(db.Float())
    def __init__(self, patient_name, patient_dob, patient_phone, patient_weight,patient_height):
        self.patient_name = patient_name
        self.patient_dob = patient_dob
        self.patient_phone_number = patient_phone
        self.patient_weight = patient_weight
        self.patient_height = patient_height



@app.route("/",methods=['GET'])
def hello():
    print((db.engine.table_names()))
    print('test')
    return 'BackendService'


#==========================================================================================


@app.route(PREFIX_URL_+'/data/patient/',methods=['GET'])
def get_all_users():
    patients = Patient.query.all()
    output = []
    for patient in patients:
        patient_data = {}
        patient_data['id'] = patient.id
        patient_data['name'] = patient.patient_name
        patient_data['phone_numberer'] = patient.patient_phone_number
        output.append(patient_data)
    return jsonify({'patient':output})


@app.route(PREFIX_URL_+"/data/patient/<patient_id>",methods=['GET'])
def get_patient_info(patient_id):
    print('get_patient_info')

    patient = Patient.query.filter_by(id=patient_id).first()
    if not patient:
        return jsonify({'message':'No patient found'})
    patient_data = {}
    patient_data['name'] = patient.patient_name
    patient_data['phone'] = patient.patient_phone_number
    return jsonify({'patient_data':patient_data})
 
@app.route(PREFIX_URL_+"/data/patient/",methods=['POST'])
def add_patient_info():
    patient_name = request.args['patient_name']
    patient_phone = request.args['patient_phone']
    patient_weight = None
    patient_height = None
    patient_dob = None
    if 'patient_dob' in request.args:
            patient_dob = request.args['patient_dob']    
    if 'patient_weight' in request.args:
            patient_weight = request.args['patient_weight']
    if 'patient_height' in request.args:
            patient_height = request.args['patient_height']
    new_patient = Patient(patient_name=patient_name,patient_phone=patient_phone,patient_weight=patient_weight,
        patient_height=patient_height,patient_dob=patient_dob)
    db.session.add(new_patient)
    db.session.commit()
    print('add_patient_info')
    return 'add_patient_info'


# @app.route("/apollo/data/patient/",methods=['PUT'])
# def update_patient_info():
#     print('update_patient_info')
#     return 'update_patient_info'


@app.route(PREFIX_URL_+"/data/patient/<patient_id>",methods=['DELETE'])
def delete_patient_info(patient_id):
    print('delete_patient_info')
    patient = Patient.query.filter_by(id=patient_id).first()
    if not patient:
        return jsonify({'message':'No patient found'})
    db.session.delete(patient)
    db.session.commit()
    return 'delete_patient_info'


#==========================================================================================





if __name__ == '__main__':
    app.run(host='0.0.0.0')

