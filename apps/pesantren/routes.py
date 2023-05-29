# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from apps.pesantren import blueprint
from flask import redirect, render_template, request
# from flask_login import login_required
from jinja2 import TemplateNotFound
from apps.pesantren.util import *
from flask_cors import cross_origin

@blueprint.route('/pesantren/add', methods=['POST'])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def add_pesantren_route():
    data = request.json
    return add_pesantren(data)

@blueprint.route('/pesantren/<int:pesantren_id>', methods=['GET','POST','DELETE'])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def get_pesantren_route(pesantren_id):
    if request.method == 'GET':
        return get_pesantren(pesantren_id)
    elif request.method == 'POST':
        data = request.form
        return update_pesantren(pesantren_id, data)
    elif request.method == 'DELETE':
        return delete_pesantren(pesantren_id)

@blueprint.route('/pesantren', methods=['GET'])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def get_all_pesantren_route():
    return get_all_pesantren()