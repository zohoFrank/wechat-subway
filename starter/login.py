from mail_pic import MailSender
import os
import itchat
import threading
import time
from PIL import Image

TEST_MAILBOX = 'zohotestcode@163.com'
SMTP_SERVER = 'smtp.163.com:25'
CONTENT = '[EMG] QR CODE from login.py'
PASSWORD = 'zoho_test'

PIC_NAME = 'QR.jpg'


def search_qr():
    delete_exist()
    while True:
        try:
            img = Image.open(PIC_NAME)
            if img is not None:
                print '\n>> Found QR\n>> Sending mails\n'
                time.sleep(1.5)
                send_mail()
                return
        except:
            continue


def delete_exist():
    cur_dir = os.getcwd()
    pic_path = os.path.join(cur_dir, PIC_NAME)
    if os.path.exists(pic_path):
        os.remove(pic_path)


def send_mail():
    ms = MailSender(TEST_MAILBOX, [TEST_MAILBOX], PASSWORD)
    ms.subject = CONTENT
    ms.smtp = SMTP_SERVER
    ms.attach_img(PIC_NAME)
    # ms.set_debug(True)
    ms.send_mails()
    print ">> Mail sent!"


class MailLogin(threading.Thread):
    def __init__(self, func, args=()):
        """
        Args:
            func (function): Function that ready to be invoked
            args (tuple): Arguments of invoked function
        """
        super(MailLogin, self).__init__()
        self.function = func
        self.args = args

    def run(self):
        if self.args == ():
            self.function()
        else:
            self.function(self.args)


def mail_login():
    # fixme Need thread lock
    thread1 = MailLogin(search_qr)
    thread2 = MailLogin(itchat.auto_login)
    thread1.start()
    thread2.start()
