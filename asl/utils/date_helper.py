# -*- coding: utf-8 -*-
'''
Created on 10.7.2013

@author: Martin Babka
'''
from datetime import date, timedelta

def format_datetime_portable(ts):
    return '{0.year:{1}}-{0.month:{1}}-{0.day:{1}}T{0.hour:{1}}:{0.minute:{1}}:{0.second:{1}}'.format(ts, '02')

def format_date_portable(ts):
    return '{0.year:{1}}-{0.month:{1}}-{0.day:{1}}'.format(ts, '02')

def format_datetime_relative(dt):

    today = date.today()
    yesterday = today - timedelta(days=1)

    if dt.strftime('%Y-%m-%d') == today.strftime('%Y-%m-%d'):
        text = u'Dnes ' + dt.strftime('%H:%M')
    elif dt.strftime('%Y-%m-%d') == yesterday.strftime('%Y-%m-%d'):
        text = u'Včera ' + dt.strftime('%H:%M')
    else:
        text = dt.strftime(u'%d.%m.%Y %H:%M')

    return text

def format_date_relative(d):

    today = date.today()
    yesterday = today - timedelta(days=1)

    if d.strftime('%Y-%m-%d') == today.strftime('%Y-%m-%d'):
        text = u'Dnes'
    elif d.strftime('%Y-%m-%d') == yesterday.strftime('%Y-%m-%d'):
        text = u'Včera'
    else:
        text = d.strftime(u'%d.%m.%Y')

    return text
