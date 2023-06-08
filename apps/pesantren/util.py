import os
import uuid

from apps.pesantren.models import *
from apps import config, db

from flask import jsonify

# def add_pesantren(data):
#     # Ambil data dari permintaan POST
#     pesantren_data = data

#     # Buat objek Pesantren
#     pesantren = Pesantren(pesantren=pesantren_data['pesantren'],
#                             yayasan=pesantren_data['yayasan'],
#                             pendiri=pesantren_data['pendiri'],
#                             pengasuh=pesantren_data['pengasuh'])

#     # Buat objek AlamatPesantren
#     alamat_pesantren = AlamatPesantren(alamat=pesantren_data['alamat']['alamat'],
#                                         kecamatan=pesantren_data['alamat']['kecamatan'],
#                                         kabupaten=pesantren_data['alamat']['kabupaten'])

#     # Tambahkan alamat_pesantren ke pesantren
#     pesantren.alamat = alamat_pesantren

#     # Buat objek KeilmuanPesantren
#     keilmuan_pesantren = KeilmuanPesantren(sanad=pesantren_data['keilmuan']['sanad'],
#                                             talim=pesantren_data['keilmuan']['talim'],
#                                             pendidikan=pesantren_data['keilmuan']['pendidikan'])
#     pesantren.keilmuan = keilmuan_pesantren
#     # Buat objek LembagaPendidikanPesantren
#     lembaga_pendidikan_pesantren = LembagaPendidikanPesantren(lembFormal=pesantren_data['lembaga_pendidikan']['lembFormal'],
#                                                                 lembNonFormal=pesantren_data['lembaga_pendidikan']['lembNonFormal'],
#                                                                 pendFormal=pesantren_data['lembaga_pendidikan']['pendFormal'],
#                                                                 lainLain=pesantren_data['lembaga_pendidikan']['lainLain'])

#     # Tambahkan keilmuan_pesantren dan lembaga_pendidikan_pesantren ke pesantren
#     pesantren.lembaga_pendidikan = lembaga_pendidikan_pesantren
#     # Buat objek InformasiTambahan
#     informasi_tambahan_pesantren = InformasiTambahan(usaha=pesantren_data['informasi_tambahan']['usaha'],
#                                             gmaps=pesantren_data['informasi_tambahan']['gmaps'])

#     pesantren.informasi_tambahan = informasi_tambahan_pesantren
#     # Buat objek Media
#     media = Media(instagram=pesantren_data['media']['instagram'],
#                     facebook=pesantren_data['media']['facebook'],
#                     twitter=pesantren_data['media']['twitter'],
#                     website=pesantren_data['media']['website'])

#     # Tambahkan informasi_tambahan dan media ke pesantren
#     pesantren.media = media

#     # Commit perubahan ke database
#     db.session.add(pesantren)
#     db.session.commit()

#     return jsonify({'message': 'Pesantren added successfully'}), 200

