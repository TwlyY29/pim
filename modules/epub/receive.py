import sys

from datetime import date
from datetime import datetime
from email.utils import parsedate_tz, mktime_tz

from mailhelper.functions import parseSender, parseHeader, replyStatus, replyWithHtmlAndAttachment, getMailTextAndCharset

# uncomment if needed - if websiteasepub isn't located in any standard dir
#sys.path.append('/path/to/installation/of/twlyy29-websiteasepub')
import websiteasepub

def receive(msg, isreply=False):
  websiteasepub.init(_basepath="../../", #specify where epubs are written to. defaults to './' 
      #_dict="/var/mail/epubs/known_hosts.json", 
      _dict="known_hosts.json", #specify filename if you wish to save functioning css classes for URLs. file is created (if necessary) in _basepath
      _attstocompare=['class','id'], #where should CSS-IDs be taken from?
      _tagstoparse=['div','article','section','main']) #which HTML-elements should be considered?
  
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
