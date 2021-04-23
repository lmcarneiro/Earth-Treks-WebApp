# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import SelectField
#from wtforms_sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField
#from wtforms.validators import DataRequired, InputRequired
from wtforms.fields.html5 import DateField

ET_URL = 'https://app.rockgympro.com/b/widget/?'

headers_g = {'User-Agent': 'Mozilla/5.0',
           'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
           'X-Requested-With': 'XMLHttpRequest' }

loc_guids = {
        'cb':'7adb2741626a47a58f11ee624dc48397',
        'cc':'2923df3b2bfd4c3bb16b14795c569270',
        'hd':'503c88b01d36493790767d49703a01c0',
        'rv':'07d503eb2ba04792a095a56cb5fe1c8e',
        'tm':'65529b9f9ddb4282924cf2a782c436d9'}

class LocationForm(FlaskForm):
    location = SelectField(
        'Location', choices=[
                            ('cb', 'Columbia'),
                            ('cc', 'Crystal City'),
                            ('hd', 'Hampden'),
                            ('rv', 'Rockville'),
                            ('tm', 'Timonium')
                    ]
        )
    day = DateField('DatePicker', format='%Y-%m-%d')
    
    
# def get_times():
#     sched = Schedule.query.order_by(Schedule.id.desc()).first()
#     return sched

class ScheduleForm(FlaskForm):

    time_slot = SelectField(
        'Time', choices=[])
    
    # time_slot = QuerySelectField(
    #     'Time', validators=[InputRequired(u'Please select a time')],
    #     query_factory=get_times, get_label='all_times')
    