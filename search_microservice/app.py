# search_microservice/app.py
from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_
from models import db, Book, Autor, Categorie

main = Flask(__name__)
main.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://mysql:mysql_password@mysql/library_db'
main.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(main)

@main.route('/search', methods=['POST'])
def search():
    search_term = request.form.get('search_term')

    if not search_term:
        return render_template('search.html', results=[])

    results = Book.query.join(Autor).join(Categorie).filter(
        or_(
            Book.book_name.ilike(f"%{search_term}%"),
            Autor.nume.ilike(f"%{search_term}%"),
            Autor.prenume.ilike(f"%{search_term}%"),
            Categorie.descriere.ilike(f"%{search_term}%")
        )
    ).all()

    formatted_results = [
        {
            'book_name': result.book_name,
            'author_name': f"{result.autor.nume} {result.autor.prenume}",
            'category': result.categorie.descriere
        } for result in results
    ]

    return render_template('search.html', results=formatted_results)

@main.route('/search', methods=['GET'])
def show_search_page():
    return render_template('search.html')

if __name__ == '__main__':
    main.run(debug=True, host='0.0.0.0')

