import sys

from datetime import date
from datetime import datetime
from email.utils import parsedate_tz, mktime_tz

from mailhelper.functions import parseSender, parseHeader, replyStatus, replyWithHtmlAndAttachment, getMailTextAndCharset

sys.path.append('/home/mirco/coding/twlyy29-websiteasepub')
import websiteasepub

def handle(msg, isreply=False):
  websiteasepub.init(#_basepath="/var/mail/epubs/", 
      #_dict="/var/mail/epubs/known_hosts.json",
      _dict="./known_hosts.json",
      _attstocompare=['class','id'],
      _tagstoparse=['div','article','section','main'])
  
  sender = parseSender(msg['from'])
  text,charset = getMailTextAndCharset(msg)
  title = None
  classes = None
  savecss = False
  needcss = False
  subj = parseHeader(msg['Subject'])
  if not isreply:
    needcss, title, classes = websiteasepub.fetchMetaFrom(text)
    if needcss:
      replyStatus(sender,classes, "{}: {}".format(subj,title))
      return True
  else:
    title = subj[subj.find("epub:") + 6 :]
    classes = text
    savecss = True
  
  if title is not None and classes is not None:
    success, epubfile, htmlfile = websiteasepub.makeEpub(title, classes, savecssclass=savecss)
    if success:
      subj = ("Re: {} - {}".format(subj,title) if not isreply and not needcss else "Re: {}".format(subj))
      replyWithHtmlAndAttachment(sender, htmlfile, epubfile, subj)
      return True
  replyStatus(sender,"an error occured during creation of epub for title\n\t{}\nmaybe could not find corresponding classes?\n\t{}\n".format(title, classes))
  return False
