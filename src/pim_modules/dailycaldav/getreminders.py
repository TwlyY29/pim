import configparser
from pathlib import Path

from datetime import datetime
from caldav.davclient import DAVClient
from collections import defaultdict
from subprocess import CalledProcessError, check_output

from . import CONF_FILE
today = datetime.now().date()

def read_config():
  CONFIG = {}
  config_object = configparser.ConfigParser()
  with open(CONF_FILE,"r") as file_object:
    config_object.read_file(file_object)
    CONFIG['defaults'] = {'skip_noduedate': (config_object['dailycaldav']).getboolean('skip_noduedate', True),
                           'get_overdue': (config_object['dailycaldav']).getboolean('get_overdue', True),
                           'get_futuredue': (config_object['dailycaldav']).getboolean('get_futuredue', True),
                           'get_withoutdue': (config_object['dailycaldav']).getboolean('get_withoutdue', False),
                           'get_all': (config_object['dailycaldav']).getboolean('get_all', False),
                           'futuredue_afterdate': (config_object['dailycaldav']).get('futuredue_afterdate', '+3'),
                           'futuredue_aftermsg': (config_object['dailycaldav']).get('futuredue_aftermsg', '(%v %b)'),
                           'withoutdue_afterdate': (config_object['dailycaldav']).get('withoutdue_afterdate', ''),
                           'withoutdue_aftermsg': (config_object['dailycaldav']).get('withoutdue_aftermsg', ''),
                           'show_priority': (config_object['dailycaldav']).getboolean('show_priority', True),
                           'show_priority_char': (config_object['dailycaldav']).get('show_priority_char', '!'),
                           'show_overdue': (config_object['dailycaldav']).getboolean('show_overdue', True),
                           'show_overdue_msg': (config_object['dailycaldav']).get('show_overdue_msg', '[overdue since DATE]'),
                          }
    CONFIG['resource'] = []
    for res in config_object['dailycaldav']['resources'].split():
      resconf = f'dailycaldav_{res}'
      if config_object.has_section(resconf):
        resource = {}
        resource['type'] = config_object[resconf].get('type','caldav')
        resource['url'] = config_object[resconf].get('url',False)
        resource['user'] = config_object[resconf].get('user',False)
        resource['passwd'] = config_object[resconf].get('passwd',False)
        todolists = config_object[resconf].get('todolists',False)
        tlists = []
        if todolists is not False:
          for t in todolists.split(' '):
            tobj = {'name':t}
            tconf = f'{resconf}_{t}'
            if config_object.has_section(tconf):
              for k,v in config_object.items(tconf):
                try_more = True
                try:
                  v = int(v)
                  try_more = False
                except:
                  pass
                if try_more:
                  try:
                    v = float(v)
                  except:
                    pass
                if try_more:
                  try:
                    v = v.lower() in ['true','yes','t','y']
                  except:
                    pass
                tobj[k] = v
            tlists.append(tobj)
        resource['todolists'] = tlists
        CONFIG['resource'].append(resource)
  return CONFIG

# taken from
# https://github.com/pydantic/pydantic/blob/fd2991fe6a73819b48c906e3c3274e8e47d0f761/pydantic/utils.py#L200
def deep_update(mapping, *updating_mappings):
    updated_mapping = mapping.copy()
    for updating_mapping in updating_mappings:
        for k, v in updating_mapping.items():
            if k in updated_mapping and isinstance(updated_mapping[k], dict) and isinstance(v, dict):
                updated_mapping[k] = deep_update(updated_mapping[k], v)
            else:
                updated_mapping[k] = v
    return updated_mapping

def get_calendar_config(config, cal, config_all):
  if config['type'] == 'caldav':
    for todolist in config['todolists']:
      if todolist['name'] == cal:
        todolist = deep_update(config_all['defaults'], todolist)
        return todolist
  elif config['type'] == 'ical':
    config = deep_update(config_all['defaults'], config)
    return config

def convert_to_remind(ical_comp, config):
  due=''
  descr=ical_comp['SUMMARY'] if 'SUMMARY' in ical_comp else ''
  if config['show_priority'] and ('PRIORITY' in ical_comp and ical_comp['PRIORITY'] > 0):
    # ~ print(ical_comp['PRIORITY'])
    char = config['show_priority_char']
    prio = f"{char* (10-ical_comp['PRIORITY'])} "
    descr = prio+descr
  after_date=''
  after_msg=''
  if 'DUE' in ical_comp:
    due = ical_comp['DUE'].dt
    if due < today:
      due = today
      if config['show_overdue']:
        msg = config['show_overdue_msg'].replace('$DATE',due.strftime('%d.%m.%y'))
        descr = f"{descr} {msg}"
    else:
      after_date = config['futuredue_afterdate']
      after_msg = config['futuredue_aftermsg']
  else:
    due = today
    after_date = config['withoutdue_afterdate']
    after_msg = config['withoutdue_aftermsg']
  return f"REM {due.strftime('%d %b %Y')} {after_date} MSG {descr} {after_msg}"

def remind(reminders):
  output = ''
  REMINDERLINE='* %s\n'
  try:
    reminders = '\n'.join(reminders)
    reminder = check_output([f"echo \"{reminders}\" | /usr/bin/remind -ga -"], shell=True)
    reminder = str(reminder, "utf-8")
    if reminder is not None and "No reminders" not in reminder: 
      reminder = reminder.strip().split('\n')
      output+='\n'.join([f"* {r}" for r in reminder[1:] if r])
  except CalledProcessError as e:
    pass
  return output if output != '' else False

def getreminders():
  output = ''
  config_all = read_config()
  
  overdue = defaultdict(list)
  duedate = defaultdict(list)
  sinedue = defaultdict(list)
  
  for config in config_all['resource']:
    if config['type'] == 'caldav':
      use_todolists = set()
      for c in config['todolists']:
        if not 'name' in c:
          raise Exception("resource>calendar needs 'name'!")
        use_todolists.add(c['name'])
      if len(use_todolists) == 0:
        continue
      
      
      with DAVClient(url=config['url'], 
                     username=config['user'] if 'user' in config else None, 
                     password=config['passwd'] if 'passwd' in config else None) as client:
        principal = client.principal()
        calendars = principal.calendars()
        
        for cal in calendars:
          if cal.name in use_todolists:
            
            if 'VTODO' in cal.get_supported_components():
              config_cal = get_calendar_config(config, cal.name, config_all)
              todos_fetched = cal.todos()
              for t in todos_fetched:
                due = t.get_due()
                if due is not None:
                  if due < today:
                    if config_cal['get_overdue'] or config_cal['get_all']:
                      overdue[cal.name].append(convert_to_remind(t.icalendar_component, config_cal))
                  else:
                    if config_cal['get_overdue'] or config_cal['get_all']:
                      duedate[cal.name].append(convert_to_remind(t.icalendar_component, config_cal))
                elif config_cal['get_withoutdue'] or config_cal['get_all']:
                  sinedue[cal.name].append(convert_to_remind(t.icalendar_component, config_cal))
  
  for cal in overdue:
    reminders = remind(overdue[cal])
    if reminders:
      output += f"Todos which are overdue in calendar '{cal}':\n{reminders}"
  for cal in duedate:
    reminders = remind(duedate[cal])
    if reminders:
      output += f"\n\nTodos which are due soon in calendar '{cal}':\n{reminders}"
  for cal in sinedue:
    reminders = remind(sinedue[cal])
    if reminders:
      output += f"\n\nTodos without a due date in calendar '{cal}':\n{reminders}"
        
  return output if output != '' else False

