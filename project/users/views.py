# -*- coding: utf-8 -*-
#################
#### imports ####
#################

from flask import flash, redirect, render_template, request, \
    url_for, Blueprint  # pragma: no cover
from flask_login import login_user, login_required, logout_user  # pragma: no cover
from project.users.forms import LoginForm  # pragma: no cover
from project.models import User, Schedule, bcrypt  # pragma: no cover
from project import db
from datetime import datetime, date
import pytz

################
#### config ####
################

users_blueprint = Blueprint(
    'users', __name__,
    template_folder='templates'
)  # pragma: no cover

################
#### routes ####
################

tz = pytz.timezone('America/New_York')
now = datetime.now(tz)
today = date(now.year, now.month, now.day)

# route for handling the login page logic
@users_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    form = LoginForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter_by(name=request.form['username']).first()
            if user is not None and bcrypt.check_password_hash(
                    user.password, request.form['password']):
                login_user(user)
                today_date = str(date.today())
                user_sched = Schedule(name_id=user.id,
                                      today=today_date,
                                      location=None,
                                      all_times=None,
                                      date_look=None,
                                      time_slot=None,
                                      date_look_num=None,
                                      time_slot_num=None,
                                      reminder=None)
                db.session.add(user_sched)
                db.session.commit()
                flash('You were logged in.')
                return redirect(url_for('home.home'))
            else:
                error = 'Invalid username or password.'
    return render_template('login.html', form=form, error=error)


@users_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You were logged out.')
    return redirect(url_for('users.login'))
