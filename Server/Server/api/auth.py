from Server import auth, bcrypt, db
from flask_restful import Resource, reqparse, abort
from Server.api import api
from Server.models import get_user, TeacherModel


register_argparse = reqparse.RequestParser()
register_argparse.add_argument("username", type=str, help="Username is required", required=True)
register_argparse.add_argument("email", type=str, help="Email is required", required=True)
register_argparse.add_argument("password", type=str, help="Password is required", required=True)

class RegisterResource(Resource):
    def post(self):
        args = register_argparse.parse_args()
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
        return '', 200
        
         
api.add_resource(RegisterResource, "/register")