import email.charset 
from email.mime.text import MIMEText
from email.mime.nonmultipart import MIMENonMultipart
from email.mime.multipart import MIMEMultipart

#taken from http://stackoverflow.com/questions/14939018/encode-mimetext-as-quoted-printables
class MIMEUTF8QPText(email.mime.nonmultipart.MIMENonMultipart):
  def __init__(self, payload):
    MIMENonMultipart.__init__(self, 'text', 'plain',charset='utf-8')
    utf8qp=email.charset.Charset('utf-8')
    utf8qp.body_encoding=email.charset.QP
    self.set_payload(payload, charset=utf8qp) 
    
