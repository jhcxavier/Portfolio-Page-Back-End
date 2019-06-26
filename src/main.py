"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from models import db, User, Product, About, Experience, Education, Skills
from flask_jwt_simple import (
    JWTManager, jwt_required, create_jwt, get_jwt_identity
)



app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)

app.config['JWT_SECRET_KEY'] = 'we are badass'  # Change this!
jwt = JWTManager(app)

#########################################################################
#JWT Security
#########################################################################

@app.route('/login', methods=['POST'])
def login():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    params = request.get_json()
    password = params.get('password', None)
    email = params.get('email', None)

    if not password:
        return jsonify({"msg": "Missing password parameter"}), 400
    if not email:
        return jsonify({"msg": "Missing email parameter"}), 400

    if password != 'test' or email != 'test':
        return jsonify({"msg": "Bad password or email"}), 401

    # Identity can be any data that is json serializable
    ret = {'jwt': create_jwt(identity=password)}
    return jsonify(ret), 200

###########################################################################

@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.toDict()), error.status_code

@app.route('/')
def sitemap():
    return generate_sitemap(app)


@app.route('/user', methods=['POST', 'GET'])
def handle_user():
    """
    Create person and retrieve all persons
    """

    # POST request
    if request.method == 'POST':
        body = request.get_json()


        if body is None:
            raise APIException("You need to specify the request body as a json object", status_code=400)
        if 'firstname' not in body:
            raise APIException('You need to specify the username', status_code=400)
        if 'email' not in body:
            raise APIException('You need to specify the email', status_code=400)

        user1 = User(
            firstname=body['firstname'],
            lastname=body['lastname'],
            email=body['email'],
            password=body['password'])
           # dobDate=body['dobDate']  )

        db.session.add(user1)
        db.session.commit()
        return "ok", 200

    # GET request
    if request.method == 'GET':
        all_user = User.query.all()
        all_user = list(map(lambda x: x.serialize(), all_user))
        return jsonify(all_user), 200

    return "Invalid Method", 404


@app.route('/user/<int:user_id>', methods=['PUT', 'GET', 'DELETE'])
def get_single_person(user_id):
    """
    Single user
    """

    # PUT request
    if request.method == 'PUT':
        body = request.get_json()
        if body is None:
            raise APIException("You need to specify the request body as a json object", status_code=400)

        user1 = User.query.get(user_id)
        if user1 is None:
            raise APIException('User not found', status_code=404)

        if "firstname" in body:
            user1.firstname = body["firstname"]
        if "email" in body:
            user1.email = body["email"]
        if "lastname" in body:
            user1.lastname = body["lastname"]
        if "password" in body:
            user1.password = body["password"]
        if "dobDate" in body:
            user1.dobDate = body["dobDate"]
        if "imageURL" in body:
            user1.imageURL = body["imageURL"]
        if "resumeStyle" in body:
            user1.resumeStyle = body["resumeStyle"]
        if "theme" in body:
            user1.theme = body["theme"]
        if "title" in body:
            user1.title = body["title"]

        db.session.commit()

        return jsonify(user1.serialize()), 200

    # GET request
    if request.method == 'GET':
        user1 = User.query.get(user_id)
        if user1 is None:
            raise APIException('User not found', status_code=404)
        return jsonify(user1.serialize()), 200

    # DELETE request
    if request.method == 'DELETE':
        user1 = User.query.get(user_id)
        if user1 is None:
            raise APIException('User not found', status_code=404)
        db.session.delete(user1)
        db.session.commit()
        return "ok", 200

    return "Invalid Method", 404

##############################################################################
#Product
##############################################################################

@app.route('/product', methods=['POST', 'GET'])
def handle_product():
    """
    Create product and retrieve all products
    """

    # POST request
    if request.method == 'POST':
        body = request.get_json()

        if body is None:
            raise APIException("You need to specify the request body as a json object", status_code=400)
        if 'description' not in body:
            raise APIException('You need to specify the description', status_code=400)
        if 'date' not in body:
            raise APIException('You need to specify the date', status_code=400)

        product1 = Product(
            description=body['description'],
            date=body['date'],
            url=body['url'],
            page=body['page'],
            user_id=body["user_id"])

        db.session.add(product1)
        db.session.commit()
        return "ok", 200

    # GET request
    if request.method == 'GET':
        all_products = Product.query.all()
        all_products = list(map(lambda x: x.serialize(), all_products))
        return jsonify(all_products), 200

    return "Invalid Method", 404


