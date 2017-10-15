"""Bridge Module

This module contains common code for wifi bridge classes.
"""
import socket
import time


def create_bridge(version, ip, port=None, pause=100, repeat=1, timeout=2):
    """Creates a bridge for a specific version

    >>> bridge = create_bridge(4, '192.168.1.182')
    >>> bridge.on('all')

    Attributes:
        version: Which bridge version to create
        ip: ip/hostname of the bridge
        port: port number of the bridge, leave None for default
        pause: number of milliseconds to wait before sending a comand
        repeat: number of times to repeat a command
        timeout: socket timeout in seconds
    """
    if version is 4 or version is 5:
        from mookfist_lled_controller.bridges.ver4 import Bridge
    elif version is 6:
        from mookfist_lled_controller.bridges.ver6 import Bridge
    else:
        raise Exception('Unsupported protocol version: %s' % version)

    return Bridge(ip=ip, port=port, pause=pause, repeat=repeat, timeout=timeout)


def scan_bridges(version=4, sock=None):
    """Scan for bridges on the network

    Returns a list of available bridges. Each bridge is a tuple of host
    and mac address.

    >>> scan_bridges()
    ('192.168.1.100', 'af:12:d4:ee:90:38')

    Attributes:
        version: Which version to scan for
        sock: If set, will use this socket instead of creating a new one
    """

    if sock is None:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(2)

    sock.bind(('', 0))
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    counter = 0
    max_tries = 5

    bridges = []

    if version is 4 or version is 5:
        scanstr = 'Link_Wi-Fi'
    elif version is  6:
        scanstr = 'HF-A11ASSISTHREAD'
    else:
        raise Exception('Unsupported bridge version: %s' % version)

    while counter < max_tries:
        try:
            sock.sendto(bytearray(scanstr.encode('utf8')), ('255.255.255.255', 48899))
            data = sock.recv(1024)
            if data:
                host, mac = data.split(','.encode('utf8'))[:2]
                bridge = (host.decode('utf8'), mac.decode('utf8'))
                if bridge not in bridges:
                    bridges.append(bridge)
            time.sleep(1)
            counter = counter + 1
        except socket.timeout:
            counter = counter + 1

    return tuple(bridges)


class BaseBridge():
    """Wifi Bridge Abstract Class

    The different versions of the LimitlessLED wifi protocol
    support the same commands but in different formats.

    This class sets up a common bridge class exposing methods
    for those commands.

    Attributes:
        ip: IP or hostname of the wifi bridge
        port: port number of the bridge
        pause: Number of milliseconds to wait before sending a command
        repeat: Number of times to repeat a command
        timeout: Socket timeout
        sock: Your own socket
    """
    def __init__(self, ip, port=None, pause=100, repeat=1, timeout=2, **kwargs):
        self.ip = ip
        self.port = port
        self.pause = pause / 1000
        self.repeat = repeat
        self.timeout = timeout

        sock = kwargs.get('sock', None)
        if sock is None:
            self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self._sock.settimeout(self.timeout)
        else:
            self._sock = sock

    def _groups(self, group):
        try:
            groups = iter(group)
        except TypeError:
            groups = (group,)
        return groups


    def on(self, group=1):
        """Turn on the lights

        Attributes:
            group: Group number(s) or 'all'
        """
        groups = self._groups(group)

        for group in groups:
            self.logger.debug('Turn on group %s' % group)
            g = self._get_group(group)
            self._send(g.on())
            self._last_set_group = group

    def off(self, group=1):
        """Turn off the lights

        Attributes:
            group: Group number(s) or 'all'
        """
        groups = self._groups(group)

        for group in groups:
            self.logger.debug('Turn off group %s' % group)
            g = self._get_group(group)
            self._send(g.off())

        self._last_set_group = None

    def color(self, color, group=1):
        """Set the color for specific group(s)

        Attributes:
            color: A value between 0 and 255
            group: Group number(s) or 'all'
        """
        groups = self._groups(group)

        for group in groups:
            self.logger.debug('Set raw color value to %s for group %s' % (color, group))
            g = self._init_group(group)
            self._send(g.color(color))

    def color_rgb(self, r, g, b, group=1):
        """Set the color for specific group(s) using RGB values

        Attributes:
            r: Red value between 0 and 255
            b: Blue value between 0 and 255
            g: Green value between 0 and 255
            group: Group number(s) or 'al'
        """
        groups = self._groups(group)
        for group in groups:
            self.logger.debug('Set color to rgb(%s,%s,%s) for group %s' % (r, g, b, group))
            grp = self._init_group(group)
            self._send(grp.color_rgb(r, g, b))

    def white(self, group=1):
        """Set color to white

        Attributes:
            group: Group number(s) or 'all'
        """

        groups = self._groups(group)

        for group in groups:
            self.logger.debug('Turn on white color for group %s' % (group))
            g = self._init_group(group)
            self._send(g.white())

    def brightness(self, brightness, group=1):
        """Set brightness

        Attributes:
            brightness: A number between 0 (dark) and 100 (bright)
            group: Group number(s) or 'all'
        """

        groups = self._groups(group)
        for group in groups:
            self.logger.debug('Setting brightness to %s for group %s' % (brightness, group))
            g = self._init_group(group)
            self._send(g.brightness(brightness))

class BaseGroup():
    """Group Interface

    Group classes are used to genreate instances of the Command class
    for the different commands possible.
    """
    def __init__(self, group, bulbtype=None):
        self.group = group
        self.bulbtype = bulbtype

    def on(self):
        raise NotImplementedError()

    def off(self):
        raise NotImplementedError()

    def color(self, color):
        raise NotImplementedError()

    def color_rgb(self, r, g, b):
        raise NotImplementedError()

    def white(self):
        raise NotImplementedError()

    def brightness(self, brightness):
        raise NotImplementedError()
