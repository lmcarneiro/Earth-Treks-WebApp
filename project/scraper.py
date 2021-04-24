#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime, date
import re
from bs4 import BeautifulSoup
import requests
from reminder import reminder
from project import scheduler, db
from project.models import Schedule, User
import pytz


def scraper():
    tz = pytz.timezone('America/New_York')
    now = datetime.now(tz)
    today = date(now.year, now.month, now.day)
    sched = Schedule.query.order_by(Schedule.id.desc()).first()
    jobs = scheduler.get_jobs()
    jobs = str(jobs)
    sched.test = jobs
    db.session.commit()
    users = User.query.order_by(User.id)
    receiver = users.filter_by(id=sched.name_id)[0].email
    started_on = sched.today
    look_for = sched.date_look
    loc = sched.location
    time_slot = sched.time_slot_num
    date_diff = date.fromisoformat(look_for) - today
    date_diff = date_diff.days
    
    ET_URL = 'https://app.rockgympro.com/b/widget/?'
    

    headers_p = {'User-Agent': 'Mozilla/5.0',
               'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
               'X-Requested-With': 'XMLHttpRequest' }
    
    loc_guids = {
            'Columbia':'7adb2741626a47a58f11ee624dc48397',
            'Crystal City':'2923df3b2bfd4c3bb16b14795c569270',
            'Hampden':'503c88b01d36493790767d49703a01c0',
            'Rockville':'07d503eb2ba04792a095a56cb5fe1c8e',
            'Timodium':'65529b9f9ddb4282924cf2a782c436d9'}
    
    params_p = {'a':'equery'}
    
    
    session = requests.Session()
    data = {
    	"PreventChromeAutocomplete": "",
    	"random": "60537a225b5d3",
    	"iframeid": "",
    	"mode": "p",
    	"fctrl_1": "offering_guid",
    	"offering_guid": loc_guids[loc],
    	"fctrl_2": "course_guid",
    	"course_guid": "",
    	"fctrl_3": "limited_to_course_guid_for_offering_guid_%s" %loc_guids[loc],
    	"limited_to_course_guid_for_offering_guid_%s" %loc_guids[loc]: "",
    	"fctrl_4": "show_date",
    	"show_date": look_for,
    	"ftagname_0_pcount-pid-1-316074": "pcount",
    	"ftagval_0_pcount-pid-1-316074": "1",
    	"ftagname_1_pcount-pid-1-316074": "pid",
    	"ftagval_1_pcount-pid-1-316074": "316074",
    	"fctrl_5": "pcount-pid-1-316074",
    	"pcount-pid-1-316074": "0",
    	"ftagname_0_pcount-pid-1-6420306": "pcount",
    	"ftagval_0_pcount-pid-1-6420306": "1",
    	"ftagname_1_pcount-pid-1-6420306": "pid",
    	"ftagval_1_pcount-pid-1-6420306": "6420306",
    	"fctrl_6": "pcount-pid-1-6420306",
    	"pcount-pid-1-6420306": "0",
    	"ftagname_0_pcount-pid-1-6304903": "pcount",
    	"ftagval_0_pcount-pid-1-6304903": "1",
    	"ftagname_1_pcount-pid-1-6304903": "pid",
    	"ftagval_1_pcount-pid-1-6304903": "6304903",
    	"fctrl_7": "pcount-pid-1-6304903",
    	"pcount-pid-1-6304903": "0",
    	"ftagname_0_pcount-pid-1-6304904": "pcount",
    	"ftagval_0_pcount-pid-1-6304904": "1",
    	"ftagname_1_pcount-pid-1-6304904": "pid",
    	"ftagval_1_pcount-pid-1-6304904": "6304904",
    	"fctrl_8": "pcount-pid-1-6304904",
    	"pcount-pid-1-6304904": "0",
    	"ftagname_0_pcount-pid-1-6570973": "pcount",
    	"ftagval_0_pcount-pid-1-6570973": "1",
    	"ftagname_1_pcount-pid-1-6570973": "pid",
    	"ftagval_1_pcount-pid-1-6570973": "6570973",
    	"fctrl_9": "pcount-pid-1-6570973",
    	"pcount-pid-1-6570973": "0",
    	"ftagname_0_pcount-pid-1-6570974": "pcount",
    	"ftagval_0_pcount-pid-1-6570974": "1",
    	"ftagname_1_pcount-pid-1-6570974": "pid",
    	"ftagval_1_pcount-pid-1-6570974": "6570974",
    	"fctrl_10": "pcount-pid-1-6570974",
    	"pcount-pid-1-6570974": "0"
    }

    res_pos = session.post(ET_URL, headers=headers_p, params=params_p, data=data)
    
    available_json = res_pos.json()
    available_soup = BeautifulSoup(available_json['event_list_html'], features='lxml')
    times = available_soup.find_all('td',
                                    attrs={
                                        'class':'offering-page-schedule-list-time-column'
                                        }
                                    )
    times = [time.text.strip('\n') for time in times]
    slots = available_soup.find_all(string=re.compile('space'))
    slots = [slot.strip('\n') for slot in slots]
    time_slots = dict(zip(times, slots))
    
    
    slot_v = []
    if len(time_slots.keys()) > 0:
        slot_t = list(time_slots.keys())[time_slot]
    if len(time_slots.values()) > 0:
        slot_v = list(time_slots.values())[time_slot]
        
    
    if 'space' in slot_v:
        num_slots = int(slot_v.split(' space')[0])
        slot_t = slot_t.replace('to  ', 'to ')
        if num_slots == 1:
            message = ('Subject: Your Sign-Up Reminder\n\nThere is 1 spot available'
                       ' on {}.'
                       '\n\nThis message was sent from Python.').format(slot_t)
        elif num_slots > 1:
            message = ('Subject: Your Sign-Up Reminder\n\nThere are {0} spots'
                      ' available on {1}.'
                      '\n\nThis message was sent from Python.').format(num_slots, slot_t)
        if message != {}:
            print(message)

        reminder([receiver], message)
        scheduler.remove_job(id='scraper')
        
    else:
        print('This job was started on %s. Today is %s.' %(started_on, str(today)))
        if date_diff < 0:
            scheduler.remove_job(id='scraper')
            message = ('Subject: Your Sign-Up Reminder\n\n'
                       'Sorry! It looks like no spots opened up for you.\nIf you'
                       'would like to try a new date please click here.')
            print('No spots opened up for you, crontab will stop looking.')
        else:
            print('Crontab is running this script every minute until a spot opens up.')
            