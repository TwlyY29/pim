import os
import sys
import configparser
import importlib

from datetime import date
from datetime import datetime
from email.utils import parsedate_tz, mktime_tz
from string import Template
from subprocess import CalledProcessError, check_output

from pim_mailhelper.functions import parseSender, replyStatus, getMailTextAndCharset

from . import OUTFILE, CONF_FILE, SUBMODS

TEXT='''$customtitle$reminders'''
REMINDERLINE='* %s\n'
REMINDCMD = "/usr/bin/remind -ga -k\"echo %s\""

RMDTITLE='customtitle'
RMDLIST='reminders'
RMDCMD='cmd'

RMDMOD='mod'
RMDSEC='sec'

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
  referrers = tuple(SUBMODS.keys())
  for sec in conf.sections():
    if sec.startswith('daily_') and sec != 'daily_attachments':
      if not sec.startswith(referrers):
        title = parse_title(conf[sec]['title'])
        command = parse_command(conf[sec]['command'])
        entries.append({RMDTITLE:title,RMDCMD:command})
      else:
        key = sec[0:sec.rfind('_')] if sec.count('_') > 1 else sec
        if SUBMODS[key]:
          entries.append({RMDMOD:key, RMDSEC:sec})
  return entries

def getreminders():
  output = ''
  config = configparser.ConfigParser()
  config.read(CONF_FILE)
  CMDS = parse_entries(config)
  appended_sys_path = False
  
  for cmd in CMDS:
    if RMDCMD in cmd:
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
          customtitle = "\n\n{}".format(cmd[RMDTITLE]) if cmd[RMDTITLE] != '' else ''
          reminder = Template(TEXT).substitute({RMDTITLE:customtitle,RMDLIST:reminders})
          output = "{}{}".format(output,reminder)
      except CalledProcessError as e:
        pass
    else:
      if not appended_sys_path:
        sys.path.append(__filepath)
        appended_sys_path = True
      themod = importlib.import_module(cmd[RMDMOD])
      check = themod.compile_output(cmd[RMDSEC], CONF_FILE)
      if check:
        customtitle, reminders = check
        customtitle = "\n\n{}\n".format(customtitle) if customtitle != '' else ''
        reminder = Template(TEXT).substitute({RMDTITLE:customtitle,RMDLIST:reminders})
        output = "{}{}".format(output,reminder)
        
  return output if output != '' else False
  
