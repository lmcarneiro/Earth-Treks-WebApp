# -*- coding: utf-8 -*-
from project import db
from project.models import User

db.create_all()

#insert data
#db.session.add(User("lucas", "lmcarneiro@smcm.edu", "Krave9!i7"))
#db.session.add(User("evelina", "Ev.cebotari@gmail.com", "MyLumps7*"))
db.session.add(User("kat", "katherine.e.lamb@gmail.com", "Borbluv<3"))

#commit the changes
db.session.commit()