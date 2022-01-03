from pim_mailhelper.functions import parseSender, replyStatus, getMailTextAndCharset

from . import CONF_FILE, CONF_SEC
import os.path
import configparser
from datetime import datetime,timedelta
import dateparser

SEP='\t'
DB_HEADER = "date\tpm\tamount\twhat\tcategory"
HELP = """Expecting:

database
date (t, y, or YYYY-MM-DD)
amount (+ for income. otherwise assume expense)
description (short)
category
"""

def init_db(filename):
  with open(filename, 'w') as _f:
    print(DB_HEADER, file=_f)
    
def string_to_date(thestr):
  if thestr == 't':
    d = datetime.now()
    return datetime(d.year, d.month, d.day)
  elif thestr == 'y':
    d = datetime.now() - timedelta(days=1)
    return datetime(d.year, d.month, d.day)
  else:
    try:
      date_parsed = dateparser.parse(thestr)
      if date_parsed is not None:
        return datetime(date_parsed.year, date_parsed.month, date_parsed.day)
    except:
      pass
  return False

def string_to_amount(thestr):
  am = False
  if thestr.count(','):
    thestr = thestr.replace(',','.')
  if thestr.count(' '):
    thestr = thestr.replace(' ','')
  try:
    am = float(thestr)
  except ValueError:
    pass
  if am < 0:
    am *= -1
  return am

def string_to_pm(thestr):
  if thestr.startswith('+'):
    return '+'
  else:
    return '-'


def get_db(dbfile, datepat):
  db = []
  with open(dbfile, 'r') as _database:
    header = _database.readline()
    header = header.strip().split(SEP)
    ind_date = header.index('date')
    ind_plusminus = header.index('pm')
    ind_amount = header.index('amount')
    ind_what = header.index('what')
    ind_category = header.index('category')
    
    for line in _database:
      line = line.strip().split(SEP)
      db.append({'date': datetime.strptime(line[ind_date], datepat),
                 'pm' : line[ind_plusminus],
                 'amount' : line[ind_amount],
                 'what' : line[ind_what],
                 'category' : line[ind_category] if len(line) > ind_category else ''})
  return db

def receive(msg, isreply=False):
  config = configparser.ConfigParser()
  config.read(CONF_FILE)

  DATEPATT = config[CONF_SEC]['date_pattern']
  databases = config[CONF_SEC]['databases']
  databases = databases.split(',') if databases.count(',') else [databases]
  
  sender = parseSender(msg['from'])
  text,charset = getMailTextAndCharset(msg)
  if text is not None and text != '':
  
    text = [t.strip() for t in text.strip().split('\n') if t != '']
    
    out_db = text[0]
    if out_db.count(','):
      out_db = out_db.split(',')
      for entry in out_db:
        entry = entry.strip()
        if entry not in databases:
          replyStatus(sender, f"could not find database for '{entry}'.\n\n" + HELP)
          return False
    else:
      if out_db not in databases:
        replyStatus(sender, f"could not find database for '{out_db}'.\n\n" + HELP)
        return False
      out_db = [out_db]
    
    exp_date = string_to_date(text[1])
    if not exp_date:
      replyStatus(sender, f"could not parse any date for '{text[1]}'.\n\n" + HELP)
      return False
    
    exp_amount = string_to_amount(text[2])
    if not exp_amount:
      replyStatus(sender, f"could not parse amount for '{text[2]}'.\n\n" + HELP)
      return False
    
    exp_pm = string_to_pm(text[2])
    
    exp_what = text[3]
    exp_cat = text[4] if len(text) > 4 else ''
    
    success = False
    
    for db in out_db:
      db_key = f"database_{db}"
      if db_key in config[CONF_SEC]:
        db_file = config[CONF_SEC][db_key]
        db_items = []
        if not os.path.isfile(db_file):
          init_db(db_file)
        else:
          db_items = get_db(db_file, DATEPATT)
        
        db_items.append({'date': exp_date,
                   'pm' : exp_pm,
                   'amount' : exp_amount,
                   'what' : exp_what,
                   'category' : exp_cat})
        if len(db_items) > 1:
          db_items = sorted(db_items,key=lambda d: d['date'],reverse=False)
        with open(db_file, 'w') as _db:
          print(DB_HEADER, file=_db)
          for entry in db_items:
            print(f"{datetime.strftime(entry['date'],DATEPATT)}\t{entry['pm']}\t{entry['amount']}\t{entry['what']}\t{entry['category']}", file=_db)
        
        replyStatus(sender,f"Successfully written entry to database '{db}'.\n\nEntry:\nDate: {datetime.strftime(entry['date'],DATEPATT)}\nAmount: {entry['amount']}\nPlusMinus: {entry['pm']}\nDescr: {entry['what']}\nCategory: {entry['category']}")
        success = True
      else:
        replyStatus(sender, f"could not find database file for '{db}'/'{db_key}'.")
    return success
  return False
    
if __name__ == '__main__':
  receive("""fun
t
19,30
schwimmbad
familie""")
  receive("""fun
y
+22,10
pizza
familie""")
  receive("""fun
today
-1,37
bier
saufen""")
  receive("""taxes
today
-500,37
rechner
hardware""")
  receive("""fun
yesterday
- 14,37
dings
saufen""")
  receive("""fun,taxes
yesterday
- 114,37
irgendwas. vergessen""")
  # ~ receive("""fun
# ~ 20.12.2021
# ~ 18,37
# ~ dings
# ~ geschenke""")
