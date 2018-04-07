from flask_jwt import jwt_required, current_identity
from flask_restful import Resource, fields, marshal_with, reqparse, abort
from db import session
from models import LawyerModel
from marshal_base_fields import lawyer_fields

parser = reqparse.RequestParser()
parser.add_argument('first_name', type=str, required=True, help='First Name field is required.')
parser.add_argument('last_name', type=str, required=True, help='Last Name field is required.')
parser.add_argument('email', type=str, required=True, help='Email field is required.')
parser.add_argument('phone', type=str, help='Phone must be a string')

class Lawyer(Resource):
    @jwt_required()
    @marshal_with(lawyer_fields)
    def get(self, id):
        lawyer = session.query(LawyerModel).filter(LawyerModel.id == id).first()
        if lawyer:
            return lawyer
        else:
            abort(404, message="Lawyer with the id " + str(id) + " doesn't exist.")
    
    @jwt_required()
    def delete(self, id):
        l = session.query(LawyerModel).filter(LawyerModel.id == id).first()

        if l:
            session.delete(l)
            session.commit()
            return {}, 204
        
        else:
            return abort(404, message="Lawyer with the id " + str(id) + " doesn't exist.")


class LawyerList(Resource):
    @jwt_required()
    @marshal_with(lawyer_fields)
    def get(self):
        return session.query(LawyerModel).all()

    @jwt_required()
    @marshal_with(lawyer_fields)
    def post(self):
        print(parser)
        args = parser.parse_args()
        lawyer = session.query(LawyerModel).filter(LawyerModel.email == args['email']).first()

        new_lawyer = LawyerModel(args['first_name'], args['last_name'], args['email'], args['phone'])

        if not lawyer:
            session.add(new_lawyer)
            session.commit()
            return new_lawyer
        else:
            abort(404, message="Lawyer with email " + args['email'] + " already exists.")
