from flask_jwt import jwt_required, current_identity
from flask_restful import Resource, fields, marshal_with, reqparse, abort
from db import session
from models import TicketModel
from marshal_base_fields import ticket_fields

parser = reqparse.RequestParser()
parser.add_argument('first_name', type=str, help='First Name field is required.')
parser.add_argument('last_name', type=str, help='Last Name field is required.')
parser.add_argument('email', type=str, required=True, help='Email field is required.')
parser.add_argument('phone', type=str, required=True, help='Phone must be a string')
parser.add_argument('description', type=str, help='Description must be a string')
parser.add_argument('closed', type=bool, help="Closed must be a boolean")

class Ticket(Resource):
    @jwt_required()
    @marshal_with(ticket_fields)
    def get(self, id):
        ticket = session.query(TicketModel).filter(TicketModel.id == id).first()
        if ticket:
            return ticket
        else:
            abort(404, message="Ticket with the id " + str(id) + " doesn't exist.")
    
    @jwt_required()
    @marshal_with(ticket_fields)
    def put(self, id):
        args = parser.parse_args()
        ticket = session.query(TicketModel).filter(TicketModel.id == id).first()

        if not ticket: abort(404, message="Ticket with the id " + str(id) + " doesn't exist.")

        ticket.first_name = args['first_name']
        ticket.last_name = args['last_name']
        ticket.email = args['email']
        ticket.phone = args['phone']
        ticket.description = args['description']
        ticket.closed = args['closed']

        session.commit()

        return ticket
    
    @jwt_required()
    def delete(self, id):
        ticket = session.query(TicketModel).filter(TicketModel.id == id).first()

        if ticket:
            session.delete(ticket)
            session.commit()
            return {}, 204
        
        else:
            return abort(404, message="Ticket with the id " + str(id) + " doesn't exist.")


class TicketList(Resource):
    @jwt_required()
    @marshal_with(ticket_fields)
    def get(self):
        return session.query(TicketModel).all()

    @jwt_required()
    @marshal_with(ticket_fields)
    def post(self):
        print(parser)
        args = parser.parse_args()

        new_ticket = TicketModel(args['first_name'], args['last_name'], args['email'], args['phone'], args['description'], args['closed'])

        session.add(new_ticket)
        session.commit()
        return new_ticket
