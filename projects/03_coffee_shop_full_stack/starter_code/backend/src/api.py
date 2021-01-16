import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

"""
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
"""
# db_drop_and_create_all()

# ROUTES
"""
@TODO implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
"""


@app.route("/drinks", methods=["GET"])
def get_drinks():
    try:
        drinks = Drink.query.all()
        format_drinks = [drink.short() for drink in drinks]

        return jsonify({"success": True, "drinks": format_drinks})
    except Exception as e:
        print(e)
        abort(404)


"""
@TODO implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
"""


@app.route("/drinks-detail", methods=["GET"])
@requires_auth(permissions="get:drinks-detail")
def get_drinks_details(payload):
    try:
        drinks = Drink.query.all()
        print(drinks)
        format_drinks = [drink.long() for drink in drinks]
        return jsonify({"success": True, "drinks": format_drinks})
    except:
        abort(404)


"""
@TODO implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
"""


@app.route("/drinks", methods=["POST"])
@requires_auth(permissions="post:drinks")
def create_drink(payload):
    try:
        body = request.get_json()

        new_drink = body.get("title", None)
        if new_drink is None:
            abort(400)
        new_drink_recipe = body.get("recipe", None)
        new_drink_recipe = json.dumps(new_drink_recipe)

        drink = Drink(title=new_drink, recipe=new_drink_recipe)
        drink.insert()

        return jsonify(
            {
                "success": True,
                "drink": drink.long(),
            }
        )
    except:
        abort(422)


"""
@TODO implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
"""


@app.route("/drinks/<int:d_id>", methods=["PATCH"])
@requires_auth(permissions="patch:drinks")
def update_drink(payload, d_id):
    try:
        body = request.get_json()

        upt_drink = Drink.query.filter(Drink.id == d_id).one_or_none()
        if upt_drink is None:
            abort(404)
        if body.get("title", None) != None:
            upt_drink.title = body.get("title", None)
        if body.get("recipe", None) != None:
            upt_drink.recipe = json.dumps(body.get("recipe", None))

        upt_drink.update()

        return jsonify(
            {
                "success": True,
                "drink": upt_drink.long(),
            }
        )
    except Exception as e:
        print(e)
        abort(422)


"""
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
"""


@app.route("/drinks/<int:d_id>", methods=["DELETE"])
@requires_auth(permissions="delete:drinks")
def delete_drink(payload, d_id):
    try:
        del_drink = Drink.query.filter(Drink.id == d_id).one_or_none()
        if del_drink is None:
            abort(404)

        del_drink.delete()

        return jsonify(
            {
                "success": True,
                "drink": del_drink.id,
            }
        )
    except Exception as e:
        print(e)
        abort(422)


# Error Handling
"""
Example error handling for unprocessable entity
"""


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({"success": False, "error": 422, "message": "unprocessable"}), 422


"""
@TODO implement error handlers using the @app.errorhandler(error) decorator
    each error handler should return (with approprate messages):
             jsonify({
                    "success": False, 
                    "error": 404,
                    "message": "resource not found"
                    }), 404

"""


@app.errorhandler(404)
def not_found(error):
    return (
        jsonify({"success": False, "error": 404, "message": "resource not found"}),
        404,
    )


@app.errorhandler(400)
def not_found(error):
    return jsonify({"success": False, "error": 400, "message": "Bad request"}), 400


@app.errorhandler(401)
def unauthorized(error):
    return jsonify({"success": False, "error": 401, "message": "Un authorized"}), 401


"""
@TODO implement error handler for 404
    error handler should conform to general task above 
"""


"""
@TODO implement error handler for AuthError
    error handler should conform to general task above 
"""


@app.errorhandler(AuthError)
def auth_error(auth):
    return (
        jsonify({"success": False, "error": auth.status_code, "message": auth.error}),
        auth.status_code,
    )
