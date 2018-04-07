from db import session
from models import AdminModel
from flask_jwt import JWT, jwt_required, current_identity
from flask_restful import abort
from functools import wraps
from flask import request
import sys

# The authentication handler used by flask_JWT. Takes an email and password
def authenticate(email, password):
  #Query the database and return the ONE user that has the matching email/password. If user doesn't exist, return None
  user = session.query(AdminModel).filter(AdminModel.email == email).one_or_none()
  if (user and user.password == password):
    return user
  else:
    return None

# payload = JWT token sent by the user (as a header attribute)
# gets the ID stored within the token and returns the user object using the id to query the database
def identity(payload):
  user_id = payload['identity']
  return session.query(AdminModel).filter(AdminModel.id == user_id).one_or_none()