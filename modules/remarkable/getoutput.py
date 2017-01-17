import os

from datetime import date
from datetime import datetime
from email.utils import parsedate_tz, mktime_tz
from string import Template
from subprocess import CalledProcessError, check_output

from . import OUTFILE
from mailhelper.functions import parseSender, replyStatus, getMailTextAndCharset

TEXT='''Some shit you find noteworthy:

$remarkable
'''

def getoutput():
  if os.path.isfile(OUTFILE):
    cmd = "cat {}".format(OUTFILE)
    try:
      text = check_output([cmd], shell=True)
      return Template(TEXT).substitute({'remarkable':text})
    except CalledProcessError as e:
      pass
  return False
