from smtplib import SMTP, SMTP_SSL
from smtplib import SMTPException
from mimetypes import guess_type
from os.path import basename
from email.utils import COMMASPACE
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.encoders import encode_base64


class EmailConnectionError(Exception):
    pass

class SendEmailError(Exception):
    pass

def get_email(email):
    if '<' in email:
        data = email.split('<')
        email = data[1].split('>')[0].strip()
    return email.strip()

class Email(object):
    def __init__(self, from_, to, subject, message, message_type='plain',
                 attachments=None, cc=None, bcc=None,
                 message_encoding='us-ascii', multi_to=False, multi_cc=False,
                 multi_bcc=False, multi_attach=False):
        self.email = MIMEMultipart()
        self.message = message
        self.email['From'] = from_
        if not multi_to:
            self.email['To'] = to
        else:
            self.email['To'] = COMMASPACE.join(to)
        self.email['Subject'] = subject
        if cc is not None:
            if not multi_cc:
                self.email['Cc'] = cc
            else:
                self.email['Cc'] = COMMASPACE.join(cc)
        if bcc is not None:
            if not multi_bcc:
                self.email['bcc'] = bcc
            else:
                self.email['bcc'] = COMMASPACE.join(bcc)
        text = MIMEText(message, message_type, message_encoding)
        self.email.attach(text)
        if attachments is not None:
            if multi_attach:
                for filename in attachments:
                    self.attach(filename)
            else:
                self.attach(attachments)

    def debug(self, mime=False):
        print 'From : ', self.email['From']
        print 'To : ', self.email['To']
        print 'Cc : ', self.email['Cc']
        print 'Bcc : ', self.email['bcc']
        print 'Subject : ', self.email['Subject']
        print 'Message :', self.message
        if mime:
            print self.email.as_string()

    def attach(self, filename):
        mimetype, encoding = guess_type(filename)
        if mimetype is None:
            mimetype = 'application/octet-stream'
        mimetype = mimetype.split('/', 1)
        fp = open(filename, 'rb')
        attachment = MIMEBase(mimetype[0], mimetype[1])
        attachment.set_payload(fp.read())
        fp.close()
        encode_base64(attachment)
        attachment.add_header('Content-Disposition', 'attachment',
                              filename=basename(filename))
        self.email.attach(attachment)

    def __str__(self):
        return self.email.as_string()

class EmailConnection(object):
    def __init__(self, server, username, password, debug=False):
        if ':' in server:
            data = server.split(':')
            self.server = data[0]
            self.port = int(data[1])
        else:
            self.server = server
            self.port = 25
        self.username = username
        self.password = password
        self.connect(debug)

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_val, trace):
        self.close()

    def connect(self, debug):
        self.connection = SMTP(host=self.server, port=self.port)
        if debug:  # Debug Information
            # self.debuglevel = 1
            self.connection.set_debuglevel(debug)
        # identify ourselves, prompting server for supported features
        self.connection.ehlo()
        # If we can encrypt this session, do it
        if self.connection.has_extn('STARTTLS'):
            self.connection.starttls()
            self.connection.ehlo()
        self.connection.esmtp_features['auth'] = 'PLAIN LOGIN'
        self.connection.login(self.username, self.password)

    def send(self, message, from_=None, to=None, verify=False):
        if type(message) == str:
            if from_ is None or to is None:
                raise EmailConnectionError('You need to specify `from_` '
                                           'and `to`')
            else:
                from_ = get_email(from_)
                to = get_email(to)
        else:
            from_ = message.email['From']
            if 'Cc' not in message.email:
                message.email['Cc'] = ''
            if 'bcc' not in message.email:
                message.email['bcc'] = ''
            to_emails = list(message.email['To'].split(',')) + \
                        message.email['Cc'].split(',') + \
                        message.email['bcc'].split(',')
            to = [get_email(complete_email) for complete_email in to_emails]
            message = str(message)
            if verify:
                for each_email in to_emails:
                    self.connection.verify(each_email)
                    # TODO option - remove emails that failed verification
        # return self.connection.sendmail(from_, to, message)
        try:
            self.connection.sendmail(from_, to, message)
        except SMTPException:
            raise SendEmailError('Message Could not be sent!')

    def close(self):
        self.connection.close()