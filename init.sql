-- init.sql


CREATE DATABASE IF NOT EXISTS library_db;

USE library_db;

SET foreign_key_checks = 0;

DROP TABLE IF EXISTS utilizator;
CREATE TABLE utilizator (
    id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    cnp VARCHAR(13) UNIQUE NOT NULL,
    phone VARCHAR(15) NOT NULL
);

DROP TABLE IF EXISTS autor;
CREATE TABLE autor (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nume VARCHAR(50) NOT NULL,
    prenume VARCHAR(50) NOT NULL
);
DROP TABLE IF EXISTS categorie;

CREATE TABLE categorie (
    id INT AUTO_INCREMENT PRIMARY KEY,
    descriere VARCHAR(50) NOT NULL
);

DROP TABLE IF EXISTS book;
CREATE TABLE book (
    id INT AUTO_INCREMENT PRIMARY KEY,
    idau INT,
    book_name VARCHAR(100) NOT NULL,
    year INT,
    idca INT,
    FOREIGN KEY (idau) REFERENCES autor(id),
    FOREIGN KEY (idca) REFERENCES categorie(id)
);

DROP TABLE IF EXISTS rezervari;
CREATE TABLE rezervari (
    id INT AUTO_INCREMENT PRIMARY KEY,
    datastart DATE NOT NULL,
    datastop DATE NOT NULL,
    idc INT,
    idu INT,
    FOREIGN KEY (idc) REFERENCES book(id),
    FOREIGN KEY (idu) REFERENCES utilizator(id)
);

DROP TABLE IF EXISTS lectura;
CREATE TABLE lectura (
    id INT AUTO_INCREMENT PRIMARY KEY,
    denumire VARCHAR(100) NOT NULL,
    perioada VARCHAR(50) NOT NULL,
    idc INT,
    idu INT,
    datasala DATE,
    FOREIGN KEY (idc) REFERENCES book(id),
    FOREIGN KEY (idu) REFERENCES utilizator(id)
);

DROP TABLE IF EXISTS user;
CREATE TABLE user (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(100) NOT NULL
);

SET foreign_key_checks = 1;


insert into utilizator (first_name, last_name, cnp, phone) values ('Ionut', 'Pop', 1850517140, 471234567);
insert into utilizator (first_name,last_name,cnp,phone) values ( 'Florin', 'Mihai', 1950517140, 471234567);

insert into autor (nume,prenume) values ('Eminescu','Mihai');
insert into autor (nume,prenume) values ('Sadoveanu','Mihail');

insert into categorie (descriere) values ('Poezii');
insert into categorie (descriere)  values ('Povesti');

insert into book (idau, book_name, year,idca) values (1,'Fat-Frumos din lacrima',1870,2);
insert into book (idau, book_name, year,idca) values (1,'Legenda Luceafarului',2008,1);
insert into book (idau, book_name, year,idca) values (1,'Poezie',2014,1);

insert into book (idau, book_name, year,idca) values (2,'Dumbrava minunata',2013,2);
insert into book (idau, book_name, year,idca) values (2,'Baltagul',2013,2);
insert into book (idau, book_name, year,idca) values (2,'Fratii Jderi',2014,2);

INSERT INTO rezervari (datastart, datastop, idc, idu) VALUES (current_date, date_add(current_date, interval 1 DAY), 1, 1);

insert into lectura (denumire, perioada, idc, idu,datasala) values ('Sala 1',3,1,1,current_date);
insert into user (username, password) values ('admin', '123456789');
