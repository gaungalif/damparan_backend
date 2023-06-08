from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy


from apps import db, ma



# Definisikan Model
class Pesantren(db.Model):
    pesantren_id = db.Column(db.Integer, primary_key=True)
    pesantren = db.Column(db.String(255))
    yayasan = db.Column(db.String(255))
    pendiri = db.Column(db.String(255))
    alamat = db.Column(db.String(255))
    kecamatan = db.Column(db.String(255))
    kabupaten = db.Column(db.String(255))
    gmaps = db.Column(db.String(255))
    instagram = db.Column(db.String(255))
    facebook = db.Column(db.String(255))
    twitter = db.Column(db.String(255))
    website = db.Column(db.String(255))
    pengasuh = db.Column(db.String(255))
    # add description withouth length limit
    deskripsi = db.Column(db.Text)
    foto_filename = db.Column(db.String(255))
    daftarPengasuh = db.relationship('daftarPengasuh', backref='pesantren', cascade='all, delete')
    sanad = db.relationship('Sanad', backref='pesantren', cascade='all, delete')
    talim = db.relationship('Talim', backref='pesantren', cascade='all, delete')
    pendidikan = db.relationship('Pendidikan', backref='pesantren', cascade='all, delete')
    lembFormal = db.relationship('LembagaPendidikanFormal', backref='pesantren', cascade='all, delete')
    lembNonFormal = db.relationship('LembagaPendidikanNonformal', backref='pesantren', cascade='all, delete')
    pendFormal = db.relationship('PendidikanFormal', backref='pesantren', cascade='all, delete')
    lainLain = db.relationship('LainLain', backref='pesantren', cascade='all, delete')
    usaha = db.relationship('Usaha', backref='pesantren', cascade='all, delete')
    fasilitas = db.relationship('Fasilitas', backref='pesantren', cascade='all, delete')


class Fasilitas(db.Model):
    fasiltas_id = db.Column(db.Integer, primary_key=True)
    pesantren_id = db.Column(db.Integer, db.ForeignKey('pesantren.pesantren_id'))
    fasilitas_name = db.Column(db.String(255))
    
class daftarPengasuh(db.Model):
    pengasuh_id = db.Column(db.Integer, primary_key=True)
    pesantren_id = db.Column(db.Integer, db.ForeignKey('pesantren.pesantren_id'))
    pengasuh_name = db.Column(db.String(255))

class Sanad(db.Model):
    sanad_id = db.Column(db.Integer, primary_key=True)
    pesantren_id = db.Column(db.Integer, db.ForeignKey('pesantren.pesantren_id'))
    sanad_name = db.Column(db.String(255))

class Talim(db.Model):
    talim_id = db.Column(db.Integer, primary_key=True)
    pesantren_id = db.Column(db.Integer, db.ForeignKey('pesantren.pesantren_id'))
    talim_name = db.Column(db.String(255))

class Usaha(db.Model):
    usaha_id = db.Column(db.Integer, primary_key=True)
    usaha_name = db.Column(db.String(100))
    pesantren_id = db.Column(db.Integer, db.ForeignKey('pesantren.pesantren_id'))


class Pendidikan(db.Model):
    pendidikan_id = db.Column(db.Integer, primary_key=True)
    pesantren_id = db.Column(db.Integer, db.ForeignKey('pesantren.pesantren_id'))
    pendidikan_name = db.Column(db.String(255))

class LembagaPendidikanFormal(db.Model):
    lembaga_formal_id = db.Column(db.Integer, primary_key=True)
    pesantren_id = db.Column(db.Integer, db.ForeignKey('pesantren.pesantren_id'))
    lembaga_formal_name = db.Column(db.String(255))

class LembagaPendidikanNonformal(db.Model):
    lembaga_nonformal_id = db.Column(db.Integer, primary_key=True)
    pesantren_id = db.Column(db.Integer, db.ForeignKey('pesantren.pesantren_id'))
    lembaga_nonformal_name = db.Column(db.String(255))

class PendidikanFormal(db.Model):
    pendidikan_formal_id = db.Column(db.Integer, primary_key=True)
    pesantren_id = db.Column(db.Integer, db.ForeignKey('pesantren.pesantren_id'))
    pendidikan_formal_name = db.Column(db.String(255))

class LainLain(db.Model):
    lainlain_id = db.Column(db.Integer, primary_key=True)
    pesantren_id = db.Column(db.Integer, db.ForeignKey('pesantren.pesantren_id'))
    lainlain_name = db.Column(db.String(255))

# Definisikan Skema Marshmallow

class FotoSchema(ma.Schema):
    class Meta:
        fields = ('foto_id', 'filename')
        
class FasilitasSchema(ma.Schema):
    class Meta:
        fields = ('fasilitas_id', 'fasilitas_name')
        
class PengasuhSchema(ma.Schema):
    class Meta:
        fields = ('pengasuh_id', 'pengasuh_name')

class SanadSchema(ma.Schema):
    class Meta:
        fields = ('sanad_id', 'sanad_name')

class TalimSchema(ma.Schema):
    class Meta:
        fields = ('talim_id', 'talim_name')
        
class UsahaSchema(ma.Schema):
    class Meta:
        fields = ('usaha_id', 'usaha_name')

class PendidikanSchema(ma.Schema):
    class Meta:
        fields = ('pendidikan_id', 'pendidikan_name')

class LembagaPendidikanFormalSchema(ma.Schema):
    class Meta:
        fields = ('lembaga_formal_id', 'lembaga_formal_name')

class LembagaPendidikanNonformalSchema(ma.Schema):
    class Meta:
        fields = ('lembaga_nonformal_id', 'lembaga_nonformal_name')

class PendidikanFormalSchema(ma.Schema):
    class Meta:
        fields = ('pendidikan_formal_id', 'pendidikan_formal_name')

class LainLainSchema(ma.Schema):
    class Meta:
        fields = ('lainlain_id', 'lainlain_name')

class PesantrenSchema(ma.Schema):
    daftarPengasuh = ma.Nested(PengasuhSchema, many=True)
    sanad = ma.Nested(SanadSchema, many=True)
    talim = ma.Nested(TalimSchema, many=True)
    pendidikan = ma.Nested(PendidikanSchema, many=True)
    lembFormal = ma.Nested(LembagaPendidikanFormalSchema, many=True)
    lembNonFormal = ma.Nested(LembagaPendidikanNonformalSchema, many=True)
    pendFormal = ma.Nested(PendidikanFormalSchema, many=True)
    lainLain = ma.Nested(LainLainSchema, many=True)
    usaha = ma.Nested(UsahaSchema, many=True)
    fasilitas = ma.Nested(FasilitasSchema, many=True)
    class Meta:
        fields = ('pesantren_id', 'pesantren', 'yayasan', 'pendiri', 'alamat', 'kecamatan', 'kabupaten', 'gmaps',
                  'instagram', 'facebook', 'twitter', 'website', 'pengasuh', 'daftarPengasuh', 'sanad', 'talim', 'pendidikan',
                  'lembFormal', 'lembNonFormal', 'pendFormal', 'lainLain', 'usaha', 'fasilitas', 'deskripsi', 'foto_filename')

pesantren_schema = PesantrenSchema()
pesantrens_schema = PesantrenSchema(many=True)