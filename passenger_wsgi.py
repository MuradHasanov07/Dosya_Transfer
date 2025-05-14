import sys
import os

INTERP = os.path.expanduser("/usr/local/bin/python3.9")
if sys.executable != INTERP:
    os.execl(INTERP, INTERP, *sys.argv)

sys.path.append(os.getcwd())

from app import app as application 