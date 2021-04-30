#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime, date
import re
from bs4 import BeautifulSoup
import requests
from reminder import reminder
from project import db
from project.models import Schedule, User
import pytz
from time import sleep


ET_URL = 'https://app.rockgympro.com/b/widget/?'


HEADERS = {
    'User-Agent':'Mozilla/5.0',
    'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
    'X-Requested-With': 'XMLHttpRequest' }

GUIDS = {
        'Columbia':'7adb2741626a47a58f11ee624dc48397',
        'Crystal City':'2923df3b2bfd4c3bb16b14795c569270',
        'Hampden':'503c88b01d36493790767d49703a01c0',
        'Rockville':'07d503eb2ba04792a095a56cb5fe1c8e',
        'Timodium':'65529b9f9ddb4282924cf2a782c436d9'}

PARAMS = {'a':'equery'}

def kaffeine_req(on):
    
    kaf_sess = requests.Session()
    kaf_get = kaf_sess.get('https://kaffeine.herokuapp.com/')
    kaf_soup = BeautifulSoup(kaf_get.text, 'lxml')
    csrf = kaf_soup.select_one('meta[name="csrf-token"]')['content']
    
    kaf_cookies = requests.utils.cookiejar_from_dict(
        requests.utils.dict_from_cookiejar(kaf_sess.cookies)
        )
    
    kaf_header = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.5',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Content-Length': '41',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'DNT': '1',
        'Host': 'kaffeine.herokuapp.com',
        'Origin': 'https://kaffeine.herokuapp.com',
        'Pragma': 'no-cache',
        'Referer': 'https://kaffeine.herokuapp.com/',
        'User-Agent': ('Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:87.0)'
                       'Gecko/20100101 Firefox/87.0'),
        'X-Requested-With': 'XMLHttpRequest',
        'X-CSRF-Token': csrf}
    
    if on is True:

        kaf_pos = kaf_sess.post('https://kaffeine.herokuapp.com/register',
                                data={'name':'earth-treks',
                                      'nap':'true', 
                                      'bedtime':'23:00'
                                      },
                                headers=kaf_header,
                                cookies=kaf_cookies
                                )
        
    
    if on is False:
        
        kaf_pos = kaf_sess.post('https://kaffeine.herokuapp.com/decaf',
                                data={'name':'earth-treks',
                                      '_method':'delete'
                                      },
                                headers=kaf_header,
                                cookies=kaf_cookies
                                )

    return kaf_pos

def scraper():

    tz = pytz.timezone('America/New_York')
    now = datetime.now(tz)
    today = date(now.year, now.month, now.day)
    sched = Schedule.query.order_by(Schedule.id.desc()).first()
    result = sched.reminder
    remind = sched.reminder
    
    kaf_pos = kaffeine_req(on=True)
    
    print('Kaffeine turned on status: %d' %kaf_pos.status_code)
    print('Kaffeine turned on contents:\n%s' %kaf_pos.content)
    
    while result == 'waiting' or remind != 'cancel':
        users = User.query.order_by(User.id)
        receiver = users.filter_by(id=sched.name_id)[0].email
        started_on = sched.today
        look_for = sched.date_look
        loc = sched.location
        time_slot = sched.time_slot
        date_diff = date.fromisoformat(look_for) - today
        date_diff = date_diff.days
        remind = sched.reminder
        if remind == 'cancel':
            return remind
        if result != 'waiting':
            return result
        
        session = requests.Session()
        
        DATA = {
        	"PreventChromeAutocomplete": "",
        	"random": "60537a225b5d3",
        	"iframeid": "",
        	"mode": "p",
        	"fctrl_1": "offering_guid",
        	"offering_guid": GUIDS[loc],
        	"fctrl_2": "course_guid",
        	"course_guid": "",
        	"fctrl_3": "limited_to_course_guid_for_offering_guid_%s" %GUIDS[loc],
        	"limited_to_course_guid_for_offering_guid_%s" %GUIDS[loc]: "",
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

        
        res_pos = session.post(ET_URL, 
                               headers=HEADERS,
                               params=PARAMS, 
                               data=DATA)
        
        available_json = res_pos.json()
        available_soup = BeautifulSoup(available_json['event_list_html'],
                                       features='lxml'
                                       )
        times = available_soup.find_all('td',
                                        attrs={
                                            'class':'offering-page-schedule-'
                                            'list-time-column'
                                            }
                                        )
        times = [time.text.strip('\n') for time in times]
        slots = available_soup.find_all(string=re.compile('space'))
        slots = [slot.strip('\n') for slot in slots]
        time_slots = dict(zip(times, slots))
        
        slot_v = []
        try:
            hour = int(time_slot[:2])
            mins = time_slot[3:5]
            if hour > 12:
                hour -= 12
                if mins != '00':
                    time_slot = '%d:%s PM' %(hour, mins)
                else:
                    time_slot = '%d PM' %hour
            else:
                if time_slot[3:5] != '00':
                    time_slot = '%d:%s AM' %(hour, mins)
                else:
                    time_slot = '%d AM' %hour
            for _ in time_slots.keys():
                if time_slot in _:
                    slot_t = _
            for _ in time_slots.values():
                slot_v = time_slots[slot_t]
        except:
            times = None
            pass
        if 'space' in slot_v:
            num_slots = int(slot_v.split(' space')[0])
            slot_t = slot_t.replace('to  ', 'to ')
            if num_slots == 1:
                message = (
                    'Subject: Your Sign-Up Reminder\n\nThere is 1 spot '
                    'available at {0} on {1}.'
                    '\n\nThis message was sent from Python.').format(loc,
                                                                     slot_t)
            elif num_slots > 1:
                message = (
                    'Subject: Your Sign-Up Reminder\n\nThere are {0} spots '
                    'available at {1} on {2}.'
                    '\n\nThis message was sent from Python.').format(num_slots,
                                                                     loc,
                                                                     slot_t)
            if message != {}:
                print(message)
                
            params = {'loc':loc,
                      'slots':num_slots,
                      'time':slot_t}
            
            reminder([receiver], params)
            result = 'sent'
            sched.reminder = 'sent'
            db.session.commit()
            kaf_pos = kaffeine_req(on=False)
            print('Kaffeine turned off status: %d' %kaf_pos.status_code)
            print('Kaffeine turned off contents:\n%s' %kaf_pos.content)
            return result
        else:
            print('This job was started on %s. Today is %s.' %(started_on, 
                                                               str(today)
                                                               )
                  )
            if date_diff < 0 or times is None:
                slot_t = time_slot
                print('No spots opened up for you, crontab will stop looking.')
                params = {'loc':loc,
                          'slots':0,
                          'time':slot_t}
                reminder([receiver], params)
                result = 'stopped'
                sched.reminder = 'stopped'
                db.session.commit()
                kaf_pos = kaffeine_req(on=False)
                print('Kaffeine turned off status: %d' %kaf_pos.status_code)
                print('Kaffeine turned off contents:\n%s' %kaf_pos.content)
                return result
            else:
                print('Crontab is running this script every minute until a '
                      'spot opens up.')
                result = 'waiting'
                sched.reminder = 'waiting'
                db.session.commit()
                return result
        
        
        sleep(30)
        
    return result