# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

# from flask_login import UserMixin

from apps import db, login_manager

from apps.authentication.util import hash_pass

# Tabel "Pesantren"
class Pesantren(db.Model):
    __tablename__ = 'Pesantren'
    
    id = db.Column(db.Integer, primary_key=True)
    pesantren = db.Column(db.String(100))
    yayasan = db.Column(db.String(100))
    pendiri = db.Column(db.String(100))
    pengasuh = db.Column(db.String(100))
    alamat = db.relationship('AlamatPesantren', backref='pesantren', uselist=False)
    media = db.relationship('Media', backref='pesantren', uselist=False)
    keilmuan = db.relationship('KeilmuanPesantren', backref='pesantren', uselist=False)
    lembaga_pendidikan = db.relationship('LembagaPendidikanPesantren', backref='pesantren', uselist=False)
    informasi_tambahan = db.relationship('InformasiTambahan', backref='pesantren', uselist=False)
    foto_pesantren = db.relationship('FotoPesantren', backref='pesantren')

# Tabel "Alamat Pesantren"
class AlamatPesantren(db.Model):
    __tablename__ = 'AlamatPesantren'

    id = db.Column(db.Integer, primary_key=True)
    alamat = db.Column(db.String(200))
    kecamatan = db.Column(db.String(100))
    kabupaten = db.Column(db.String(100))
    pesantren_id = db.Column(db.Integer, db.ForeignKey('pesantren.id'))

# Tabel "Keilmuan Pesantren"
class KeilmuanPesantren(db.Model):
    __tablename__ = 'KeilmuanPesantren'

    id = db.Column(db.Integer, primary_key=True)
    sanad = db.Column(db.String(200))
    talim = db.Column(db.String(200))
    pendidikan = db.Column(db.String(200))
    pesantren_id = db.Column(db.Integer, db.ForeignKey('pesantren.id'))


# Tabel "Lembaga Pendidikan Pesantren"
class LembagaPendidikanPesantren(db.Model):
    __tablename__ = 'LembagaPendidikanPesantren'
    
    id = db.Column(db.Integer, primary_key=True)
    lembFormal = db.Column(db.String(200))
    lembNonFormal = db.Column(db.String(200))
    pendFormal = db.Column(db.String(200))
    lainLain = db.Column(db.String(200))
    pesantren_id = db.Column(db.Integer, db.ForeignKey('pesantren.id'))


# Tabel "Informasi Tambahan"
class InformasiTambahan(db.Model):
    __tablename__ = 'InformasiTambahan'
    
    id = db.Column(db.Integer, primary_key=True)
    usaha = db.Column(db.String(200))
    gmaps = db.Column(db.String(200))
    pesantren_id = db.Column(db.Integer, db.ForeignKey('pesantren.id'))
    

# Tabel "Media"
class Media(db.Model):
    __tablename__ = 'Media'
    
    id = db.Column(db.Integer, primary_key=True)
    instagram = db.Column(db.String(100))
    facebook = db.Column(db.String(100))
    twitter = db.Column(db.String(100))
    website = db.Column(db.String(100))
    pesantren_id = db.Column(db.Integer, db.ForeignKey('pesantren.id'))

# Tabel "Foto Pesantren"
class FotoPesantren(db.Model):
    __tablename__ = 'FotoPesantren'
        
    id = db.Column(db.Integer, primary_key=True)
    foto = db.Column(db.String(100))
    pesantren_id = db.Column(db.Integer, db.ForeignKey('pesantren.id'))