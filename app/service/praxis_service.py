import requests
from flask_mail import Message
from flask_jwt_extended import jwt_required, get_jwt_identity, get_raw_jwt
from app import app, mailapp, auto, PROFILE_SERVICE_URL, db
from flask import request, render_template, flash, redirect, url_for, session, jsonify
from passlib.hash import sha256_crypt
from sqlalchemy.orm import with_polymorphic

from app.domain import *

@app.route('/doc')
@auto.doc()
def documentation():
    '''
    return API documentation page
    '''
    return auto.html()

@app.route('/praxis/get-all', methods=['GET'])
@auto.doc(args=['user identity (JWT_token)'])
@jwt_required
def get_all():
    '''
    Returns all praxis objects
    '''
    praxises = Praxis.query.all()

    resp = jsonify([praxis.json_dict() for praxis in praxises[::-1]])
    return resp

@app.route('/praxis/get-by-student-email', methods=['POST'])
@jwt_required
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


@app.route('/praxis/get-by-email', methods=['GET'])
@auto.doc(args=['user identity (JWT_token)'])
@jwt_required
def get_by_email_with_token():
    '''
    Returns all praxis objects based on the user JWT token identity
    '''
    email = get_jwt_identity()

    spraxises = db.session().query(Praxis).join(StudentForm).filter(StudentForm.email == email).all()
    mpraxis = db.session().query(Praxis).join(MentorForm).filter(MentorForm.email == email).all()
    ppraxis = db.session().query(Praxis).join(ProfessorForm).filter(ProfessorForm.email == email).all()

    # dont do this

    praxises = []
    if spraxises:
        praxises = spraxises
    elif mpraxis:
        praxises = mpraxis
    elif ppraxis:
        praxises = ppraxis
    else:
        resp = jsonify(success=False, message='profile not found')
        resp.status_code = 404
        return resp
    resp = jsonify([praxis.json_dict() for praxis in praxises[::-1]])
    return resp

@app.route('/praxis/get-form-by-email', methods=['POST'])
@auto.doc(args=['user identity (JWT_token)', 'praxis_id'])
@jwt_required
def get_form_by_email():
    '''
    Returns the user specific form from a praxis, based on the user token identity
    '''
    email = get_jwt_identity()
    praxis_id = request.get_json()['praxis_id']

    praxis = db.session().query(Praxis).filter_by(id=praxis_id).first()
    form = {}

    if praxis.student_form.email == email:
        form = praxis.student_form
    elif praxis.mentor_form.email == email:
        form = praxis.mentor_form
    elif praxis.professor_form == email:
        form = praxis.professor_form
    else:
        resp = jsonify(success=False, message='praxis not found')
        resp.status_code = 404
        return resp

    form_json = form.json_dict()
    if praxis.student_form.email == email:
        form_json['type'] = 'student_form'
    elif praxis.mentor_form.email == email:
        form_json['type'] = 'mentor_form'
    elif praxis.professor_form == email:
        form_json['type'] = 'professor_form'
    else:
        resp = jsonify(success=False, message='praxis not found')
        resp.status_code = 404
        return resp
    resp = jsonify(form_json)
    return resp

@app.route('/praxis/get-by-email', methods=['POST'])
@jwt_required
def get_by_email():
    email = request.get_json()['email']

    spraxises = db.session().query(Praxis).join(StudentForm).filter(StudentForm.email == email).all()
    mpraxis = db.session().query(Praxis).join(MentorForm).filter(MentorForm.email == email).first()
    ppraxis = db.session().query(Praxis).join(ProfessorForm).filter(ProfessorForm.email == email).first()

    # dont do this

    praxises = []
    if spraxises:
        praxises = spraxises
    elif mpraxis:
        praxises = mpraxis
    elif ppraxis:
        praxises = ppraxis
    else:
        resp = jsonify(success=False, message='profile not found')
        resp.status_code = 404
        return resp
    resp = jsonify([praxis.json_dict() for praxis in praxises[::-1]])
    return resp

@app.route('/praxis/create', methods=['POST'])
@auto.doc(args=['user identity (JWT_token)', 'praxis object (json)'])
@jwt_required
def create_praxis():
    praxis_json = request.get_json()
    if not praxis_json:
        student_email = get_jwt_identity()
    else:
        student_email = praxis_json['student_email']

    praxis = Praxis()
    sform = StudentForm(email=student_email)


    pform = ProfessorForm()
    mform = MentorForm()
    rform = ReportForm()

    praxis.student_form = sform
    praxis.professor_form = pform
    praxis.mentor_form = mform
    praxis.report_form = rform

    db.session().add(praxis)
    db.session().commit()

    # update student form based on student profile
    try:
        auth_token = request.headers.get('Authorization')
        profile_url = PROFILE_SERVICE_URL + 'profile/get-by-email'
        profile_response = requests.post(profile_url, json={'email': student_email},
                                         headers={'Authorization': auth_token})
        profile_json = profile_response.json()
        if profile_json:
            sform.update_from_dict(profile_json)
    except:
        # student profiel couldn't be found
        pass

    db.session().commit()

    praxis = db.session().query(Praxis).filter_by(id=praxis.id).first()

    resp = jsonify(praxis.json_dict())
    return resp

