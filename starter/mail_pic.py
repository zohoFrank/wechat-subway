import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.text import MIMEText


class MailSender(object):
    """
    Attributes:
        _from_address (str): Sender's mail address
        _to_address (list[str]): Receivers' mail addresses
        __password (str): Password of sender's email

        _smtp (str): Sender's mail SMTP server address and port
        _message (MIMEMultipart): MIME message
        _subject (str): Title of the mail, usually default
        _text (str): Raw text of mail context
        _image (list[str]): Paths of all pictures
        _debug (bool): Debug level
    """

    def __init__(self, sender='', receivers=None, password=''):
        if receivers is None:
            receivers = []
        self._from_address = sender
        self._to_address = receivers
        self.__password = password

        self._smtp = ''
        self._message = MIMEMultipart()
        self._subject = 'Just an email'
        self._text = ''
        self._image = []
        self._debug = False

    # getter and setter #
    @property
    def sender(self):
        return self._from_address

    @sender.setter
    def sender(self, email):
        self._from_address = email
        self._set_msg()

    @property
    def receivers(self):
        return self._to_address

    @receivers.setter
    def receivers(self, rec_list):
        """
        Args:
            rec_list (list or str): receiver(s) who will get the mail
        """
        if type(rec_list) == list:
            self._to_address = list(rec_list)
        else:
            self._to_address = [rec_list]

    @property
    def password(self):
        """
        Returns:
            Do not return the visible password.
        """
        return 'Password not visible!'

    @password.setter
    def password(self, pwd):
        self.__password = pwd

    @property
    def smtp(self):
        return self._smtp

    @smtp.setter
    def smtp(self, _smtp):
        self._smtp = _smtp

    @property
    def subject(self):
        return self._subject

    @subject.setter
    def subject(self, _subject):
        self._subject = _subject

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, txt):
        self._text = txt

    # helpers #
    def _set_msg(self):
        self._message['subject'] = self._subject
        self._message['From'] = self._from_address
        self._message['To'] = ','.join(self._to_address)

    def _attach_all(self):
        for path in self._image:
            img = open(path, 'rb')
            msg_img = MIMEImage(img.read())
            img.close()
            msg_img.add_header('Content-ID', '<' + path + '>')
            rich_text = MIMEText('<img src="cid:' + path + '">', 'html', 'utf-8')
            self._message.attach(rich_text)  # KEY HTML text must be attached before image
            self._message.attach(msg_img)

    # necessary methods #
    def set_smtp(self, smtp):
        self.smtp = smtp

    def send_mails(self):
        self._set_msg()
        self._attach_all()
        server = smtplib.SMTP(self._smtp)
        server.set_debuglevel(self._debug)
        server.login(self._from_address, self.__password)
        try:
            server.sendmail(self._from_address, self._to_address, self._message.as_string())
        finally:
            server.quit()

    # optional methods #
    def attach_img(self, path):
        # todo Allow more pictures to be attached
        """
        Push all images' paths into the list
        Args:
            path (str): Relative path of the picture file.
        """
        self._image.append(path)

    def append_rcver(self, receiver):
        self._to_address.append(receiver)

    def set_debug(self, is_):
        self._debug = is_


if __name__ == '__main__':
    import re

    ms = MailSender()
    ms.sender = str(raw_input("Send from: "))
    # handling receivers
    input_rcv = str(raw_input("To (separated by ','): "))
    rcv_list = re.findall(r'([^,]+)\.', input_rcv)
    ms.receivers = rcv_list

    ms.password = str(raw_input("Password: "))

    # todo Set a dictionary of ordinary smtp servers
    ms.set_smtp('smtp.163.com:25')

    ms.subject = str(raw_input("Subject: "))

    # todo Handling image attachment
    ms.attach_img('../Picture1.jpg')

    ms.set_debug(True)
    ms.send_mails()
