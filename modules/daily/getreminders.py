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

__filepath = os.path.dirname(os.path.realpath(__file__))

CMDS=[
#{RMDTITLE:'Let yourself be reminded of some important stuff:', RMDCMD:"su mail -c \"/usr/bin/remind -ga -k\\\"echo %s\\\" {}\"".format(OUTFILE)},
{RMDTITLE:'Let yourself be reminded of some important stuff:', RMDCMD:"{} {}".format(REMINDCMD,OUTFILE)},
{RMDTITLE:'Today is a holiday:', RMDCMD:"wget -q -0- https://www.mozilla.org/media/caldata/GermanHolidays.ics | {}/ical2rem.pl --lead-time 0 | {} -".format(__filepath,REMINDCMD)}

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
  
