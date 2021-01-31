from app import app
from flask import request, render_template, flash, redirect, url_for, session, jsonify
from passlib.hash import sha256_crypt
from sqlalchemy.orm import with_polymorphic

from app.domain import *

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
    email = request.get_json()['email']

    praxises = db.session().query(Praxis).join(StudentForm).filter(StudentForm.email == email).all()
    # spraxis = db.session().query(Praxis).join(StudentForm).filter(StudentForm.email == email).first()
    # spraxis = db.session().query(Praxis).join(StudentForm).filter(StudentForm.email == email).first()

    if praxis:
        resp = jsonify([praxis.json_dict() for praxis in praxises])
        return resp
    else:
        resp = jsonify(success=False, message='profile not found')
        resp.status_code = 404
        return resp

@app.route('/praxis/create', methods=['POST'])
def create_praxis():
    praxis_json = request.get_json()

    praxis = Praxis()
    sform = StudentForm(email=praxis_json['student_email'])
    pform = ProfessorForm()
    mform = MentorForm()

    praxis.student_form = sform
    praxis.professor_form = pform
    praxis.mentor_form = mform

    db.session().add(praxis)
    db.session().commit()

    praxis = db.session().query(Praxis).filter_by(id=praxis.id).first()

    resp = jsonify(praxis.json_dict())
    return resp

@app.route('/praxis/update', methods=['PUT'])
def update_praxis():
    praxis_json = request.get_json()
    praxis = Praxis.query.filter_by(id=praxis_json['id']).first()

    praxis.update_from_dict(praxis_json)
    db.session().commit()

    praxis = Praxis.query.filter_by(id=praxis_json['id']).first()

    resp = jsonify(praxis.json_dict())
    return resp

@app.route('/praxis/delete', methods=['DELETE'])
def delete_praxis():
    id = request.get_json['id']

    praxis = Praxis.query.filter_by(id=id).first()

    db.session().delete(praxis)
    db.session().commit()

    resp = jsonify(praxis.json_dict())
    return resp