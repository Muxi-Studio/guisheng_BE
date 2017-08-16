# coding: utf-8
from flask import render_template,jsonify,Response,g,request
import json
import datetime
from ..models import Everydaypic
from . import api
from .. import db
from ..decorators import admin_required,edit_required

@api.route('/everydaypic/', methods=['GET'])
def get_everydaypic():
    everydaypic = Everydaypic.query.order_by(Everydaypic.time.desc()).first()
    return Response(json.dumps({
        "img_url":everydaypic.img_url,
        "climate":everydaypic.climate,
        "date":everydaypic.date,
        }),mimetype='application/json')

#-----------------------------------后台管理API---------------------------------------
@api.route('/everydaypic/', methods=['POST'])
@edit_required
def add_everydaypic():
    everydaypic = Everydaypic.from_json(request.get_json())
    everydaypic.time = datetime.utcnow()+timedelta(hours=8)
    db.session.add(everydaypic)
    db.session.commit()
    return jsonify({
        'id':everydaypic.id
    }), 201
