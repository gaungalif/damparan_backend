# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from apps.pesantren import blueprint
from flask import redirect, render_template, request
# from flask_login import login_required
from jinja2 import TemplateNotFound
from apps.pesantren.util import *

@blueprint.route('/pesantren/add', methods=['POST'])
def add_pesantren_route():
    data = request.json
    return add_pesantren(data)

@blueprint.route('/pesantren/<int:pesantren_id>', methods=['GET','PUT','DELETE',])
def get_pesantren_route(pesantren_id):
    if request.method == 'GET':
        return get_pesantren(pesantren_id)
    elif request.method == 'PUT':
        data = request.form
        return update_pesantren(pesantren_id, data)
    else:
        return delete_pesantren(pesantren_id)

@blueprint.route('/pesantren', methods=['GET'])
def get_all_pesantren_route():
    return get_all_pesantren()