#!/usr/bin/python

import serial

class _Getch:
    """Gets a single character from standard input.  Does not echo to the
screen."""
    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            self.impl = _GetchUnix()

    def __call__(self): return self.impl()


class _GetchUnix:
    def __init__(self):
        import tty, sys

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


class _GetchWindows:
    def __init__(self):
        import msvcrt

    def __call__(self):
        import msvcrt
        return msvcrt.getch()


getch = _Getch()

class RemoteControl:
    def __init__(self):
        self.ser = serial.Serial('/dev/ttyAMA0', 9600, timeout=1)

    def write(self, c):
        self.ser.write(str(c))
        self.ser.read(1)

if __name__ == '__main__':
    rc = RemoteControl()
    while True:
        c = getch()
        if c == 'q':
            break
        rc.write(c)
