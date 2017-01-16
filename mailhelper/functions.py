from email.header import Header, decode_header, make_header
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import re
from subprocess import Popen, PIPE

from .MIMEUTF8QPText import MIMEUTF8QPText

def getMailTextAndCharset(msg):
  for part in msg.walk():
    if part.get_content_type() == 'text/plain':
      text = part.get_payload(decode=True)
      charset = part.get_content_charset()
      if not isinstance(text,str):
        text = text.decode(charset) 
      return (text, charset)


def getMessage(line):
    found = re.search('(?<=\*\s)\w+', line)
    i = found.start(0) if found is not None else -1
    if i != -1:
        return line[i:]


def parseHeader(toParse):
  return str(make_header(decode_header(toParse))).strip().lower()


def parseSender(toParse):
  sender = re.search('<(.*)>', toParse) if toParse is not None and toParse != '' else None
  sender = sender.group(1) if sender is not None else 'unknown'
  return sender.lower()


def replyStatus(to, status, subj = 'no subject', sender = 'noreply@nodomain.com'):
    mail = MIMEUTF8QPText(status + '\n')
    mail['Subject'] = Header(subj).encode()
    mail['From'] = sender
    mail['To'] = to
    p = Popen(["/usr/sbin/sendmail", "-t", "-oi"], stdin=PIPE)
    p.communicate(str.encode(mail.as_string()))


def replyWithHtmlAndAttachment(to, htmlfile, attchdfile, subj = 'no subject', sender = 'noreply@nodomain.com'):
    mail = MIMEMultipart()
    mail['Subject'] = Header(subj).encode()
    mail['From'] = sender
    mail['To'] = to
    
    fp_attch = open(attchdfile,"rb")
    part = MIMEApplication(fp_attch.read())
    fp_attch.close()
    part.add_header('Content-Disposition', 'attachment', filename=os.path.basename(attchdfile).decode("utf-8") )
    mail.attach(part)
    
    fp_html = open(htmlfile,'r', encoding='utf-8')
    mail.attach(MIMEText(fp_html.read(), 'html')) 
    fp_html.close()
    
    p = Popen(["/usr/sbin/sendmail", "-t", "-oi"], stdin=PIPE)
    p.communicate(str.encode(mail.as_string()))
