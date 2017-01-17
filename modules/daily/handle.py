from mailhelper.functions import parseSender, replyStatus, getMailTextAndCharset

OUTFILE = '../../reminders-daily'
REMINDERTEMPLATE = 'REM %s MSG %s\n'

def handle(msg, isreply=False):
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
        text = text.strip().split('\n')
        if len(text) % 2 == 0:
          repeat = int(len(text) / 2) * REMINDERTEMPLATE
          thefile.write(repeat % tuple(text))
          replyStatus(sender,'successfully written reminder:\n\n'+repeat % tuple(text))
          thefile.close()
          return True
        else:
          replyStatus(sender,'error writing reminder due to odd number of lines: \n'+str(len(text)))
          thefile.close()
  return False
