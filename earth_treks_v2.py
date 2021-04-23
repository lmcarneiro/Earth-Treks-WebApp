#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Must be called in terminal as 'earth_treks.py [receivers] [date_choice] [time]'
"""

import requests
from datetime import date, timedelta, datetime
from bs4 import BeautifulSoup
import re
from reminder import reminder, reminder2, check_response
from crontab import CronTab
import sys
import os
from delete_cron import delete_cron

args = sys.argv
args = args[1:]
receiver = []

today = date.today()

try:
    with open('/home/lucas/Documents/Social/Earth_Treks/start.txt', 'r') as f:
        first_day = f.read()
    if first_day == '':
        os.remove('/home/lucas/Documents/Social/Earth_Treks/start.txt')

except FileNotFoundError:
    with open('/home/lucas/Documents/Social/Earth_Treks/start.txt', 'w') as f:
        f.write(str(today))
    print('This job is being set on %s' %today)
    first_day = today


if '[' in args[0]:
    if len(args) == 4:
        args.pop(0)
        args.pop(0)
        args.insert(0, '[l,e]')
        
    receiver = ['lmcarneiro@smcm.edu', 'Ev.cebotari@gmail.com']

elif args[0] == 'l':
    receiver.append('lmcarneiro@smcm.edu')
    
elif args[0] == 'e':
    receiver.append('Ev.cebotari@gmail.com')

date_choice = int(args[1])
time = int(args[2])

try:
    with open('/home/lucas/Documents/Social/Earth_Treks/date.txt', 'r') as f:
        show_date = f.read()
    if show_date == '':
        os.remove('/home/lucas/Documents/Social/Earth_Treks/date.txt')
except FileNotFoundError:
    show_date = str(today + timedelta(days=date_choice))
    with open('/home/lucas/Documents/Social/Earth_Treks/date.txt', 'w') as f:
        f.write(show_date)
        
date_choice = datetime.strptime(show_date, '%Y-%m-%d').date() - today
date_choice = date_choice.days
        
print('Looking for spots on %s.' %show_date)
print()

command = ('/home/lucas/anaconda3/bin/python '
           '/home/lucas/Documents/Social/Earth_Treks/'
           'earth_treks.py %s %d %d > /tmp/EarthTreks.log 2>&1' %(args[0],
                                                                  date_choice,
                                                                  time))

cron = CronTab(user='lucas')
try:
    job = next(cron.find_comment('Earth Treks'))
except:    
    job = cron.new(command=command, comment='Earth Treks')
    job.minute.every(1)
    cron.write()
            
ET_URL = 'https://app.rockgympro.com/b/widget/?'

headers_g = {'User-Agent': 'Mozilla/5.0',
           'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
           'X-Requested-With': 'XMLHttpRequest' }

headers_p = {'User-Agent': 'Mozilla/5.0',
           'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
           'X-Requested-With': 'XMLHttpRequest' }

params_g = {'a':'offering',
          'offering_guid':'2923df3b2bfd4c3bb16b14795c569270',
          'random':'60536721b6263',
          'iframeid':'',
          'mode':'p'}

params_p = {'a':'equery'}

session = requests.Session()

data = {
	"PreventChromeAutocomplete": "",
	"random": "60537a225b5d3",
	"iframeid": "",
	"mode": "p",
	"fctrl_1": "offering_guid",
	"offering_guid": "2923df3b2bfd4c3bb16b14795c569270",
	"fctrl_2": "course_guid",
	"course_guid": "",
	"fctrl_3": "limited_to_course_guid_for_offering_guid_2923df3b2bfd4c3bb16b14795c569270",
	"limited_to_course_guid_for_offering_guid_2923df3b2bfd4c3bb16b14795c569270": "",
	"fctrl_4": "show_date",
	"show_date": show_date,
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

res_get = session.get(ET_URL, headers=headers_g, params=params_g)
cookies = requests.utils.cookiejar_from_dict(requests.utils.dict_from_cookiejar(session.cookies))
res_pos = session.post(ET_URL, headers=headers_p, params=params_p, data=data,
                       cookies=cookies)

content_g = res_get.content

available_json = res_pos.json()

available_soup = BeautifulSoup(available_json['event_list_html'], features='lxml')
times = available_soup.find_all('td', attrs={'class':'offering-page-schedule-list-time-column'})
times = [time.text.strip('\n') for time in times]
slots = available_soup.find_all(string=re.compile('space'))
no_slot = available_soup.find_all(string=re.compile('full'))
slots = [slot.strip('\n') for slot in slots]
time_slots = dict(zip(times, slots))

slot_v = []
if len(time_slots.keys()) > 0:
    slot_t = list(time_slots.keys())[time]
if len(time_slots.values()) > 0:
    slot_v = list(time_slots.values())[time]

if 'space' in slot_v:
    num_slots = int(slot_v.split(' space')[0])
    if num_slots == 1:
        slots = slot_t
    elif num_slots > 1:
        slots = (num_slots, slot_t)
        
    reminder2(receiver, slots)
    if slot_v != {}:
        print('The number of slots available on %s is: %d.' %(slot_t, num_slots))
    delete_cron()
        
else:
    print('This job was started on %s. Today is %s.' %(first_day, str(today)))
    if date_choice < 0:
        delete_cron()
        print('No spots opened up for you, crontab will stop looking.')
    else:            
        print('Crontab is running this script every minute until a spot opens up.')