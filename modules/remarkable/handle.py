from datetime import date
from datetime import datetime
from email.utils import parsedate_tz, mktime_tz

from mailhelper.functions import parseSender, replyStatus, getMailTextAndCharset

OUTFILE = '../../reminders-remarkable'

def handle(msg, isreply=False):
  sender = parseSender(msg['from'])
  try:
    thefile = open(OUTFILE, 'r+', encoding='utf-8')
  except IOError as ioe:
    replyStatus(sender, 'error saving remarkable: could not open '+OUTFILE+'\n'+ioe.getMessage())
  else:
    date = None
    date_tuple = parsedate_tz(msg['Date'])
    if date_tuple:
      date = datetime.fromtimestamp(mktime_tz(date_tuple))
    if date:
      content = thefile.read()
      thefile.seek(0)
      thefile.write(date.strftime("%A, %d.%m.%y, %H:%M:\n"))
      text,charset = getMailTextAndCharset(msg)
      if not isinstance(text,str):
        text = text.decode(charset) 
      #text = quopri.decodestring(text).decode(charset).encode('utf-8')
      for line in text.splitlines():
        thefile.write("\t{}\n".format(line))
      thefile.write("\t---\n\n{}".format(content))
      replyStatus(sender,'successfully written remarkable reminder\n')
      return True
    else:
      replyStatus(sender,'could not parse date from msg\n')
  return False
