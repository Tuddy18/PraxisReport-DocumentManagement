from app import app
from flask import request, render_template, flash, redirect, url_for, session, jsonify
from passlib.hash import sha256_crypt
from sqlalchemy.orm import with_polymorphic

from app.domain.praxis import *
from app.domain.student_form import *


@app.route('/praxis/get-all', methods=['GET'])
def get_all():
    praxises = Praxis.query.all()


    resp = jsonify([praxis.json_dict() for praxis in praxises])
    return resp


@app.route('/praxis/get-by-student-email', methods=['POST'])
def get_by_semail():
    email = request.get_json()['email']

    praxis = db.session().query(Praxis).join(StudentForm).filter(StudentForm.email == email).first()

    if praxis:
        resp = jsonify(praxis.json_dict())
        return resp
    else:
        resp = jsonify(success=False, message='profile not found')
        resp.status_code = 404
        return resp

@app.route('/praxis/get-by-email', methods=['POST'])
def get_by_email():
    email = request.form['email']

    praxis = db.session().query(Praxis).join(StudentForm).filter(StudentForm.email == email).first()
    # spraxis = db.session().query(Praxis).join(StudentForm).filter(StudentForm.email == email).first()
    # spraxis = db.session().query(Praxis).join(StudentForm).filter(StudentForm.email == email).first()

    if praxis:
        resp = jsonify(praxis.json_dict())
        return resp
    else:
        resp = jsonify(success=False, message='profile not found')
        resp.status_code = 404
        return resp

