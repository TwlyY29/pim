import os

from datetime import date
from datetime import datetime
from email.utils import parsedate_tz, mktime_tz
from string import Template
from subprocess import CalledProcessError, check_output

from pim_mailhelper.functions import parseSender, replyStatus, getMailTextAndCharset
import configparser

from . import OUTFILE, CONF_FILE

TEXT='''$customtitle$reminders'''
REMINDERLINE='* %s\n'
REMINDCMD = "/usr/bin/remind -ga -k\"echo %s\""

RMDTITLE='customtitle'
RMDLIST='reminders'
RMDCMD='cmd'

__filepath = os.path.dirname(os.path.realpath(__file__))

def parse_title(title):
  return title+'\n\n'

def parse_command(cmd):
  cmd = cmd.replace('#ical2rem.pl#',__filepath+'/ical2rem.pl')
  cmd = cmd.replace('#REMINDPIPE#',REMINDCMD+' -')
  cmd = cmd.replace('#REMINDFROMFILE#',REMINDCMD)
  return cmd
  
def parse_entries(conf):
  entries = []
  for sec in conf.sections():
    if sec.startswith('daily_') and sec != 'daily_statusreport':
      title = parse_title(conf[sec]['title'])
      command = parse_command(conf[sec]['command'])
      entries.append({RMDTITLE:title,RMDCMD:command})
  return entries

def getreminders():
  output = ''
  config = configparser.ConfigParser()
  config.read(CONF_FILE)
  CMDS = parse_entries(config)
  
  for cmd in CMDS:
    try:
      reminder = check_output([cmd[RMDCMD]], shell=True)
      reminder = str(reminder, "utf-8")
      if reminder is None or "No reminders" in reminder: 
        continue
      else:
        reminder = reminder.strip().split('\n')
        reminders = ''
        for r in reminder:
          reminders += REMINDERLINE % r
        customtitle = "\n\n{}".format(cmd[RMDTITLE]) if cmd[RMDTITLE] is not '' else ''
        reminder = Template(TEXT).substitute({RMDTITLE:customtitle,RMDLIST:reminders})
        output = "{}{}".format(output,reminder)
    except CalledProcessError as e:
      pass
  return output if output is not '' else False
  
