import re
import os
import time

PARSE_REX = re.compile(" for\s+(\S+)(\s+from\s+(\S+)\s+port\s+(\d+))?")

def parse(string, base_time):
    """
    >>> parse("Jan 01 00:11:22 srv1 sshd[1000]: Accepted password for xxxx from 10.10.0.1 port 64000 ssh2", time.gmtime())
    >>> parse("Jan  1 00:11:22 srv1 sshd[1000]: Accepted password for xxxx from 10.10.0.1 port 64000 ssh2", time.gmtime())
    >>> parse("Feb 22 11:22:33 srv1 sshd[2000]: Failed password for xxxx from 10.10.0.2 port 4550 ssh2", time.gmtime())
    >>> parse("Mar 30 22:33:44 srv1 sshd[3000]: fatal: Timeout before authentication for 10.10.0.3", time.gmtime())
    """

    bites = string.split(None, 5)
    if len(bites) < 6:
        return None

    try:
        ts = time.strptime(" ".join(bites[:3]), "%b %d %H:%M:%S")
    except ValueError:
        return None

    if ts[1:] > base_time[1:]:
        ts = time.mktime((base_time[0]-1,) + ts[1:])
    else:
        ts = time.mktime((base_time[0],) + ts[1:])

    result = dict()
    result["timestamp"] = time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime(ts))
    result["server"] = bites[3]

    match = PARSE_REX.search(bites[5])
    if match is not None:
        _for, group, _from, port = match.groups()
        if group is not None:
            result["user"] = _for
            result["ip"] = _from
            result["port"] = port
        else:
            result["ip"] = _for
        result["message"] = bites[5][:match.start()]
    else:
        result["message"] = bites[5]

    return result

from abusehelper.contrib.tailbot.tailbot import TailBot

class SSHLogBot(TailBot):

    def parse(self, line, mtime):
        return parse(line, time.gmtime(mtime))

if __name__ == "__main__":
    SSHLogBot.from_command_line().execute()