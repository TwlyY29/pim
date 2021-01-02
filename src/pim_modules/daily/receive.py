from pim_mailhelper.functions import parseSender, replyStatus, getMailTextAndCharset

import re
import dateparser
from datetime import timedelta, date

from . import OUTFILE
REMINDERTEMPLATE = 'REM %s%s MSG %s\n'

def calc_date_diff(thediff, date, before=True):
  days = 0
  weeks = 0
  years = 0
  for entry in thediff.lower().split(","):
    n = int(re.sub('[a-z]','',entry))
    if 'day' in entry:
      days = n
    elif 'week' in entry:
      weeks = n
    elif 'year' in entry:
      days += n * 365
  if before:
    delta = date - timedelta(days=days, weeks=weeks)
  else:
    delta = date + timedelta(days=days, weeks=weeks)
  return delta.strftime('%d %b %Y')

def is_date_ok(thedate):
  try:
    date_parsed = dateparser.parse(thedate)
    return date_parsed is not None
  except:
    return False

def receive(msg, isreply=False):
  sender = parseSender(msg['from'])
  try:
    thefile = open(OUTFILE, 'a', encoding='utf-8')
  except IOError as ioe:
    replyStatus(sender, 'error saving reminder: could not open '+OUTFILE+'\n'+ioe.getMessage())
  else:
    with thefile:
      text,charset = getMailTextAndCharset(msg)
      if text is not None and text != '':
        #text = quopri.decodestring(text).decode(charset).encode('utf-8')
        text = [t.strip() for t in text.strip().split('\n') if t != '']
        if len(text) % 2 == 0:
          # ~ repeat = int(len(text) / 2) * REMINDERTEMPLATE
          # ~ thefile.write(repeat % tuple(text))
          # ~ thefile.close()
          written = ''
          for i in range(0,int(len(text)/2)+1,2):
            offset = ''
            thedate = text[i]
            if '+' in thedate:
              s = thedate.split('+')
              thedate = s[0]
              offset = ' +'+s[1]
            txt = text[i+1]
            if 'before' in text[i] or 'after' in text[i]:
              if 'before' in text[i]:
                s = text[i].split('before')
                before=True
              elif 'after' in text[i]:
                s = text[i].split('after')
                before=False
              to_calc = s[0].strip()
              thedate = s[1].strip()
              if not is_date_ok(thedate):
                replyStatus(sender,'error handling reminder due to odd date spec \''+thedate+'\'')
                return False
              thedate = calc_date_diff(to_calc, dateparser.parse(thedate), before)
            else:
              if not is_date_ok(thedate):
                replyStatus(sender,'error handling reminder due to odd date spec \''+thedate+'\'')
                return False
            if '+' in thedate and '%' not in txt:
              txt = txt + ' %b'
            written += REMINDERTEMPLATE % (thedate, offset, txt)
          thefile.write(written)
          replyStatus(sender,'successfully written reminder:\n\n'+written)
          return True
        else:
          replyStatus(sender,'error writing reminder due to odd number of lines: \n'+str(len(text)))
          return False
  return False
