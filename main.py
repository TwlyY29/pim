#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os, sys, email, getpass
import email.generator

import modules

from mailhelper.functions import parseSender, parseHeader

EMERGENCY_ADDRESS='mirco.schoenfeld@phir.org'
ALLOWED_MAILADDRESSES=['mirco.schoenfeld@ifi.lmu.de','mirco.schoenfeld@digitalestadtmuenchen.de', 'mirco.schoenfeld@phir.org']

SUBJECT_FOR_REPLY='[reminder] Status'
FROM_FOR_REPLY='reminder@mircoschoenfeld.de'

BASEPATH = './'
SAVEMAIL = os.path.join(BASEPATH,'lastmail')
REPLYSIGNS=('re:','aw:')


def initLogger():
    import logging
    logger = logging.getLogger('receivereminder')
    hdlr = logging.FileHandler(os.path.join(BASEPATH,'pim.log'))
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr) 
    logger.setLevel(logging.INFO)
    return logger

logger = initLogger()


msg = email.message_from_file(sys.stdin)
accept = False

sender = parseSender(msg['from'])
if sender == 'unknown':
  logger.warn('could not parse sender from %s', msg['from'])
  sys.exit(1)

# accept message?
for recip in ALLOWED_MAILADDRESSES:
  if recip in sender:
    sender = recip
    accept = True
    break
if not accept: 
  if logger is not None: logger.info('declining mail from %s', sender)
  replyStatus(EMERGENCY_ADDRESS,'incoming reminder from unallowed mail: '+sender+'\n', subj = SUBJECT_FOR_REPLY, sender = FROM_FOR_REPLY)
  sys.exit(1)

logger.info('running as %s', getpass.getuser())
logger.info('accepting mail')

if SAVEMAIL != '':
  try:
   out = open(SAVEMAIL, 'w', encoding='utf-8')
  except IOError as ioe:
   pass
  else:
   with out:
     generator = email.generator.Generator(out)
     generator.flatten(msg)
     out.close()

subj = parseHeader(msg['Subject'])
logger.info('mail has subj '+subj)

isreply = any(subj.startswith(word) for word in REPLYSIGNS)
if not isreply:
  if modules.handle(subj,msg):
    logger.info("successfully handled mail")
    sys.exit(0)
elif isreply:
  if modules.handlereply(subj,msg):
    logger.info("successfully handled mail")
    sys.exit(0)
else:
  logThis = 'could not determine action. msg-subject was \''+msg['Subject']+'\' - parsed to \''+subj+'\')'
  logger.warn(logThis)
  replyStatus(sender, logThis, subj = SUBJECT_FOR_REPLY, sender = FROM_FOR_REPLY)
  sys.exit(1)
