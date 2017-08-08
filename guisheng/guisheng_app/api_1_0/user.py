# coding: utf-8

from . import api
from guisheng_app import db
from flask import request,jsonify,Response
from flask_login import login_user, logout_user, current_user, login_required
from guisheng_app.models import User
from guisheng_app.decorators import admin_required,edit_required
import json
import base64

@api.route('/register/',methods=['GET','POST'])
def register():
    if request.method == 'POST':
        name = request.get_json().get("username")
        email = request.get_json().get("email")
        password = request.get_json().get("password")
        if not User.query.filter_by(name=name).first() and not User.query.filter_by(email=email).first():
            user = User(name=name,
                    email=email,
                    password=password)
            db.session.add(user)
            db.session.commit()
            user_id=User.query.filter_by(email=email).first().id
            return jsonify({
                "created":user_id,
            })

@api.route('/login/', methods=['GET', 'POST'])
def login():
    email = request.get_json().get("email")
    password = request.get_json().get("password")
    try:
        user = User.query.filter_by(email=email).first()
    except:
        user = None
        uid = None
    if user is not None and user.verify_password(password):
        uid = user.id
        token = user.generate_auth_token()
        return jsonify({
            "uid":user.id,
            "token":token,
        })

#-----------------------------------后台管理API---------------------------------------
@api.route('/user/list/', methods=['GET'])
@edit_required
def user_list():
    count = int(request.args.get('count'))
    page = int(request.args.get('page'))
    user_list = User.query.filter_by(role_id=3).limit(count).offset((page-1)*count)
    users = [{
                "id":user.id,
                "name":user.name,
                "user_role":user.user_role
            } for user in user_list]
    num = User.query.filter_by(role_id=3).count()
    return jsonify({
        "users":users,
        "num":num
        })

@api.route('/role/author/', methods=['POST'])
@edit_required
def change_to_author():
    id = int(request.get_json().get("id"))
    user = User.query.get_or_404(id)
    user.user_role = 1
    db.session.add(user)
    db.session.commit()
    return jsonify({
        "update":user.id,
        }),200

@api.route('/role/user/', methods=['POST'])
@edit_required
def change_to_common_user():
    id = int(request.get_json().get("id"))
    user = User.query.get_or_404(id)
    user.user_role = 0
    db.session.add(user)
    db.session.commit()
    return jsonify({
        "update":user.id,
        }),200

@api.route('/admin/register/', methods=['POST'])
def admin_register():
    name = request.get_json().get("username")
    email = request.get_json().get("email")
    password = request.get_json().get("password")
    if not User.query.filter_by(name=name).first() and not User.query.filter_by(email=email).first():
        user = User(name=name,
                email=email,
                password=password,
                role_id=4)
        db.session.add(user)
        db.session.commit()
        user_id=User.query.filter_by(email=email).first().id
        return jsonify({
            "created":user_id,
        })


@api.route('/admin/login/', methods=['GET', 'POST'])
def admin_login():
    email = request.get_json().get("email")
    password = request.get_json().get("password")
    try:
        user = User.query.filter_by(email=email).first()
    except:
        user = None
        uid = None
    if user is not None and user.verify_password(password) and (user.role_id==2 or user.role_id==4):
        uid = user.id
        token = user.generate_auth_token()
        encode_token = base64.b64encode(token)
        basic_token = "".join(["Basic ",encode_token])
        return jsonify({
            "uid":user.id,
            "token":basic_token,
        })

