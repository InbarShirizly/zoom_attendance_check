from server import auth, bcrypt, db
from flask_restful import Resource, reqparse, abort, HTTPException
from server.api import api, custom_types
from server.models.orm import get_user, TeacherModel
from server.config import RestErrors


class RegisterResource(Resource):
    def __init__(self):
        super().__init__()
        self._post_args = reqparse.RequestParser(bundle_errors=True)
        self._post_args.add_argument("username", type=custom_types.username, location='json', required=True)
        self._post_args.add_argument("email", type=custom_types.email, location='json', required=True)
        self._post_args.add_argument("password", type=custom_types.password, location='json', required=True)

    def post(self):
        args = self._post_args.parse_args()
        
        user = TeacherModel(
            username=args['username'],
            email=args['email'],
            password=args['password']
        )
        db.session.add(user)
        db.session.commit()
        return '', 204
        
         
api.add_resource(RegisterResource, "/register")