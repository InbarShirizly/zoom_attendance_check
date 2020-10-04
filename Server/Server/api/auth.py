from Server import auth, bcrypt, db
from flask_restful import Resource, reqparse, abort
from Server.api import api
from Server.models import get_user, TeacherModel


class RegisterResource(Resource):
    def __init__(self):
        super().__init__()
        self._post_args = reqparse.RequestParser()
        self._post_args.add_argument("username", type=str, help="Username is required", location='json', required=True)
        self._post_args.add_argument("email", type=str, help="Email is required", location='json', required=True)
        self._post_args.add_argument("password", type=str, help="Password is required", location='json', required=True)

    def post(self):
        args = self._post_args.parse_args()
        if TeacherModel.query.filter_by(username=args['username']).first():
            return abort(400, message="Username already taken")
        if TeacherModel.query.filter_by(email=args['email']).first():
            return abort(400, message="Email already taken")
        
        user = TeacherModel(
            username=args['username'],
            email=args['email'],
            password=bcrypt.generate_password_hash(args['password'])
        )
        db.session.add(user)
        db.session.commit()
        return '', 204
        
         
api.add_resource(RegisterResource, "/register")