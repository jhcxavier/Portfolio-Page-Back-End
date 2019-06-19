"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from models import db, User, Product, About

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)

@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

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
            lastname=body['firstname'],
            email=body['email'],
            password=body['password'],
            dobDate=body['dobDate'],
            imageURL=body['imageURL'],
            resumeStyle=body['resumeStyle'],
            theme=body['theme'],
            title=body['title'])

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


@app.route('/about/<int:product_id>', methods=['PUT', 'GET', 'DELETE'])
def get_single_about(about_id):
    """
    Single user
    """

    # PUT request
    if request.method == 'PUT':
        body = request.get_json()
        if body is None:
            raise APIException("You need to specify the request body as a json object", status_code=400)

        about1 = Product.query.get(about_id)
        if about1 is None:
            raise APIException('User not found', status_code=404)

        if "description" in body:
            about1.description = body["description"]
        if "date" in body:
            about1.date = body["date"]
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

if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT)


