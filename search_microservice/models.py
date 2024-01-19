from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Utilizator(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    cnp = db.Column(db.String(13), unique=True, nullable=False)
    phone = db.Column(db.String(15), nullable=False)

class Autor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nume = db.Column(db.String(50), nullable=False)
    prenume = db.Column(db.String(50), nullable=False)

class Categorie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    descriere = db.Column(db.String(50), nullable=False)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    idau = db.Column(db.Integer, db.ForeignKey('autor.id'))
    book_name = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer)
    idca = db.Column(db.Integer, db.ForeignKey('categorie.id'))
    autor = db.relationship('Autor', foreign_keys=[idau])
    categorie = db.relationship('Categorie', foreign_keys=[idca])

class Rezervari(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    datastart = db.Column(db.Date, nullable=False)
    datastop = db.Column(db.Date, nullable=False)
    idc = db.Column(db.Integer, db.ForeignKey('book.id'))  # Adaugă cheia străină pentru Book
    idu = db.Column(db.Integer, db.ForeignKey('utilizator.id'))  # Adaugă cheia străină pentru Utilizator
    # Adaugă cheile străine
    book = db.relationship('Book', foreign_keys=[idc])
    utilizator = db.relationship('Utilizator', foreign_keys=[idu])

class Lectura(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    denumire = db.Column(db.String(100), nullable=False)
    perioada = db.Column(db.String(50), nullable=False)
    idc = db.Column(db.Integer, db.ForeignKey('book.id'))  # Adaugă cheia străină pentru Book
    idu = db.Column(db.Integer, db.ForeignKey('utilizator.id'))  # Adaugă cheia străină pentru Utilizator
    datasala = db.Column(db.Date)
    # Adaugă cheile străine
    book = db.relationship('Book', foreign_keys=[idc])
    utilizator = db.relationship('Utilizator', foreign_keys=[idu])
