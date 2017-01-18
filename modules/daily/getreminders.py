import os

from datetime import date
from datetime import datetime
from email.utils import parsedate_tz, mktime_tz
from string import Template
from subprocess import CalledProcessError, check_output

from mailhelper.functions import parseSender, replyStatus, getMailTextAndCharset

from . import OUTFILE

TEXT='''Let yourself be reminded of some important stuff:

$reminders
'''
REMINDERLINE='* %s\n'

REMINDCMD = "/usr/bin/remind -ga -k\"echo %s\""
CMDS=[
#"su mail -c \"{}\" {}\"".format(REMINDCMD,OUTFILE),
"{} {}".format(REMINDCMD,OUTFILE),
#"wget -q -O- http://www.google.com/calendar/ical/8saefumocvgmlnep6jjescdsd8%40group.calendar.google.com/public/basic.ics | /home/mirco/coding/twlyy29-pim/modules/daily/ical2rem.pl --lead-time 1 | {} -".format(REMINDCMD)
]

def getreminders():
  reminders = ''
  for cmd in CMDS:
    try:
      print("trying '{}'".format(cmd))
      reminder = check_output([cmd], shell=True)
      if reminder is None or "No reminders" in reminder: 
        return False
      else:
        reminder = reminder.strip().split('\n')
        for r in reminder:
          reminders += REMINDERLINE % r
    except CalledProcessError as e:
      pass
  if reminders is not '':
    return Template(TEXT).substitute({'reminders':reminders})
  return False
  
