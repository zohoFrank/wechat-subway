class PackageManager(object):

    def __init__(self):
        self.enabled_plugins = {
            'system': [],
            'text': [],
            'map': [],
            'card': [],
            'note': [],
            'sharing': [],
            'picture': [],
            'recording': [],
            'attachment': [],
            'video': [],
            'friends': [],
            'useless': []
        }

    def list(self, ptype=None):
        if ptype is not None:
            return {ptype: self.enabled_plugins[ptype]}
        return self.enabled_plugins

    def install(self, plugin):
        pass

    def uninstall(self, plugin):
        pass

    def register_all(self):
        pass
