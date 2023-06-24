# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

# from flask_login import login_required
#import photos from apps
import os
from flask import redirect, render_template, request
from jinja2 import TemplateNotFound
from flask_cors import cross_origin
from apps import uploadconfig
from apps import response
from apps.config import Config
from apps.pesantren import blueprint
# from apps.pesantren.util import *
from werkzeug.utils import secure_filename
from apps.pesantren.models import *
from apps import db
from apps.home.routes import login_required
from flask import jsonify

@blueprint.route('/pesantren/<int:pesantren_id>', methods=['GET', 'PUT', 'DELETE'])
@cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
@login_required
def pesantren_detail(pesantren_id, current_user):
    pesantren = Pesantren.query.get(pesantren_id)

    if pesantren:
        if request.method == 'GET':
            return pesantren_schema.jsonify(pesantren)
        elif request.method == 'PUT':
            # Mengambil data baru dari request
            pesantren_data = request.json
            pesantren.pesantren = pesantren_data['pesantren']
            pesantren.yayasan = pesantren_data['yayasan']
            # Update properti lainnya sesuai kebutuhan

            db.session.commit()
            return jsonify({'message': 'Pesantren updated successfully.'}), 200
        elif request.method == 'DELETE':
            #delete the photo files also
            # os.remove(os.path.join(Config.UPLOADED_PHOTOS_DEST, pesantren.foto_filename))
            db.session.delete(pesantren)
            db.session.commit()
            return jsonify({'message': 'Pesantren deleted successfully.'}), 200
    else:
        return jsonify({'message': 'Pesantren not found.'}), 404

    
@blueprint.route('/pesantren', methods=['GET'])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
@login_required
def get_pesantren(current_user):
    all_pesantren = Pesantren.query.all()
    result = pesantrens_schema.dump(all_pesantren)
    return jsonify(result)

# Endpoint untuk Menambahkan Data Pesantren
# Endpoint untuk Menambahkan Data Pesantren
@blueprint.route('/pesantren', methods=['POST'])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
@login_required
def add_pesantren(current_user):
    pesantren = request.json['pesantren']
    yayasan = request.json['yayasan']
    pendiri = request.json['pendiri']
    foto_filename = request.json['foto_filename']
    alamat = request.json['alamat']['alamat']
    kecamatan = request.json['alamat']['kecamatan']
    kabupaten = request.json['alamat']['kabupaten']
    gmaps = request.json['informasi_tambahan']['gmaps']
    instagram = request.json['media']['instagram']
    facebook = request.json['media']['facebook']
    twitter = request.json['media']['twitter']
    website = request.json['media']['website']
    pengasuh = request.json['pengasuh']
    daftarpengasuh = request.json['daftarPengasuh']
    deskripsi = request.json['deskripsi']
    sanad = request.json['keilmuan']['sanad']
    talim = request.json['keilmuan']['talim']
    pendidikan = request.json['keilmuan']['pendidikan']
    lembagaformal = request.json['lembaga_pendidikan']['lembFormal']
    lembaganonformal = request.json['lembaga_pendidikan']['lembNonFormal']
    pendidikanformal = request.json['lembaga_pendidikan']['pendFormal']
    lainlain = request.json['lembaga_pendidikan']['lainLain']
    usaha = request.json['informasi_tambahan']['usaha']
    fasilitas = request.json['informasi_tambahan']['fasilitas']

    new_pesantren = Pesantren(pesantren=pesantren, yayasan=yayasan, pendiri=pendiri, foto_filename=foto_filename, alamat=alamat,
                              kecamatan=kecamatan, kabupaten=kabupaten, gmaps=gmaps, instagram=instagram,
                              facebook=facebook, twitter=twitter, website=website, pengasuh=pengasuh, deskripsi=deskripsi)

    for fasilitas_name in fasilitas:
        fasilitas_obj = Fasilitas(fasilitas_name=fasilitas_name)
        new_pesantren.fasilitas.append(fasilitas_obj)
        
    for pengasuh_name in daftarpengasuh:
        pengasuh_obj = daftarPengasuh(pengasuh_name=pengasuh_name)
        new_pesantren.daftarPengasuh.append(pengasuh_obj)

    for sanad_name in sanad:
        sanad_obj = Sanad(sanad_name=sanad_name)
        new_pesantren.sanad.append(sanad_obj)

    for talim_name in talim:
        talim_obj = Talim(talim_name=talim_name)
        new_pesantren.talim.append(talim_obj)
    
    for usaha_name in usaha:
        usaha_obj = Usaha(usaha_name=usaha_name)
        new_pesantren.usaha.append(usaha_obj)

    for pendidikan_name in pendidikan:
        pendidikan_obj = Pendidikan(pendidikan_name=pendidikan_name)
        new_pesantren.pendidikan.append(pendidikan_obj)

    for lembaga_formal_name in lembagaformal:
        lembaga_formal_obj = LembagaPendidikanFormal(lembaga_formal_name=lembaga_formal_name)
        new_pesantren.lembFormal.append(lembaga_formal_obj)

    for lembaga_nonformal_name in lembaganonformal:
        lembaga_nonformal_obj = LembagaPendidikanNonformal(lembaga_nonformal_name=lembaga_nonformal_name)
        new_pesantren.lembNonFormal.append(lembaga_nonformal_obj)

    for pend_formal_name in pendidikanformal:
        pend_formal_obj = PendidikanFormal(pendidikan_formal_name=pend_formal_name)
        new_pesantren.pendFormal.append(pend_formal_obj)

    for lainlain_name in lainlain:
        lainlain_obj = LainLain(lainlain_name=lainlain_name)
        new_pesantren.lainLain.append(lainlain_obj)
  
    db.session.add(new_pesantren)
    db.session.commit()

    return pesantren_schema.jsonify(new_pesantren)

