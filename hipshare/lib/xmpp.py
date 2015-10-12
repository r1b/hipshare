import logging
from sleekxmpp import ClientXMPP

log = logging.getLogger(__name__)

class HipshareXMPP(ClientXMPP):
    def __init__(self, jid, password):
        ClientXMPP.__init__(self, jid, password)

        self.add_event_handler("session_start", self.session_start, threaded=True)

    def session_start(self, event):
        self.send_presence()
        self.get_roster()

class Client(object):
    def __init__(self, config):
        self.config = config
        self.xmpp = HipshareXMPP(config.strategy['jid'], config.strategy['password'])

        for plugin in config.options['plugins']:
            self.xmpp.register_plugin(plugin)

    def connect(self, *args, **kwargs):
        return self.xmpp.connect(*args, **kwargs)

    def disconnect(self, *args, **kwargs):
        return self.xmpp.disconnect(*args, **kwargs)

    def get_plugin(self, plugin):
        return self.xmpp.plugin[plugin]

    def process(self, *args, **kwargs):
        return self.xmpp.process(*args, **kwargs)

    def line_emitter(self, data):
        log.debug("Emitting {} to {}:".format(data, self.config.strategy['rooms']))
        for room in self.config.strategy['rooms']:
            self.xmpp.send_message(**{
                "mto": room,
                "mbody": data,
                "mtype": 'groupchat'
            })
