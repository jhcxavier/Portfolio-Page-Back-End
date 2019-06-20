from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy import Table, Column, Integer, ForeignKey

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(80), unique=True, nullable=True)
    lastname = db.Column(db.String(80), unique=True, nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=True)
    password = db.Column(db.String(80), unique=True, nullable=True)
    dobDate = db.Column(db.String(10), unique=True, nullable=True)
    imageURL = db.Column(db.String(120), unique=True, nullable=True)
    resumeStyle = db.Column(db.String(120), unique=True, nullable=True)
    theme = db.Column(db.String(120), unique=True, nullable=True)
    title = db.Column(db.String(120), unique=True, nullable=True)
    product = db.relationship('Product', lazy=True)
    about = db.relationship('About', lazy=True)
    experience = db.relationship('Experience', lazy=True)
    #children = relationship("Child")
    #products = db.relationship('Product', backref='User', lazy=True)
    def __repr__(self):
        return '<User %r>' % self.firstname

    def serialize(self):
        experiences = []
        for e in self.experience:
            experiences.append(e.serialize())

        return {
            "firstname": self.firstname,
            "lastname": self.lastname,
            "email": self.email,
            "password": self.password,
            "dobDate": self.dobDate,
            "imageURL": self.imageURL,
            "resumeStyle": self.resumeStyle,
            "theme": self.theme,
            "title": self.title,
            "id": self.id,
            "experiences": experiences
        }

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(80), nullable=True)
    date = db.Column(db.String(80), nullable=True)
    url = db.Column(db.String(80), nullable=True)
    page = db.Column(db.Boolean(80), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    #children = relationship("Child")
    #products = db.relationship('Product', backref='User', lazy=True)

    def __repr__(self):
        return '<Product %r>' % self.description

    def serialize(self):
        return {
            "description": self.description,
            "date": self.date,
            "url": self.url,
            "page": self.page,
            "user_id": self.user_id,
            "id": self.id

        }

class About(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(80), nullable=True)
    resume = db.Column(db.String(80), nullable=True)
    page = db.Column(db.String(80), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    #children = relationship("Child")
    #products = db.relationship('Product', backref='User', lazy=True)

    def __repr__(self):
        return '<About %r>' % self.description

    def serialize(self):
        return {
            "description": self.description,
            "resume": self.resume,
            "page": self.page,
            "user_id": self.user_id,
            "id": self.id

        }

class Experience(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=True)
    company = db.Column(db.String(80), nullable=True)
    description = db.Column(db.String(80), nullable=True)
    fromDate = db.Column(db.String(80), nullable=True)
    toDate = db.Column(db.String(80), nullable=True)
    resume = db.Column(db.String(80), nullable=True)
    page = db.Column(db.String(80), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    #children = relationship("Child")
    #products = db.relationship('Product', backref='User', lazy=True)

    def __repr__(self):
        return '<Experience %r>' % self.title

    def serialize(self):
        return {
            "title": self.title,
            "company": self.company,
            "description": self.description,
            "fromDate": self.fromDate,
            "toDate": self.toDate,
            "resume": self.resume,
            "page": self.page,
            "id": self.id

        }