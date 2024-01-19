#app.py - aplicatie principala
from flask import Flask, render_template, request, redirect, url_for, jsonify, current_app, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_session import Session
from datetime import datetime
from sqlalchemy import or_
from models import db, Utilizator, Autor, Categorie, Book, Rezervari,Lectura
import requests

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://mysql:mysql_password@mysql/library_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'secret_key'
db.init_app(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __init__(self, user_id, username, password):
        self.id = user_id
        self.username = username
        self.password = password

@login_manager.user_loader
def load_user(user_id):
    return db.session.query(User).get(int(user_id))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and user.password == password:
            login_user(user)
            return redirect(url_for('index'))
        else:
            error = 'Invalid username or password'

    return render_template('login.html', error=error)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/')
@login_required
def index():
    return render_template('index.html')

@app.route('/books')
@login_required
def lista_carti():
    books = Book.query.all()
    return render_template('books-list.html', books=books)

@app.route('/books/adauga_carte', methods=['GET', 'POST'])
@login_required
def adauga_carte():
    if request.method == 'POST':
        book_name = request.form.get('bookName')
        autor_id = request.form.get('autor_id')
        year = request.form.get('year')
        categorie_id = request.form.get('categorie_id')

        if not book_name or not autor_id or not year or not categorie_id:
            return render_template('eroare.html', mesaj='Toate câmpurile sunt obligatorii!')

        year = int(year)
        new_book = Book(book_name=book_name, idau=autor_id, year=year, idca=categorie_id)
        db.session.add(new_book)
        db.session.commit()

        return redirect(url_for('lista_carti'))

    autori = Autor.query.all()
    categorii = Categorie.query.all()
    return render_template('book-form.html', autori=autori, categorii=categorii)

@app.route('/books/sterge_carte', methods=['GET', 'POST'])
@login_required
def sterge_carte():
    if request.method == 'POST':
        book_id = request.form.get('bookId')

        book = Book.query.get(book_id)
        if book:
            db.session.delete(book)
            db.session.commit()
            return redirect(url_for('lista_carti'))

    books = Book.query.all()
    return render_template('book-delete.html', books=books)

@app.route('/books/editare_carte/<int:id>', methods=['GET', 'POST'])
@login_required
def editare_carte(id):
    book = Book.query.get(id)
    autori = Autor.query.all()
    categorii = Categorie.query.all()

    if request.method == 'POST':
        book_name = request.form.get('bookName')
        autor_id = request.form.get('autor_id')
        year = request.form.get('year')
        categorie_id = request.form.get('categorie_id')

        book.book_name = book_name
        book.idau = autor_id
        book.year = year
        book.idca = categorie_id
        db.session.commit()
        return redirect(url_for('lista_carti'))

    return render_template('edit-book.html', book=book, autori=autori, categorii=categorii)

@app.route('/utilizatori')
@login_required
def utilizatori():
    utilizatori = Utilizator.query.all()
    return render_template('utilizatori-list.html', utilizatori=utilizatori)

@app.route('/utilizatori/adauga', methods=['GET', 'POST'])
@login_required
def adauga_utilizator():
    if request.method == 'POST':
        first_name = request.form.get('firstName')
        last_name = request.form.get('lastName')
        cnp = request.form.get('cnp')
        phone = request.form.get('phone')

        utilizator_nou = Utilizator(first_name=first_name, last_name=last_name, cnp=cnp, phone=phone)
        db.session.add(utilizator_nou)
        db.session.commit()

        return redirect(url_for('utilizatori'))

    return render_template('utilizator-form.html')

@app.route('/utilizatori/sterge_utilizator', methods=['GET', 'POST'])
@login_required
def sterge_utilizator():
    if request.method == 'POST':
        utilizator_id = request.form.get('utilizatorId')
        if utilizator_id:
            utilizator = Utilizator.query.get(utilizator_id)

            if utilizator:
                db.session.delete(utilizator)
                db.session.commit()

                return redirect(url_for('utilizatori'))

    utilizatori = Utilizator.query.all()
    return render_template('utilizator-delete.html', utilizatori=utilizatori)

@app.route('/utilizatori/edit_utilizator/<int:utilizator_id>', methods=['GET', 'POST'])
@login_required
def edit_utilizator(utilizator_id):
    utilizator = Utilizator.query.get(utilizator_id)

    if request.method == 'POST':
        firstName = request.form.get('first_name')
        lastName = request.form.get('last_name')
        cnp = request.form.get('cnp')
        phone = request.form.get('phone')

        utilizator.first_name = firstName
        utilizator.last_name = lastName
        utilizator.cnp = cnp
        utilizator.phone = phone

        db.session.commit()

        return redirect(url_for('utilizatori'))

    return render_template('edit-utilizator.html', utilizator=utilizator)


@app.route('/lecturi')
@login_required
def lecturi():
    lista_lecturi = Lectura.query.all()
    return render_template('lecturi-list.html', lecturi=lista_lecturi)

@app.route('/lecturi/adauga_lectura', methods=['GET', 'POST'])
@login_required
def adauga_lectura():
    if request.method == 'POST':
        try:
            denumire = request.form.get('denumire')
            book_id = request.form.get('book_id')
            utilizator_id = request.form.get('utilizator_id')
            perioada = request.form.get('perioada')
            datasala = request.form.get('datasala')

            if not denumire or not book_id or not utilizator_id or not perioada or not datasala:
                flash('Toate câmpurile sunt obligatorii!', 'error')
                return redirect(url_for('adauga_lectura'))

            perioada = int(perioada)

            datasala = datetime.strptime(datasala, '%Y-%m-%d').date()

            new_lectura = Lectura(denumire=denumire, idc=book_id, idu=utilizator_id, perioada=perioada, datasala=datasala)
            db.session.add(new_lectura)
            db.session.commit()

            flash('Inregistrare adaugata cu succes!', 'success')

            return redirect(url_for('lecturi'))

        except IntegrityError:
            db.session.rollback()
            flash('Eroare la adăugarea înregistrării! Asigură-te că cartea și utilizatorul sunt valizi.', 'error')
            return redirect(url_for('adauga_lectura'))

    books = Book.query.all()
    utilizatori = Utilizator.query.all()
    return render_template('lecturi-form.html', books=books, utilizatori=utilizatori)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')