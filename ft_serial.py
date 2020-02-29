#! /usr/bin/env python
# -*- coding: utf-8 -*-
import io
import time
import sys
PARITY_NONE, PARITY_EVEN, PARITY_ODD, PARITY_MARK, PARITY_SPACE = 'N', 'E', 'O', 'M', 'S'
STOPBITS_ONE, STOPBITS_ONE_POINT_FIVE, STOPBITS_TWO = (1, 1.5, 2)
FIVEBITS, SIXBITS, SEVENBITS, EIGHTBITS = (5, 6, 7, 8)

PARITY_NAMES = {
    PARITY_NONE: 'None',
    PARITY_EVEN: 'Even',
    PARITY_ODD: 'Odd',
    PARITY_MARK: 'Mark',
    PARITY_SPACE: 'Space',
}

class SerialBase(io.RawIOBase):
    """\
    Serial port base class. Provides __init__ function and properties to
    get/set port settings.
    """

    # default values, may be overridden in subclasses that do not support all values
    BAUDRATES = (50, 75, 110, 134, 150, 200, 300, 600, 1200, 1800, 2400, 4800,
                 9600, 19200, 38400, 57600, 115200, 230400, 460800, 500000,
                 576000, 921600, 1000000, 1152000, 1500000, 2000000, 2500000,
                 3000000, 3500000, 4000000)
    BYTESIZES = (FIVEBITS, SIXBITS, SEVENBITS, EIGHTBITS)
    PARITIES = (PARITY_NONE, PARITY_EVEN, PARITY_ODD, PARITY_MARK, PARITY_SPACE)
    STOPBITS = (STOPBITS_ONE, STOPBITS_ONE_POINT_FIVE, STOPBITS_TWO)

    def __init__(self,
                 port=None,
                 baudrate=9600,
                 bytesize=EIGHTBITS,
                 parity=PARITY_NONE,
                 stopbits=STOPBITS_ONE):
        """Initialize comm port object. If a "port" is given, then the port will be
            opened immediately. Otherwise a Serial port object in closed state
            is returned.
        """

        self.is_open = False
        self.portstr = None
        # correct values are assigned below through properties
        self.name = None
        self._port = None
        self._baudrate = None
        self._bytesize = None
        self._parity = None
        self._stopbits = None

        # assign values using get/set methods using the properties feature
        self.port = port
        self.baudrate = baudrate
        self.bytesize = bytesize
        self.parity = parity
        self.stopbits = stopbits

    ##-------------Порт----------##
    @property
    def port(self):
            """\
                Get the current port setting. The value that was passed on init or using
                setPort() is passed back.
            """
            return self._port

    @port.setter
    def port(self, port):
        if port is not None and not isinstance(port, str):
            print("\"port\" must be None or a string")
        was_open = self.is_open
        if was_open:
            self.close()
            self.portstr = port
            self._port = port
            self.name = self.portstr
            if was_open:
                self.open()

    ##---------Скорость--------##
    @property
    def baudrate(self):
        return self._baudrate

    @baudrate.setter
    def baudrate(self, baudrate):
        try:
            b = int(baudrate)
        except TypeError:
            raise ValueError("Not a valid baudrate: {!r}".format(baudrate))
        else:
            if b < 0:
                print("ERROR: \'baudrate\' must be positive")
                exit(1)
            self._baudrate = b
            if self.is_open:
                pass

    ##_____Бит данных_____##
    @property
    def bytesize(self):
        """Get the current byte size setting."""
        return self._bytesize

    @bytesize.setter
    def bytesize(self, bytesize):
        """Change byte size."""
        if bytesize not in self.BYTESIZES:
            print("Not a valid byte size: \'" + str(bytesize) + "\'")
        self._bytesize = bytesize
        if self.is_open:
            pass
            # self._reconfigure_port()

    ##_____Бит четности_____##
    @property
    def parity(self):
        """Get the current parity setting."""
        return self._parity

    @parity.setter
    def parity(self, parity):
        """Change parity setting."""
        if parity not in self.PARITIES:
            print("Not a valid parity: {!r}".format(parity))
        self._parity = parity
        if self.is_open:
            pass
            # self._reconfigure_port()

    ##------------Стопбит-------------##
    @property
    def stopbits(self):
        """Get the current stop bits setting."""
        return self._stopbits

    @stopbits.setter
    def stopbits(self, stopbits):
        """Change stop bits size."""
        if stopbits not in self.STOPBITS:
            print("Not a valid stop bit size: {!r}".format(stopbits))
        self._stopbits = stopbits
        if self.is_open:
            pass
            # self._reconfigure_port()
