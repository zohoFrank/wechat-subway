import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.text import MIMEText


class MailSender(object):
    """
    Attributes:
        _from_address (str): Sender's mail address
        _to_address (List[str]): Receivers' mail addresses
        __password (str): Password of sender's email
        _smtp (str): Sender's mail SMTP server address and port
        _subject (str): Title of the mail, usually default
        _debug (bool): Debug level
    """
    def __init__(self, sender='', receivers=None, password=''):
        if receivers is None:
            receivers = []
        self._from_address = sender
        self._to_address = receivers
        self.__password = password
        self._smtp = ''
        self._subject = '[EMERGENT] Wechat Login QR code'
        self._debug = False
        # call helpers
        self._set_msg()

    # getter and setter #
    @property
    def sender(self):
        return self._from_address

    @sender.setter
    def sender(self, email):
        self._from_address = email

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
        self._subject = _subject;

    # helpers #
    def _set_msg(self):
        self._message = MIMEMultipart()
        self._message['subject'] = self._subject
        self._message['From'] = self._from_address
        self._message['To'] = ','.join(self._to_address)

    # necessary methods #
    def set_smtp(self, smtp):
        self.smtp = smtp

    def attach_rich_text(self, text_part):
        # todo Reveal image in the mail
        """
        Attach html format text to the mail.
        Args:
            text_part (str): Text with or without html elements.
        """
        msg_text = MIMEText('<img src="cid:qr">' + text_part, 'html', 'utf-8')
        self._message.attach(msg_text)

    def attach_img(self, path):
        # todo Allow more pictures to be attched
        """
        Attach image to the mail if necessary.
        Args:
            path (str): Relative path of the picture file.
        """
        img = open(path, 'rb')
        msg_img = MIMEImage(img.read())
        img.close()
        msg_img.add_header('Content-ID', '<qr>')
        self._message.attach(msg_img)

    def send_mails(self):
        server = smtplib.SMTP(self._smtp)
        server.login(self._from_address, self.__password)
        server.set_debuglevel(self._debug)
        try:
            server.sendmail(self._from_address, self._to_address, self._message.as_string())
        finally:
            server.quit()

    # optional methods #
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
    ms.attach_rich_text(str(raw_input("Content: ")))

    # todo Handling image attachment
    ms.attach_img('../Picture1.jpg')
    ms.send_mails()
