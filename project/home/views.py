# -*- coding: utf-8 -*-
#################
#### imports ####
#################

from project import db, app#, scheduler  # pragma: no cover
from project.models import Schedule#, Location, User  # pragma: no cover
from project.home.forms import LocationForm, ScheduleForm  # pragma: no cover
from flask import render_template, Blueprint, request,\
    url_for, flash, redirect  # pragma: no cover
from flask_login import login_required, current_user # pragma: no cover
from datetime import datetime, date
import requests
from bs4 import BeautifulSoup
import re
import json
from scraper import scraper
import pytz
from threading import Thread

################
#### config ####
################

home_blueprint = Blueprint(
    'home', __name__,
    template_folder='templates'
)  # pragma: no cover

################
#### routes ####
################


ET_URL = 'https://app.rockgympro.com/b/widget/?'

HEADERS_G = {'User-Agent': 'Mozilla/5.0',
           'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
           'X-Requested-With': 'XMLHttpRequest' }

LOC_GUIDS = {
        'cb':['Columbia', '7adb2741626a47a58f11ee624dc48397'],
        'cc':['Crystal City', '2923df3b2bfd4c3bb16b14795c569270'],
        'hd':['Hampden', '503c88b01d36493790767d49703a01c0'],
        'rv':['Rockville', '07d503eb2ba04792a095a56cb5fe1c8e'],
        'tm':['Timonium', '65529b9f9ddb4282924cf2a782c436d9']}

tz = pytz.timezone('America/New_York')
now = datetime.now(tz)
TODAY = date(now.year, now.month, now.day)

@home_blueprint.route('/', methods=["GET", "POST"])
@login_required
def home():
    error = None
    user = current_user
    user_scheds = Schedule.query.filter_by(name_id=user.id)
    sched = user_scheds.order_by(Schedule.id.desc()).first()
    status = sched.reminder
    if status == 'waiting':
        return redirect(url_for('home.scrape'))
    
    form = LocationForm(request.form)

    if form.validate_on_submit():
        look_for = form.day.data
        loc = form.location.data
        if loc == 'hd' and look_for.weekday() in [5, 6]:
            error = "Hampden is closed on the weekends. Please pick a new date."
            return render_template('index.html', form=form, error=error)
        
        time_delta = look_for - TODAY
        time_delta = time_delta.days
        if time_delta < 0:
            error = ("Invalid date. Please make sure you picked today or a "
                "later date.")
            return render_template('index.html', form=form, error=error)
        #GET request to earth treks to get the locations times
        params_g = {'a':'offering',
              'offering_guid':LOC_GUIDS[loc],
              'random':'60536721b6263',
              'iframeid':'',
              'mode':'p'
            }
        sess = requests.Session()
        res_get = sess.get(ET_URL, headers=HEADERS_G, params=params_g)
        get_soup = BeautifulSoup(res_get.content, features='lxml')
        script = get_soup.find_all('script')
        var_dates = script[-1].contents[0]
        if str(look_for) not in var_dates:
            error = ("Sorry! Looks like this date doesn't have any available "
                "time slots left. Please try another date.")
            return render_template('index.html', form=form, error=error)
        
        times = re.findall('"%s.*?}' %look_for, var_dates)[0]
        times_dict = json.loads(times[13:])
        times = [i[11:] for i in times_dict['specific_datetimes']]
        #Update the current schedule session
        sched = Schedule.query.order_by(Schedule.id.desc()).first()
        sched.location = LOC_GUIDS[form.location.data][0]
        sched.date_look_num = time_delta
        sched.date_look = look_for
        sched.all_times = times
        db.session.commit()
        return redirect(url_for('home.schedule'))

    return render_template('index.html', form=form, error=error)
    
@home_blueprint.route('/schedule', methods=["GET", "POST"])
@login_required
def schedule():
    error = None
    sched = Schedule.query.order_by(Schedule.id.desc()).first()
    times = sched.all_times
    form = ScheduleForm(request.form)
    form.time_slot.choices = []
    for i, time in enumerate(times):
        form.time_slot.choices += [(i, time)]
    
    if form.validate_on_submit():
        sched = Schedule.query.order_by(Schedule.id.desc()).first()
        sched.time_slot_num = form.time_slot.data
        date = sched.date_look
        slot = sched.all_times[int(form.time_slot.data)]
        sched.time_slot = slot
        sched.reminder = 'waiting'
        location = sched.location
        db.session.commit()
        flash((
            "Thanks! " +
            "Scheduler is now looking for spots on {0} at {1} at the {2} " +
            "location.").format(date, slot, location)
            )

        return redirect(url_for('home.scrape'))
    else:
        return render_template('schedule.html', form=form, error=error)
    
@home_blueprint.route('/scraper')
@login_required
def scrape():
    error = None
    run_func()
    return render_template('scraper.html', error=error)

def run_func():
    thr = Thread(target=run_async_func, args=[app], daemon=True)
    thr.start()
    return thr

def run_async_func(app):
    with app.app_context():
        result = scraper()
        return result

@home_blueprint.route('/cancel')
@login_required
def cancel():
    error = None
    sched = Schedule.query.order_by(Schedule.id.desc()).first()
    sched.reminder = 'cancel'
    db.session.commit()
    return render_template('cancel.html', error=error)
