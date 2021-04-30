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
from scraper import scraper, kaffeine_req
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

def run_check():
    user = current_user
    user_scheds = Schedule.query.filter_by(name_id=user.id)
    sched = user_scheds.order_by(Schedule.id.desc()).first()
    if sched is not None:
        status = sched.reminder
        if status == 'waiting':
            return redirect(url_for('home.scrape'))

@home_blueprint.route('/', methods=["GET", "POST"])
@login_required
def home():
    error = None
    run_check()
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
        if res_get.status_code == 200:
            pass
        else:
            error = (
                'Looks like something went wrong with Earth Treks.'
                'Please check their website.'
                "If Earth Treks looks ok, it's our bad. Please contact admin."
                )
            return render_template('index.html', form=form, error=error)
        get_soup = BeautifulSoup(res_get.content, features='lxml')
        script = get_soup.find_all('script')
        var_dates = script[-1].contents[0]
        if str(look_for) not in var_dates:
            error = ("Sorry! Looks like this date doesn't have any available "
                "time slots left. Please try another date.")
            return render_template('index.html', form=form, error=error)
        else:
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
    run_check()
    sched = Schedule.query.order_by(Schedule.id.desc()).first()
    times = sched.all_times
    form = ScheduleForm(request.form)
    form.time_slot.choices = []
    if times is None:
        return redirect(url_for('home.home'))
    for i, time in enumerate(times):
        form.time_slot.choices += [(i, time)]
    
    if form.validate_on_submit():
        sched = Schedule.query.order_by(Schedule.id.desc()).first()
        sched.time_slot_num = form.time_slot.data
        slot = sched.all_times[int(form.time_slot.data)]
        sched.time_slot = slot
        sched.reminder = 'waiting'
        db.session.commit()

        return redirect(url_for('home.scrape'))
    else:
        return render_template('schedule.html', form=form, error=error)
    
@home_blueprint.route('/running')
@login_required
def scrape():
    error = None
    sched = Schedule.query.order_by(Schedule.id.desc()).first()
    if sched.reminder != 'waiting':
        return redirect(url_for('home.home'))
    date = datetime.fromisoformat(sched.date_look)
    date = date.strftime('%m/%d/%y')
    time = sched.time_slot
    hour = int(time[:2])
    if hour > 12:
        hour -= 12
        time = '%d:%s PM' %(hour, time[3:5])
    else:
        time = '%d:%s AM' %(hour, time[3:5])
    data = {'loc':sched.location,
            'date':date,
            'time':time}
    if data['loc'] is None:
        error = 'Something went wrong. Try logging out and starting a new job.'
        return render_template('running.html', data=data, error=error)
    run_func()
    return render_template('running.html', data=data, error=error)

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
    status = sched.reminder
    if status == 'waiting':
        sched.reminder = 'cancel'
        kaf_pos = kaffeine_req(on=False)
        print('Kaffeine turned off status: %d' %kaf_pos.status_code)
        print('Kaffeine turned off contents:\n%s' %kaf_pos.content)
        db.session.commit()
    else:
        flash('You tried to cancel an already completed job.'
              'No jobs currently running.')
        return redirect(url_for('home.home'))
        
    return render_template('cancel.html', error=error)
