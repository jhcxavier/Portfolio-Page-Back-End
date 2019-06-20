from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy import Table, Column, Integer, ForeignKey

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(80), unique=True, nullable=True, default=None)
    lastname = db.Column(db.String(80), unique=True, nullable=True, default=None)
    email = db.Column(db.String(120), unique=True, nullable=True, default=None)
    password = db.Column(db.String(80), unique=True, nullable=True, default=None)
    dobDate = db.Column(db.String(10), unique=True, nullable=True, default=None)
    imageURL = db.Column(db.String(120), unique=True, nullable=True, default=None)
    resumeStyle = db.Column(db.String(120), unique=True, nullable=True, default=None)
    theme = db.Column(db.String(120), unique=True, nullable=True, default=None)
    title = db.Column(db.String(120), unique=True, nullable=True, default=None)
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
    description = db.Column(db.String(80), nullable=True, default=None)
    date = db.Column(db.String(80), nullable=True, default=None)
    url = db.Column(db.String(80), nullable=True, default=None)
    page = db.Column(db.Boolean(80), nullable=True, default=None)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True, default=None)
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
    description = db.Column(db.String(80), nullable=True, default=None)
    resume = db.Column(db.String(80), nullable=True, default=None)
    page = db.Column(db.String(80), nullable=True, default=None)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True, default=None)
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
    title = db.Column(db.String(80), nullable=True, default=None)
    company = db.Column(db.String(80), nullable=True, default=None)
    description = db.Column(db.String(80), nullable=True, default=None)
    fromDate = db.Column(db.String(80), nullable=True, default=None)
    toDate = db.Column(db.String(80), nullable=True, default=None)
    resume = db.Column(db.String, nullable=True, default="False")
    page = db.Column(db.String, nullable=True, default="False")
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True, default=None)
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