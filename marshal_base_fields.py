from flask_restful import fields

user_fields = {
    'id': fields.Integer,
    'email': fields.String
}

lawyer_fields = {
    'id': fields.Integer,
    'first_name': fields.String,
    'last_name': fields.String,
    'email': fields.String,
    'phone': fields.String
}

ticket_fields = {
    'id': fields.Integer,
    'first_name': fields.String,
    'last_name': fields.String,
    'email': fields.String,
    'phone': fields.String,
    'description': fields.String,
    'closed': fields.Boolean
}