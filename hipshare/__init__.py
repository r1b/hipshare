import logging
import pty
import shlex
import sys

from hipshare.lib.config import Config
from hipshare.lib.io import LineReader
from hipshare.lib.util import die, usage
from hipshare.lib.xmpp import Client

import hipshare.lib.logger

log = logging.getLogger(__name__)

class Hipshare(object):
    def __init__(self, strategy):
        self.config = Config(strategy)
        self.xmpp = Client(self.config)
        self.reader = LineReader(self.xmpp.line_emitter)

    def share(self):
        # XXX: Not very pythonic >:(
        log.debug("Establishing XMPP connection")
        if not self.xmpp.connect():
            die("Could not connect, see xmpp.log for details")

        # Join all rooms
        muc_plugin = self.xmpp.get_plugin('xep_0045')
        log.debug("Joining rooms: {}".format(self.config.strategy['rooms']))
        for room in self.config.strategy['rooms']:
            muc_plugin.joinMUC(room, self.config.options['nick'])

        # Process XMPP events in another thread
        log.debug("Spawning XMPP worker")
        self.xmpp.process()

        '''
        Spawn a new shell in a pseudo terminal, pty polls with select()
        and notifies LineReader when data is available. There's an annoying
        bug right now; pty doesn't know when to die because it never
        gets EOF. Idk how to deal with this but you can just hit crlf twice
        after exiting the shell.
        '''
        log.info("@_@ You are being watched @_@")
        pty.spawn(self.config.options['shell'], self.reader.read)
        log.info("X_X You are alone again X_X")

        # Close XMPP connection
        # XXX: If I didn't set send_close=False here, this took a long time
        # to exit. My guess is that hipchat doesn't properly respond to the
        # stream footer but idk.
        log.debug("Tearing down XMPP connection")
        self.xmpp.disconnect(send_close=False)

if __name__ == "__main__":
    try:
        hipshare = Hipshare(sys.argv[1])
    except IndexError:
        usage()
    hipshare.share()
