from flask import Response, request,abort
from database.models import Movie
from flask_restful import Resource
from flask_jwt_extended import jwt_required,current_user
from functools import wraps


def checkuser(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if current_user.isAdmin == 1:
            return func(*args, **kwargs)
        return abort(401)
    return wrapper

class MoviesApi(Resource):
    @jwt_required()
    @checkuser()
    def get(self):
        #movies = Movie.objects().to_json()
        movies={'name':'Jalva'}
        print(movies)
        return movies, 200

    @jwt_required()
    def post(self):
        body = request.get_json()
        movie = Movie(**body).save()
        id = movie.id
        return {'id': str(id)}, 200


class MovieApi(Resource):
    @jwt_required()
    def put(self, id):
        body = request.get_json()
        Movie.objects.get(id=id).update(**body)
        return '', 200

    @jwt_required()
    def delete(self, id):
        movie = Movie.objects.get(id=id).delete()
        return '', 200

    def get(self, id):
        movies = Movie.objects.get(id=id).to_json()
        return Response(movies, mimetype="application/json", status=200)


