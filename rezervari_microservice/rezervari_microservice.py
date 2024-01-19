# microserviciu_rezervari.py
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from datetime import datetime
from models import db, Book, Utilizator, Rezervari

app_rezervari = Flask(__name__)
app_rezervari.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://mysql:mysql_password@mysql/library_db'
app_rezervari.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app_rezervari.config['SECRET_KEY'] = 'secret_key'
db.init_app(app_rezervari)

@app_rezervari.route('/rezervari')
def rezervari():
    rezervari = Rezervari.query.all()
    return render_template('rezervari-list.html', rezervari=rezervari)

@app_rezervari.route('/rezervari/adauga_rezervare', methods=['GET', 'POST'])
def adauga_rezervare():
    if request.method == 'POST':
        try:
            # Preia datele din formular
            book_id = request.form.get('book_id')
            utilizator_id = request.form.get('utilizator_id')
            data_start = request.form.get('dataStart')
            data_stop = request.form.get('dataStop')

            # Crează o nouă rezervare și adauga în baza de date
            rezervare = Rezervari(
                idc=book_id,
                idu=utilizator_id,
                datastart=data_start,
                datastop=data_stop
            )
            db.session.add(rezervare)
            db.session.commit()

            return redirect(url_for('rezervari'))

        except IntegrityError:
            db.session.rollback()
            return redirect(url_for('adauga_rezervare'))

    books = Book.query.all()
    utilizatori = Utilizator.query.all()
    return render_template('rezervari-form.html', books=books, utilizatori=utilizatori)

@app_rezervari.route('/rezervari/sterge_rezervare', methods=['GET', 'POST'])
def sterge_rezervare():
    if request.method == 'POST':
        rezervare_id = request.form.get('rezervareId')
        rezervare = Rezervari.query.get(rezervare_id)

        if rezervare:
            db.session.delete(rezervare)
            db.session.commit()

            return redirect(url_for('rezervari'))

    rezervari = Rezervari.query.all()
    return render_template('rezervari-delete.html', rezervari=rezervari)

if __name__ == '__main__':
    app_rezervari.run(debug=True, host='0.0.0.0')
