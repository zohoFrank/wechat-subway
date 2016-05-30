from mail_pic import MailSender

import itchat
import thread
import re
from PIL import Image

TEST_MAILBOX = 'zohotestcode@163.com'
SMTP_SERVER = 'smtp.163.com:25'
CONTENT = 'QR CODE'
PASSWORD = 'zoho_test'


def send_qr():
    ms = MailSender()

    ms.sender = TEST_MAILBOX
    ms.receivers = TEST_MAILBOX
    ms.password = PASSWORD
    ms.set_smtp(SMTP_SERVER)

    ms.subject = CONTENT
    ms.attach_rich_text(CONTENT)

    while True:
        try:
            img = Image.open('QR.jpg')
            if img is not None:
                print "\n>> QR Found\n"
                ms.attach_img('QR.jpg')
                ms.send_mails()
                return
        except:
            pass


def login_method(method=''):
    """
    Main login functions caller.
    Args:
        method (str): Any string not equal to '' will be considered as using email.

    """
    thread.start_new_thread(itchat.auto_login(), ())
    if method != '':
        thread.start_new_thread(send_qr(), ())
    else:
        return


if __name__ == '__main__':
    itchat.auto_login()