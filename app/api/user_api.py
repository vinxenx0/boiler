from flask import Blueprint, request
from flask_restful import Resource, Api
from app.models.user import User
from app.models.database import db

api_bp = Blueprint('api', __name__)
api = Api(api_bp)

class UserAPI(Resource):
    def get(self, user_id):
        user = User.query.get(user_id)
        if not user:
            return {"message": "User not found"}, 404
        return {"id": user.id, "username": user.username, "email": user.email}, 200

    def delete(self, user_id):
        user = User.query.get(user_id)
        if not user:
            return {"message": "User not found"}, 404
        db.session.delete(user)
        db.session.commit()
        return {"message": "User deleted"}, 200

api.add_resource(UserAPI, '/user/<int:user_id>')
