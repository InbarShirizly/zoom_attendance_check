from server import auth, bcrypt, db
from flask_restful import Resource, reqparse, abort, HTTPException
from server.api import api, custom_types, login_token_serializer
from server.models.orm import TeacherModel
from server.models.utils import get_user
from server.config import RestErrors


class LoginResource(Resource):
    """
    Resource which is responsible for the login of a user to the application
    """
    def __init__(self):
        super().__init__()
        self._post_args = reqparse.RequestParser(bundle_errors=True)
        self._post_args.add_argument("auth", type=str, location='json', required=True) # Username or Email
        self._post_args.add_argument("password", type=str, location='json', required=True)

    def post(self):
        """
        The function will login a user to the application
        params are given from self._post_args as json in raw post data
        :param auth: username or email of the user (str)
        :param password: the password of the user (str)
        :return: token to authenticate as the logged user (json)
        """
        args = self._post_args.parse_args()
        user = get_user(args['auth'], args['password'])
        if not user:
            abort(400, message=RestErrors.INVALID_CREDENTIALS)
        return {'token':login_token_serializer.dumps(user.id)}


class RegisterResource(Resource):
    """
    Resource which is responsible for registering new user to the application
    """
    def __init__(self):
        super().__init__()
        self._post_args = reqparse.RequestParser(bundle_errors=True)
        self._post_args.add_argument("username", type=custom_types.username, location='json', required=True)
        self._post_args.add_argument("email", type=custom_types.email, location='json', required=True)
        self._post_args.add_argument("password", type=custom_types.password, location='json', required=True)

    def post(self):
        """
        The function will register new user to the application
        params are given from self._put_args as json in raw post data
        check server.api.validators class for full details about the types
        :param username: username of the new user (custom_types.username)
        :param email: email of the new user (custom_types.email)
        :param password: password of the new user (custom_types.password)
        :return: token to authenticate as the new user (json)
        """
        args = self._post_args.parse_args()
        user = TeacherModel(
            username=args['username'],
            email=args['email'],
            password=args['password']
        )
        db.session.add(user)
        db.session.commit()
        return {'token':login_token_serializer.dumps(user.id)}
        
        
api.add_resource(RegisterResource, "/register")
api.add_resource(LoginResource, "/login")