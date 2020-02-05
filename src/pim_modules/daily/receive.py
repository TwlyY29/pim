from pim_mailhelper.functions import parseSender, replyStatus, getMailTextAndCharset

import re
import dateparser
from datetime import timedelta, date

from . import OUTFILE
REMINDERTEMPLATE = 'REM %s MSG %s\n'

def calc_date_diff(before, date):
  days = 0
  weeks = 0
  years = 0
  for entry in before.lower().split(","):
    n = int(re.sub('[a-z]','',entry))
    if 'day' in entry:
      days = n
    elif 'week' in entry:
      weeks = n
    elif 'year' in entry:
      days += n * 365
  delta = date - timedelta(days=days, weeks=weeks)
  return delta.strftime('%d %b %Y')


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
          for i in range(0,int(len(text)/2),2):
            thedate = text[i]
            if 'before' in text[i]:
              s = text[i].split('before')
              before = s[0].strip()
              thedate = s[1].strip()
              offset = ''
              if '+' in thedate:
                s = thedate.split('+')
                thedate = s[0]
                offset = ' +'+s[1]
              thedate = calc_date_diff(before, dateparser.parse(thedate))+offset
            written += REMINDERTEMPLATE % (thedate, text[i+1]) + '\n'
          thefile.write(written)
          replyStatus(sender,'successfully written reminder:\n\n'+written)
          return True
        else:
          replyStatus(sender,'error writing reminder due to odd number of lines: \n'+str(len(text)))
          thefile.close()
  return False
