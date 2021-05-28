from flask import Flask
from database.db import initialize_db
from flask_restful import Api
from resources.routes import initialize_routes
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager






app = Flask(__name__)
#app.config['JWT_SECRET_KEY']={'t1NP63m4wnBg6nyHYKfmc2TpCOGI4nss'}
app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'

api = Api(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)






app.config['MONGODB_SETTINGS'] = {
    'host': 'mongodb://localhost/movie-bag'
}

initialize_db(app)
initialize_routes(api)


from functools import wraps

from flask import jsonify


def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt_claims()
        if claims['roles'] != 'admin':
            return jsonify(msg='Admins only!'), 403
        else:
            return fn(*args, **kwargs)
    return wrapper







app.run()