def add_pesantren(data):
    # Ambil data dari permintaan POST
    pesantren_data = data

    # Buat objek Pesantren
    pesantren = Pesantren(
        pesantren=pesantren_data['pesantren'],
        yayasan=pesantren_data['yayasan'],
        pendiri=pesantren_data['pendiri']
    )

    # Tambahkan pengasuh ke pesantren
    pengasuh = [Pengasuh(nama=nama) for nama in pesantren_data['pengasuh']]
    pesantren.pengasuh = pengasuh

    # Buat objek AlamatPesantren
    alamat_pesantren = AlamatPesantren(
        alamat=pesantren_data['alamat']['alamat'],
        kecamatan=pesantren_data['alamat']['kecamatan'],
        kabupaten=pesantren_data['alamat']['kabupaten']
    )

    # Tambahkan alamat_pesantren ke pesantren
    pesantren.alamat = alamat_pesantren

    # Buat objek KeilmuanPesantren
    keilmuan_pesantren = KeilmuanPesantren(
        sanad=pesantren_data['keilmuan']['sanad'],
        talim=[KeilmuanPesantren(talim=nama) for nama in pesantren_data['keilmuan']['talim']],
        pendidikan=[KeilmuanPesantren(pendidikan=nama) for nama in pesantren_data['keilmuan']['pendidikan']]
    )
    pesantren.keilmuan = keilmuan_pesantren

    # Buat objek LembagaPendidikanPesantren
    lembaga_pendidikan_pesantren = LembagaPendidikanPesantren(
        lembFormal=[LembagaPendidikanPesantren(lembFormal=nama) for nama in pesantren_data['lembaga_pendidikan']['lembFormal']],
        lembNonFormal=[LembagaPendidikanPesantren(lembNonFormal=nama) for nama in pesantren_data['lembaga_pendidikan']['lembNonFormal']],
        pendFormal=[LembagaPendidikanPesantren(pendFormal=nama) for nama in pesantren_data['lembaga_pendidikan']['pendFormal']],
        lainLain=[LembagaPendidikanPesantren(lainLain=nama) for nama in pesantren_data['lembaga_pendidikan']['lainLain']]
    )

    # Tambahkan lembaga_pendidikan_pesantren ke pesantren
    pesantren.lembaga_pendidikan = lembaga_pendidikan_pesantren

    # Buat objek InformasiTambahan
    informasi_tambahan_pesantren = InformasiTambahan(
        gmaps=pesantren_data['informasi_tambahan']['gmaps'],
    )
    
    # Tambahkan informasi_tambahan_pesantren ke pesantren
    pesantren.informasi_tambahan = informasi_tambahan_pesantren

    usaha = [Usaha(nama=nama) for nama in pesantren_data['informasi_tambahan']['usaha']]
    
    pesantren.usaha = usaha
    # Buat objek Media
    media = Media(
        instagram=pesantren_data['media']['instagram'],
        facebook=pesantren_data['media']['facebook'],
        twitter=pesantren_data['media']['twitter'],
        website=pesantren_data['media']['website']
    )

    # Tambahkan media ke pesantren
    pesantren.media = media

    # Commit perubahan ke database
    db.session.add(pesantren)
    db.session.commit()

    return jsonify({'message': 'Pesantren added successfully'}), 200

def update_pesantren(pesantren_id, data):
    pesantren = Pesantren.query.get(pesantren_id)
    if not pesantren:
        return {'error': 'Pesantren not found'}, 404

    # Memperbarui data pesantren
    pesantren.pesantren = data['pesantren']
    pesantren.yayasan = data['yayasan']
    pesantren.pendiri = data['pendiri']
    pesantren.pengasuh = data['pengasuh']

    # Memperbarui data alamat pesantren
    alamat_pesantren = pesantren.alamat
    alamat_pesantren.alamat = data['alamat_pesantren']
    alamat_pesantren.kecamatan = data['kecamatan']
    alamat_pesantren.kabupaten = data['kabupaten']

    # Memperbarui data keilmuan pesantren
    keilmuan_pesantren = KeilmuanPesantren.query.filter_by(pesantren_id=pesantren.id).first()
    keilmuan_pesantren.sanad = data['sanad']
    keilmuan_pesantren.talim = data['talim']
    keilmuan_pesantren.pendidikan = data['pendidikan']

    # Memperbarui data lembaga pendidikan pesantren
    lembaga_pendidikan_pesantren = LembagaPendidikanPesantren.query.filter_by(pesantren_id=pesantren.id).first()
    lembaga_pendidikan_pesantren.lembFormal = data['lembFormal']
    lembaga_pendidikan_pesantren.lembNonFormal = data['lembNonFormal']
    lembaga_pendidikan_pesantren.pendFormal = data['pendFormal']
    lembaga_pendidikan_pesantren.lainLain = data['lainLain']

    # Memperbarui data informasi tambahan
    informasi_tambahan = InformasiTambahan.query.filter_by(pesantren_id=pesantren.id).first()
    informasi_tambahan.usaha = data['usaha']
    informasi_tambahan.gmaps = data['gmaps']

    # Memperbarui data foto pesantren
    foto_pesantren = FotoPesantren.query.filter_by(pesantren_id=pesantren.id).first()
    foto_pesantren.foto = data['foto']

    # Commit perubahan ke database
    db.session.commit()

    return {'message': 'Pesantren updated successfully'}, 200


