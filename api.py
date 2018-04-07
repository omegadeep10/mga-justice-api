from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from db import session
from datetime import timedelta

app = Flask(__name__, static_folder='static')
app.config['SECRET_KEY'] = 'tacos_320' # used for signing tokens
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://mga2j:justice23@mgajustice-db.cu92s72c9cow.us-east-1.rds.amazonaws.com/mga_justice?charset=utf8&use_unicode=0'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # we don't use track mods, this gets rid of an error in the console
app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=3600) # default to JWT expiration of one hour
app.config['JWT_AUTH_USERNAME_KEY'] = 'email' # we use email, not the default 'username' field that flask_JWT expects
app.config['ERROR_404_HELP'] = False

api = Api(app)
CORS(app)

@app.teardown_appcontext
def close_session(exception=None):
    session.remove()

#initialize flask_JWT
from flask_jwt import JWT, jwt_required, current_identity
from controllers.auth import authenticate, identity
jwt = JWT(app, authenticate, identity)

# NOTE: To obtain auth token, use the /auth endpoint, passing in a JSON object with email and password fields.
#       This endpoint is not shown here since it's automatically setup by flask_jwt.
from controllers.lawyer import Lawyer, LawyerList
from controllers.ticket import Ticket, TicketList
from controllers.send import SendTicket

# /lawyers => GET, POST
api.add_resource(LawyerList, '/lawyers')

# /lawyers/:id => GET, DELETE
api.add_resource(Lawyer, '/lawyers/<int:id>')

# /tickets => GET, POST
api.add_resource(TicketList, '/tickets')

# /tickets/:id => GET, PUT, DELETE
api.add_resource(Ticket, '/tickets/<int:id>')

# /send/:ticket_id/:lawyer_id => GET
api.add_resource(SendTicket, '/send/<string:ticket_id>/<string:lawyer_id>')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)