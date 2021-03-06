from app import app
from flask import request, render_template, flash, redirect, url_for, session, jsonify
from passlib.hash import sha256_crypt
from sqlalchemy.orm import with_polymorphic

from app.domain.student_form import *


#@app.route('/student-form/get-all', methods=['GET'])
def get_all_sf():
    forms = StudentForm.query.all()

    if forms:
        resp = jsonify([form.json_dict() for form in forms])
        return resp
    else:
        resp = jsonify(success=False)
        resp.status_code = 404
        return resp


#@app.route('/student-form/get-by-student-email', methods=['POST'])
def get_sf_by_email():
    email = request.get_json()['email']

    form = db.session().query(StudentForm).filter(StudentForm.email == email).first()

    if form:
        resp = jsonify(form.json_dict())
        return resp
    else:
        resp = jsonify(success=False)
        resp.status_code = 404
        return resp

#@app.route('/student-form/create', methods=['POST'])
def create():
    sf_json = request.get_json()

    form = StudentForm()
    form.update_from_dict(sf_json)

    db.session().add(form)
    db.session().commit()

    profile = db.session().query(StudentForm).filter_by(id=form.id).first()

    resp = jsonify(profile.json_dict())
    return resp