def delete_pesantren(pesantren_id):
    pesantren = Pesantren.query.get(pesantren_id)
    if not pesantren:
        return jsonify({'error': 'Pesantren not found'}), 404

    db.session.delete(pesantren)
    db.session.commit()

    return jsonify({'message': 'Pesantren deleted successfully'}), 200

def get_all_pesantren():
    pesantren_list = Pesantren.query.all()

    data = []
    for pesantren in pesantren_list:
        # Mengambil data yang diperlukan dari setiap objek pesantren
        nama = pesantren.pesantren
        yayasan_pengasuh = pesantren.yayasan + '/' + pesantren.pengasuh
        alamat = pesantren.alamat
        # fasilitas = pesantren.fasilitas

        # Mengambil foto pesantren
        foto_pesantren = FotoPesantren.query.filter_by(pesantren_id=pesantren.id).first()
        foto = foto_pesantren.foto if foto_pesantren else None

        # Membuat dictionary dengan data yang diperlukan
        pesantren_data = {
            'id': pesantren.id,
            'pesantren': nama,
            'yayasan_pengasuh': yayasan_pengasuh,
            'alamat': alamat.alamat + ', ' + alamat.kecamatan + ', ' + alamat.kabupaten,
            # 'Fasilitas': fasilitas,
            'foto': foto
        }
        data.append(pesantren_data)

    return jsonify(data), 200

def get_pesantren(pesantren_id):
    pesantren = Pesantren.query.get(pesantren_id)
    if not pesantren:
        return jsonify({'error': 'Pesantren not found'}), 404

    # Mengambil data yang diperlukan dari objek pesantren
    nama = pesantren.pesantren
    yayasan_pengasuh = pesantren.yayasan + '/' + pesantren.pengasuh
    alamat = pesantren.alamat
    # fasilitas = pesantren.fasilitas

    # Mengambil foto pesantren
    foto_pesantren = FotoPesantren.query.filter_by(pesantren_id=pesantren.id).first()
    foto = foto_pesantren.foto if foto_pesantren else None

    # Membuat dictionary dengan data yang diperlukan
    data = {
        'id': pesantren.id,
        'pesantren': nama,
        'yayasan_pengasuh': yayasan_pengasuh,
        'alamat': alamat.alamat + ', ' + alamat.kecamatan + ', ' + alamat.kabupaten,
        # 'Fasilitas': fasilitas,
        'foto': foto
    }

    return jsonify(data), 200

def detail_pesantren(pesantren_id):
    pesantren = Pesantren.query.get(pesantren_id)
    if not pesantren:
        return jsonify({'error': 'Pesantren not found'}), 404

    # Mengambil data yang diperlukan dari objek pesantren
    nama = pesantren.pesantren
    yayasan_pengasuh = pesantren.yayasan + '/' + pesantren.pengasuh
    alamat = pesantren.alamat
    # fasilitas = pesantren.fasilitas

    # Mengambil lembaga pendidikan pesantren
    lembaga_pendidikan_pesantren = LembagaPendidikanPesantren.query.filter_by(pesantren_id=pesantren.id).first()
    lembaga_pendidikan = {
        'lembFormal': lembaga_pendidikan_pesantren.lembFormal,
        'lembNonFormal': lembaga_pendidikan_pesantren.lembNonFormal,
        'pendFormal': lembaga_pendidikan_pesantren.pendFormal,
        'lainLain': lembaga_pendidikan_pesantren.lainLain
    }

    # Mengambil foto pesantren
    foto_pesantren = FotoPesantren.query.filter_by(pesantren_id=pesantren.id).first()
    foto = foto_pesantren.foto if foto_pesantren else None

    # Membuat dictionary dengan data yang diperlukan
    data = {
        'pesantren': nama,
        'yayasan_pengasuh': yayasan_pengasuh,
        'pendidikan': lembaga_pendidikan,
        'alamat': alamat.alamat + ', ' + alamat.kecamatan + ', ' + alamat.kabupaten,
        # 'Fasilitas': fasilitas,
        'foto': foto
    }

    return jsonify(data), 200
