from sqlalchemy import Column, Integer, String, Date, ForeignKey, Table, Boolean
from sqlalchemy import select, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import relationship, backref, column_property
from sqlalchemy.ext.hybrid import hybrid_property
import sys
from db import session

Base = declarative_base()

class AdminModel(Base):
  __tablename__ = 'admin'

  id = Column(Integer, primary_key=True)
  email = Column(String(255), nullable=False, unique=True)
  password = Column(String, nullable=False)

  def __str__(self):
    return "Admin object: (email='%s')" % self.email

  def __init__(self, email, password):
    self.email = email
    self.password = password


class LawyerModel(Base):
  __tablename__ = 'lawyer'

  id = Column(Integer, primary_key=True)
  first_name = Column(String(255), nullable=False)
  last_name = Column(String(255), nullable=False)
  email = Column(String(255), nullable=False)
  phone = Column(String(255))

  def __str__(self):
    return "Lawyer object: (course='%s')" % self.email

  def __init__(self, first_name, last_name, email, phone):
    self.first_name = first_name
    self.last_name = last_name
    self.email = email
    self.phone = phone

class TicketModel(Base):
  __tablename__ = 'ticket'

  id = Column(Integer, primary_key=True)
  first_name = Column(String(255))
  last_name = Column(String(255))
  email = Column(String(255), nullable=False)
  phone = Column(String(255), nullable=False)
  description = Column(String)
  closed = Column(Boolean, default=False)

  def __str__(self):
    return "Ticket object: (course='%s')" % self.id
  
  def __init__(self, first_name, last_name, email, phone, description, closed=False):
    self.first_name = first_name
    self.last_name = last_name
    self.email = email
    self.phone = phone
    self.description = description
    self.closed = closed