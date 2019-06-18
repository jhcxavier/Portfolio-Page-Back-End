from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy import Table, Column, Integer, ForeignKey

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(80), unique=True, nullable=False)
    lastname = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=True, nullable=False)
    dobDate = db.Column(db.String(10), unique=True, nullable=False)
    imageURL = db.Column(db.String(120), unique=True, nullable=False)
    resumeStyle = db.Column(db.String(120), unique=True, nullable=False)
    theme = db.Column(db.String(120), unique=True, nullable=False)
    title = db.Column(db.String(120), unique=True, nullable=False)
    products = db.relationship('Product', backref='user', lazy=True)
    #children = relationship("Child")
    #products = db.relationship('Product', backref='User', lazy=True)
    def __repr__(self):
        return '<User %r>' % self.firstname

    def serialize(self):
        # products = []
        # for g in self.products:
        #     products.append(g.serialize())
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
            # "products": products
        }

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(80), unique=True, nullable=False)
    date = db.Column(db.Date(80), unique=True, nullable=False)
    url = db.Column(db.String(80), unique=True, nullable=False)
    page = db.Column(db.Boolean(80), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    #children = relationship("Child")
    #products = db.relationship('Product', backref='User', lazy=True)
   
    def __repr__(self):
        return '<Product %r>' % self.firstname

    def serialize(self):
        return {
            "description": self.description,
            "date": self.date,
            "url": self.url,
            "page": self.page,
            "id": self.id

        }