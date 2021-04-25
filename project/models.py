# -*- coding: utf-8 -*-

from project import db  # pragma: no cover
from project import bcrypt  # pragma: no cover
from sqlalchemy import ForeignKey  # pragma: no cover
#from sqlalchemy.orm import relationship  # pragma: no cover
from sqlalchemy_utils import ScalarListType



    
class Location(db.Model):
    
    __tablename__ = "locations"
    
    id = db.Column(db.String(255), primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    
    
    
    def __init__(self, id, name):
        self.id = id
        self.name = name
    
    def __repr__(self):
        return '<{}>'.format(self.name)
    
class User(db.Model):
    
    __tablename__ = "users"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    
    
    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')
        
    def is_authenticated(self):
        return True
    
    def is_active(self):
        return True
    
    def is_anonymous(self):
        return False
    
    def get_id(self):
        return self.id
    
    def __repr__(self):
        return '<name - {}>'.format(self.name)
    
class Schedule(db.Model):
    
    __tablename__ = "schedules"
    
    id = db.Column(db.Integer, primary_key=True)
    name_id = db.Column(db.Integer, ForeignKey('users.id'))
    today = db.Column(db.String(10), nullable=False)
    location = db.Column(db.String(20), nullable=True)
    all_times = db.Column(ScalarListType())
    date_look = db.Column(db.String(20), nullable=True)
    time_slot = db.Column(db.String(20), nullable=True)
    date_look_num = db.Column(db.Integer, nullable=True)
    time_slot_num = db.Column(db.Integer, nullable=True)
    reminder = db.Column(db.String(256), nullable=True)
    
    #schedules_name = relationship("User", foreign_keys="users.name")
    #schedules_loc = relationship("Schedule", foreign_keys="locations.name")
    
    def __init__(self, name_id, today, location, all_times, date_look,
                 time_slot, date_look_num, time_slot_num, reminder):
        self.name_id = name_id
        self.today = today
        self.location = location
        self.all_times = all_times
        self.date_look = date_look
        self.time_slot = time_slot
        self.date_look_num = date_look_num
        self.time_slot_num = time_slot_num
        self.reminder = reminder
        
    def __repr__(self):
        return '<{}>'.format([i for i in self.all_times])

# class Test(db.Model):
    
#     __tablename__ = "test"
    
#     id = db.Column(db.Integer, primary_key=True)
#     test = db.Column(db.String(256), nullable=True)
    
#     def __init__(self, test):
#         self.test = test