# @blueprint.route('/pesantren/upload-foto', methods=['POST'])
# @cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
# def upload_fotos():
#     pesantren_id = request.form.get('pesantren_id')
#     pesantren = Pesantren.query.get(pesantren_id)
#     if 'foto' not in request.form:
#         return jsonify({'message': 'Foto tidak tersedia'}), 400

#     docs = request.form.get('foto')
#     pesantren.foto_filename = docs
#     db.session.commit()
#     return response.success(
#         {
#             'foto': docs,
#             'pesantren_id': pesantren_id
            
#         }, 
#         "Sukses mengupload file"
#     )
    # pesantren_name = pesantren.pesantren
    # if 'foto' not in request.files:
    #     return jsonify({'message': 'Foto tidak tersedia'}), 400

    # docs = request.files['foto']

    # if docs.filename == '':
    #     return jsonify({'message': 'Foto tidak tersedia'}), 400
    # if docs and uploadconfig.allowed_file(docs.filename):

    #     # filename = secure_filename(docs.filename)
    #     renamefile = pesantren_name+'.jpg'

    #     docs.save(os.path.join(Config.UPLOADED_PHOTOS_DEST, renamefile))

    #     pesantren.foto_filename = renamefile
    #     db.session.commit()
        
    #     return response.success(
    #         {
    #             'foto': renamefile,
    #             'pesantren_id': pesantren_id
                
    #         }, 
    #         "Sukses mengupload file"
    #     )

    # else:
    #     return response.badRequest([],'File tidak diizinkan')
    
@blueprint.route('/pesantren/get-foto/<int:pesantren_id>', methods=['GET'])
@cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
@login_required
def get_fotos(pesantren_id, current_user):
    pesantren = Pesantren.query.get(pesantren_id)
    if pesantren == None:
        return response.badRequest([], 'Pesantren tidak ditemukan')
    if pesantren.foto_filename == None:
        return response.badRequest([], 'Foto tidak tersedia')
    foto_filename = pesantren.foto_filename
    return response.success(
            {
                'foto': foto_filename,
                'pesantren_id': pesantren_id
                
            }, 
            "FILE FOUND"
        )
