"""
Plugin for controlling package_manager on wechat.

Input to active manage-mode:
Local: 'manage -l ' + account_name
Foreign: 'manage -f ' + account_name + ' ' + key

To exit manage-mode:
'manage -d'
"""
from plugin import Plugin


class ManagerController(Plugin):
    def __init__(self, key, account_name):
        super(ManagerController, self).__init__(name='manager-controller', properties=['system'])
        self.__key = key
        self.__name = account_name
        self.__msg = ''
        self.__from = ''
        self.__to = ''

        self.__manage_mode = False

    # Helpers
    # Manage mode selector
    def verify(self):
        local = 'manage -l {0}'.format(self.__name)
        foreign = 'manage -f {0} {1}'.format(self.__name, self.__key)
        if self.__msg == local and self.__from == self.__to:
            return 'local'
        elif self.__msg == foreign:
            return 'foreign'
        else:
            return None

    def exit_mode(self):
        return self.__msg == 'manage -d'

    # Operations

    # Reply message
    def confirm_info(self, cfm_type):
        # todo
        pass

    # Override / API
    def filter(self, msg):
        if msg['Type'] != 'Text':
            return False
        self.__msg = msg['Text']                # Get message content
        self.__from = msg['FromUserName']
        self.__to = msg['ToUserName']

        # Handle special input
        if self.verify() is not None:
            self.__manage_mode = True
            return True
        else:
            return True if self.__manage_mode else False

    def handle_msg(self):
        # Mode en/disabling
        verification = self.verify()
        if verification is not None:
            self.confirm_info(verification)
        elif self.exit_mode():
            self.confirm_info('exit')

        # Manage mode operations todo

    def __str__(self):
        return 'manager-controller'

