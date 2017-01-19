import os

from datetime import date
from datetime import datetime
from email.utils import parsedate_tz, mktime_tz
from string import Template
from subprocess import CalledProcessError, check_output

from mailhelper.functions import parseSender, replyStatus, getMailTextAndCharset

from . import OUTFILE

TEXT='''$customtitle

$reminders

'''
REMINDERLINE='* %s\n'
REMINDCMD = "/usr/bin/remind -ga -k\"echo %s\""

RMDTITLE='customtitle'
RMDLIST='reminders'
RMDCMD='cmd'

CMDS=[
{RMDTITLE:'Let yourself be reminded of some important stuff:', RMDCMD:"su mail -c \"/usr/bin/remind -ga -k\\\"echo %s\\\" {}\"".format(OUTFILE)},
#"{} {}".format(REMINDCMD,OUTFILE),
{RMDTITLE:'Today at Sports and Health:', RMDCMD:"wget -q -O- http://www.sports-and-health.de/events.ics | ./modules/daily/ical2rem.pl --lead-time 0 | {} -".format(REMINDCMD)}
]

def getreminders():
  output = ''
  for cmd in CMDS:
    try:
      #print("trying '{}'".format(cmd[RMDCMD]))
      reminder = check_output([cmd[RMDCMD]], shell=True)
      if reminder is None or "No reminders" in reminder: 
        continue
      else:
        reminder = reminder.strip().split('\n')
        reminders = ''
        for r in reminder:
          reminders += REMINDERLINE % r
        reminder = Template(TEXT).substitute({RMDTITLE:cmd[RMDTITLE],RMDLIST:reminders})
        output = "{}{}".format(output,reminder)
    except CalledProcessError as e:
      pass
  return output if output is not '' else False
  
