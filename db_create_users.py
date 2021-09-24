# -*- coding: utf-8 -*-
from project import db
from project.models import User

#db.create_all()

#insert data
#db.session.add(User("lucas", "lmcarneiro@smcm.edu", "Krave9!i7"))

#commit the changes
db.session.commit()