@app.route('/praxis/update', methods=['PUT'])
@auto.doc(args=['user identity (JWT_token)', 'praxis object (json)'])
@jwt_required
def update_praxis():
    praxis_json = request.get_json()
    praxis = Praxis.query.filter_by(id=praxis_json['id']).first()

    praxis.update_from_dict(praxis_json)
    db.session().commit()

    praxis = Praxis.query.filter_by(id=praxis_json['id']).first()

    resp = jsonify(praxis.json_dict())
    return resp

@app.route('/praxis/update-prof-mentor', methods=['PUT'])
@auto.doc(args=['user identity (JWT_token)', 'id', 'professor_email', 'mentor_email', 'should_send_email'])
@jwt_required
def update_praxis_mentors():
    '''
    Updates the professor and mentor of a praxis object and notifies them via email
    '''
    praxis_json = request.get_json()
    praxis = Praxis.query.filter_by(id=praxis_json['id']).first()

    prof_email = praxis_json['professor_email']
    mentor_email = praxis_json['mentor_email']

    praxis.professor_form.email = prof_email
    praxis.mentor_form.email = mentor_email

    db.session().commit()

    should_send_mail = praxis_json['should_send_email']
    if should_send_mail:
        try:
            msg = Message('UBB PraxisReport info', sender=app.config['MAIL_USERNAME'], recipients=[prof_email, mentor_email])
            msg.body = f"Hello!\n You have been requested to fill out your info for a praxis for student {praxis.student_form.email}. \n Please login and fill out the data:\n"
            msg.body += 'https://ubb-documente-practica.herokuapp.com'
            mailapp.send(msg)
        except:
            pass

    # update student form based on student profile
    try:
        pform = praxis.professor_form
        mform = praxis.mentor_form

        auth_token = request.headers.get('Authorization')
        profile_url = PROFILE_SERVICE_URL + 'profile/get-by-email'
        prof_response = requests.post(profile_url, json={'email': pform.email},
                                         headers={'Authorization': auth_token})
        prof_json = prof_response.json()
        if prof_json:
            pform.update_from_dict(prof_json)

        mentor_reponse = requests.post(profile_url, json={'email': mform.email},
                                      headers={'Authorization': auth_token})
        mentor_json = mentor_reponse.json()
        if mentor_json:
            mform.update_from_dict(mentor_json)
    except:
        # student profiel couldn't be found
        pass

    db.session().commit()
    praxis = Praxis.query.filter_by(id=praxis_json['id']).first()

    resp = jsonify(praxis.json_dict())
    return resp

@app.route('/praxis/update-status', methods=['PUT'])
@auto.doc(args=['user identity (JWT_token)', 'id', 'status_message', 'accepted'])
@jwt_required
def update_praxis_status():
    '''
    Updates the status of a praxis and adds a message
    '''
    praxis_json = request.get_json()
    praxis = Praxis.query.filter_by(id=praxis_json['id']).first()

    praxis.status_message = praxis_json['status_message']
    praxis.status = 'completed' if praxis_json['accepted'] else 'incorrect'
    db.session().commit()

    praxis = Praxis.query.filter_by(id=praxis_json['id']).first()

    resp = jsonify(praxis.json_dict())
    return resp

@app.route('/praxis/delete', methods=['DELETE'])
@auto.doc(args=['user identity (JWT_token)', 'id'])
@jwt_required
def delete_praxis():
    id = request.get_json()['id']

    praxis = Praxis.query.filter_by(id=id).first()

    db.session().delete(praxis)
    db.session().commit()

    resp = jsonify(praxis.json_dict())
    return resp

@app.route('/praxis/request-report-notification', methods=['POST'])
@auto.doc(args=['user identity (JWT_token)', 'praxis_id'])
@jwt_required
def request_report_notification():
    '''
    Sends an email notification to the praxis mentor (if the praxis status is completed) to fill out report data
    '''
    email = get_jwt_identity()
    praxis_id = request.get_json()['praxis_id']

    praxis = db.session().query(Praxis).filter_by(id=praxis_id).first()

    if praxis:
        if praxis.status == 'completed':
            mentor_email = praxis.mentor_form.email
            try:
                msg = Message('UBB PraxisReport request', sender=app.config['MAIL_USERNAME'], recipients=[mentor_email])
                msg.body = f"Hello!\n You have been requested to fill out a praxis report for student {praxis.student_form.email}. \n Please login and fill out the data:\n"
                msg.body += 'https://ubb-documente-practica.herokuapp.com'
                mailapp.send(msg)
            except:
                pass
            resp = jsonify(success=True, message='Success!')
            return resp
        else:
            resp = jsonify(success=False, message='praxis not completed')
            resp.status_code = 404
            return resp
    else:
        resp = jsonify(success=False, message='praxis not found')
        resp.status_code = 404
        return resp