@app.route('/product/<int:product_id>', methods=['PUT', 'GET', 'DELETE'])
def get_single_product(product_id):
    """
    Single user
    """

    # PUT request
    if request.method == 'PUT':
        body = request.get_json()
        if body is None:
            raise APIException("You need to specify the request body as a json object", status_code=400)

        product1 = Product.query.get(product_id)
        if product1 is None:
            raise APIException('User not found', status_code=404)

        if "description" in body:
            product1.description = body["description"]
        if "date" in body:
            product1.date = body["date"]
        if "url" in body:
            product1.url = body["url"]
        if "page" in body:
            product1.page = body["page"]
        db.session.commit()

        return jsonify(product1.serialize()), 200

    # GET request
    if request.method == 'GET':
        product1 = Product.query.get(product_id)
        if product1 is None:
            raise APIException('User not found', status_code=404)
        return jsonify(product1.serialize()), 200

    # DELETE request
    if request.method == 'DELETE':
        product1 = Product.query.get(product_id)
        if product1 is None:
            raise APIException('User not found', status_code=404)
        db.session.delete(product1)
        db.session.commit()
        return "ok", 200

    return "Invalid Method", 404

################################################################################
#About
################################################################################

@app.route('/about', methods=['POST', 'GET'])
def handle_about():
    """
    Create about and retrieve it all
    """

    # POST request
    if request.method == 'POST':
        body = request.get_json()

        if body is None:
            raise APIException("You need to specify the request body as a json object", status_code=400)
        if 'description' not in body:
            raise APIException('You need to specify the description', status_code=400)
        if 'resume' not in body:
            raise APIException('You need to specify the resume', status_code=400)

        about1 = About(
            description=body['description'],
            resume=body['resume'],
            page=body['page'],
            user_id=body["user_id"])

        db.session.add(about1)
        db.session.commit()
        return "ok", 200

    # GET request
    if request.method == 'GET':
        all_about = About.query.all()
        all_about = list(map(lambda x: x.serialize(), all_about))
        return jsonify(all_about), 200

    return "Invalid Method", 404


@app.route('/about/<int:about_id>', methods=['PUT', 'GET', 'DELETE'])
def get_single_about(about_id):
    """
    Single user
    """

    # PUT request
    if request.method == 'PUT':
        body = request.get_json()
        if body is None:
            raise APIException("You need to specify the request body as a json object", status_code=400)

        about1 = About.query.get(about_id)
        if about1 is None:
            raise APIException('User not found', status_code=404)

        if "description" in body:
            about1.description = body["description"]
        if "resume" in body:
            about1.resume = body["resume"]
        if "page" in body:
            about1.page = body["page"]

        db.session.commit()

        return jsonify(about1.serialize()), 200

    # GET request
    if request.method == 'GET':
        about1 = About.query.get(about_id)
        if about1 is None:
            raise APIException('User not found', status_code=404)
        return jsonify(about1.serialize()), 200

    # DELETE request
    if request.method == 'DELETE':
        about1 = About.query.get(about_id)
        if about1 is None:
            raise APIException('User not found', status_code=404)
        db.session.delete(about1)
        db.session.commit()
        return "ok", 200

    return "Invalid Method", 404

###############################################################################
#Experience
###############################################################################

@app.route('/experience', methods=['POST', 'GET'])
def handle_experience():
    """
    Create experience and retrieve it all
    """

    # POST request
    if request.method == 'POST':
        body = request.get_json()

        if body is None:
            raise APIException("You need to specify the request body as a json object", status_code=400)
        if 'title' not in body:
            raise APIException('You need to specify the title', status_code=400)
        if 'company' not in body:
            raise APIException('You need to specify the company', status_code=400)

        experience1 = Experience(
            title=body['title'],
            company=body['company'],
            description=body['description'],
            fromDate=body['fromDate'],
            toDate=body['toDate'],
            resume=body['resume'],
            page=body["page"],
            user_id=body["user_id"])

        db.session.add(experience1)
        db.session.commit()
        return "ok", 200

    # GET request
    if request.method == 'GET':
        all_experience = Experience.query.all()
        all_experience = list(map(lambda x: x.serialize(), all_experience))
        return jsonify(all_experience), 200

    return "Invalid Method", 404


@app.route('/experience/<int:experience_id>', methods=['PUT', 'GET', 'DELETE'])
def get_single_experience(experience_id):
    """
    Single user
    """

    # PUT request
    if request.method == 'PUT':
        body = request.get_json()
        if body is None:
            raise APIException("You need to specify the request body as a json object", status_code=400)

        experience1 = Experience.query.get(experience_id)
        if experience1 is None:
            raise APIException('User not found', status_code=404)

        if "title" in body:
            experience1.title = body["title"]
        if "company" in body:
            experience1.company = body["company"]
        if "description" in body:
            experience1.description = body["description"]
        if "fromDate" in body:
            experience1.fromDate = body["fromDate"]
        if "toDate" in body:
            experience1.toDate = body["toDate"]
        if "resume" in body:
            experience1.resume = body["resume"]
        if "page" in body:
            experience1.page = body["page"]
        db.session.commit()

        return jsonify(experience1.serialize()), 200

    # GET request
    if request.method == 'GET':
        experience1 = Experience.query.get(experience_id)
        if experience1 is None:
            raise APIException('User not found', status_code=404)
        return jsonify(experience1.serialize()), 200

    # DELETE request
    if request.method == 'DELETE':
        experience1 = Experience.query.get(experience_id)
        if experience1 is None:
            raise APIException('User not found', status_code=404)
        db.session.delete(experience1)
        db.session.commit()
        return "ok", 200

    return "Invalid Method", 404

