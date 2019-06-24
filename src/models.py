from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy import Table, Column, Integer, ForeignKey

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(80), unique=False, default="")
    lastname = db.Column(db.String(80), unique=False, default="")
    email = db.Column(db.String(120), unique=True, default="")
    password = db.Column(db.String(80), unique=False, default="")
    dobDate = db.Column(db.String(10), unique=False, default="")
    imageURL = db.Column(db.String(120), unique=False, default="")
    resumeStyle = db.Column(db.String(120), unique=False, default="")
    theme = db.Column(db.String(120), unique=False, default="")
    title = db.Column(db.String(120), unique=False, default="")
    about = db.relationship('About', lazy=True)
    product = db.relationship('Product', lazy=True)
    experience = db.relationship('Experience', lazy=True)
    education = db.relationship('Education', lazy=True)
    skills = db.relationship('Skills', lazy=True)

    def __repr__(self):
        return '<User %r>' % self.firstname

    def serialize(self):
        experiences = []
        for e in self.experience:
            experiences.append(e.serialize())
        education = []
        for e in self.education:
            education.append(e.serialize())
        skills = []
        for e in self.skills:
            skills.append(e.serialize())

        return {
            "user": {
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
                "porpuse": self.purpose,
                "display": self.objective
            },
            "experience": experiences,
            "education": education,
            "skills": skills,
            "about": [
				{
					"description":
						"I really enjoy coding and helping out others, my favorite subject to read is about aliens and other civilizations.\nThis is just some writing so we can see how it looks when there is a good amount of context. Maybe I can create some more content to fill up.",
					"resume": "true",
					"page": "false"
				},
				{
					"description": "Another about me section in case I want a different one in the resume from the page.",
					"resume": "false",
					"page": "true"
				}
			],
			"purpose": [
				{
					"description": "Helping companies reach their goals by serving them great mate.",
					"resume": "true",
					"page": "true"
				}
			],
            "links": [
				{
					"url": "https://www.linkedin.com/in/hernan-garcia-448400186/"
				},
				{
					"url": "https://github.com/hernanjkd"
				}
			]
        }

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(80), default="")
    date = db.Column(db.String(80), default="")
    url = db.Column(db.String(80), default="")
    page = db.Column(db.Boolean(80), default="")
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), default="")

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
    description = db.Column(db.String(80), default="")
    resume = db.Column(db.String(80), default="")
    page = db.Column(db.String(80), default="")
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), default="")

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
    title = db.Column(db.String(80), default="")
    company = db.Column(db.String(80), default="")
    description = db.Column(db.String(80), default="")
    fromDate = db.Column(db.String(80), default="")
    toDate = db.Column(db.String(80), default="")
    resume = db.Column(db.String(140), default="False")
    page = db.Column(db.String(120), default="False")
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), default="")

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

class Education(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    school = db.Column(db.String(120), default="")
    degree = db.Column(db.String(120), default="")
    course = db.Column(db.String(120), default="")
    fromDate = db.Column(db.String(80), default="")
    toDate = db.Column(db.String(80), default="")
    resume = db.Column(db.String(140), default="False")
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), default="")

    def __repr__(self):
        return '<Education %r>' % self.school

    def serialize(self):
        return {
            "school": self.school,
            "degree": self.degree,
            "course": self.course,
            "fromDate": self.fromDate,
            "toDate": self.toDate,
            "resume": self.resume,
            "id": self.id

        }

class Skills(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    skill = db.Column(db.String(120), default="")
    resume = db.Column(db.String(140), default="False")
    page = db.Column(db.String(140), default="False")
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), default="")

    def __repr__(self):
        return '<Skills %r>' % self.skill

    def serialize(self):
        return {
            "skill": self.skill,
            "resume": self.resume,
            "page": self.page,
            "id": self.id
        }

