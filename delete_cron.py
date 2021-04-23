#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 25 11:11:04 2021

@author: lucas
"""

from crontab import CronTab
import os

def delete_cron():
    
    cron = CronTab(user='lucas')
    job = next(cron.find_comment('Earth Treks'))
    cron.remove(job)
    cron.write()
    os.remove('/home/lucas/Documents/Social/Earth_Treks/start.txt')
    os.remove('/home/lucas/Documents/Social/Earth_Treks/date.txt')
    print('Cron job was deleted.')