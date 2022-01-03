from __future__ import print_function

import os.path
import configparser
from . import CONF_FILE

def parse_entries(conf):
  entries = []
  if conf.has_section('daily_attachments'):
    entries.extend(conf['daily_attachments']['files'].split())
  return entries

def getattachments():
  config = configparser.ConfigParser()
  config.read(CONF_FILE)
  attchmnts = [_f for _f in parse_entries(config) if os.path.isfile(_f)]
  return attchmnts if len(attchmnts) > 0 else False
  
if __name__ == '__main__':
  print(getattachments())
