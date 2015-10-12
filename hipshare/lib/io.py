import logging
import os
import termios

log = logging.getLogger(__name__)
BUF_SIZE=1024
SEP=b'\r\n' # XXX: portability &c

# Buffered reader impl over lines
class LineReader(object):
    def __init__(self, *emitters):
        self.buf = b''
        self.emitters = emitters

    def read(self, fd):
        # Read into buffer
        data = os.read(fd, BUF_SIZE)
        self.buf += data

        # Shift off lines from the buffer
        idx = self.buf.rfind(SEP)
        if idx != -1:
            idx += len(SEP)
            lines = self.buf[:idx]
            self.buf = self.buf[idx:]

            # Dispatch lines to subscribers
            for emitter in self.emitters:
                emitter(lines.decode('utf-8'))

        # Pass along original data to pty's stdout
        return data
