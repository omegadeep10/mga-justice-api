from flask_jwt import jwt_required, current_identity
from flask_restful import Resource, fields, marshal_with, reqparse, abort
from db import session
from models import TicketModel, LawyerModel
from marshal_base_fields import ticket_fields
from mail_it import send_mail

parser = reqparse.RequestParser()
parser.add_argument('first_name', type=str, help='First Name field is required.')
parser.add_argument('last_name', type=str, help='Last Name field is required.')
parser.add_argument('email', type=str, required=True, help='Email field is required.')
parser.add_argument('phone', type=str, required=True, help='Phone must be a string')
parser.add_argument('description', type=str, help='Description must be a string')
parser.add_argument('closed', type=bool, help="Closed must be a boolean")

class SendTicket(Resource):
    @jwt_required()
    def get(self, ticket_id, lawyer_id):
        ticket = session.query(TicketModel).filter(TicketModel.id == ticket_id).first()
        lawyer = session.query(LawyerModel).filter(LawyerModel.id == lawyer_id).first()

        if not ticket or not lawyer:
            abort(404, message="Ticket or lawyer do not exist.")

        ticket.closed = True
        
        subject = '[TICKET] You have a new MGA Justice help request from ' + ticket.first_name + " " + ticket.last_name
        body = f"""Hello {lawyer.first_name + " " + lawyer.last_name},

        You have a new MGA Justice help request.

        name: {ticket.first_name + " " + ticket.last_name}
        email: {ticket.email}
        phone: {ticket.phone}
        description: {ticket.description}

        Have a nice day.
        """
        
        # Broken due to mailgun disabled domain :( - reenable when it's working
        send_mail('mgajustice@deeppatel.me', [lawyer.email], subject, body)
        session.commit()

        return {}, 204