###############################################################################
#Education
###############################################################################

@app.route('/education', methods=['POST', 'GET'])
def handle_education():
    """
    Create education and retrieve it all
    """

    # POST request
    if request.method == 'POST':
        body = request.get_json()

        if body is None:
            raise APIException("You need to specify the request body as a json object", status_code=400)
        if 'school' not in body:
            raise APIException('You need to specify the school', status_code=400)
        if 'degree' not in body:
            raise APIException('You need to specify the degree', status_code=400)

        education1 = Education(
            school=body['school'],
            degree=body['degree'],
            course=body['course'],
            fromDate=body['fromDate'],
            toDate=body['toDate'],
            resume=body['resume'],
            user_id=body["user_id"])

        db.session.add(education1)
        db.session.commit()
        return "ok", 200

    # GET request
    if request.method == 'GET':
        all_education = Education.query.all()
        all_education = list(map(lambda x: x.serialize(), all_education))
        return jsonify(all_education), 200

    return "Invalid Method", 404


@app.route('/education/<int:education_id>', methods=['PUT', 'GET', 'DELETE'])
def get_single_education(education_id):
    """
    Single user
    """

    # PUT request
    if request.method == 'PUT':
        body = request.get_json()
        if body is None:
            raise APIException("You need to specify the request body as a json object", status_code=400)

        education1 = Education.query.get(education_id)
        if education1 is None:
            raise APIException('User not found', status_code=404)

        if "school" in body:
            education1.school = body["school"]
        if "degree" in body:
            education1.degree = body["degree"]
        if "course" in body:
            education1.course = body["course"]
        if "fromDate" in body:
            education1.fromDate = body["fromDate"]
        if "toDate" in body:
            education1.toDate = body["toDate"]
        if "resume" in body:
            education1.resume = body["resume"]

        db.session.commit()

        return jsonify(education1.serialize()), 200

    # GET request
    if request.method == 'GET':
        education1 = Experience.query.get(education_id)
        if education1 is None:
            raise APIException('User not found', status_code=404)
        return jsonify(education1.serialize()), 200

    # DELETE request
    if request.method == 'DELETE':
        education1 = Education.query.get(education_id)
        if education1 is None:
            raise APIException('User not found', status_code=404)
        db.session.delete(education1)
        db.session.commit()
        return "ok", 200

    return "Invalid Method", 404

############################################################################
#Skills
############################################################################

@app.route('/skills', methods=['POST', 'GET'])
def handle_skills():
    """
    Create skill and retrieve it all
    """

    # POST request
    if request.method == 'POST':
        body = request.get_json()

        if body is None:
            raise APIException("You need to specify the request body as a json object", status_code=400)
        if 'skill' not in body:
            raise APIException('You need to specify the skill', status_code=400)
        if 'resume' not in body:
            raise APIException('You need to specify the resume', status_code=400)

        skill1 = Skills(
            skill=body['skill'],
            resume=body['resume'],
            page=body['page'],
            user_id=body["user_id"])

        db.session.add(skill1)
        db.session.commit()
        return "ok", 200

    # GET request
    if request.method == 'GET':
        all_skill = Skills.query.all()
        all_skill = list(map(lambda x: x.serialize(), all_skill))
        return jsonify(all_skill), 200

    return "Invalid Method", 404


@app.route('/skills/<int:skill_id>', methods=['PUT', 'GET', 'DELETE'])
def get_single_skills(skill_id):
    """
    Single user
    """

    # PUT request
    if request.method == 'PUT':
        body = request.get_json()
        if body is None:
            raise APIException("You need to specify the request as a json object", status_code=400)

        skill1 = Skills.query.get(skill_id)
        if skill1 is None:
            raise APIException('User not found', status_code=404)

        if "skill" in body:
            skill1.skill = body["skill"]
        if "resume" in body:
            skill1.resume = body["resume"]
        if "page" in body:
            skill1.page = body["page"]

        db.session.commit()

        return jsonify(skill1.serialize()), 200

    # GET request
    if request.method == 'GET':
        skill1 = Skills.query.get(skill_id)
        if skill1 is None:
            raise APIException('User not found', status_code=404)
        return jsonify(skill1.serialize()), 200

    # DELETE request
    if request.method == 'DELETE':
        skill1 = Skills.query.get(skill_id)
        if skill1 is None:
            raise APIException('User not found', status_code=404)
        db.session.delete(skill1)
        db.session.commit()
        return "ok", 200

    return "Invalid Method", 404


if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT)


