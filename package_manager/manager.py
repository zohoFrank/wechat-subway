
class PackageManager(object):

    def __init__(self):
        self._installed = []
        self._active = []
        self._available = []

    @property
    def installed(self):
        return self._installed

    @property
    def active(self):
        return self._active

    @property
    def available(self):
        return self.available

    def install_plugin(self, plugin):
        pass

    def disable_plugin(self, plugin):
        pass

    def enable_plugin(self, plugin):
        pass

    def scan_available_plugins(self, plugin):
        pass
