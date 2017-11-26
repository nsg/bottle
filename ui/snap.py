import subprocess
import yaml
import datetime
import re

# I found the APIs annoying and took the fun out of this, so
# for now I just parse the output of the snap command... horribe?
# sure, it is, and it will break in the future but it's a start,
# it works :)

class SnapSearchResult:

    def __init__(self, name=None):
        self.name = name
        self.version = None
        self.developer = None
        self.notes = None
        self.summary = None
        self.description = None
        self.publisher = None
        self.contact = None
        self.snap_id = None
        self.commands = None
        self.tracking = None
        self.installed = {}
        self.refreshed = None
        self.channels = {}

def update_result(sr):
    p = subprocess.Popen(["snap", "info", sr.name], stdout=subprocess.PIPE)
    r = p.communicate()
    stdout = r[0].decode('utf-8')

    # The info output is valid YAML so :)
    yd = yaml.load(stdout)

    sr.summary = yd.get('summary', None)
    sr.description = yd.get('description', None)
    sr.publisher = yd.get('publisher', None)
    sr.contact = yd.get('contact', None)
    sr.snap_id = yd.get('snap-id', None)
    sr.commands = yd.get('commands', None)
    sr.tracking = yd.get('tracking', None)
    i = yd.get('installed', {})
    if i:
        i = i.split()
        sr.installed = { "version": i[0], "rev": re.sub("[^0-9]", "",i[1]), "size": i[2] }
    sr.refreshed = yd.get('refreshed', "1970-01-01 00:00:00 +0000 GMT")
    sr.refreshed = datetime.datetime.strptime(sr.refreshed, "%Y-%m-%d %H:%M:%S %z %Z")
    sr.channels = yd.get('channels', {})
    if sr.channels:
        d = {}
        for k,v in sr.channels.items():
            i = v.split()
            if i[0] == "↑":
                sr.channels[k] = d
            else:
                d = { "version": i[0], "rev": re.sub("[^0-9]", "",i[1]), "size": i[2] }
                sr.channels[k] = d

    return sr

def find(name):
    p = subprocess.Popen(["snap", "find", name], stdout=subprocess.PIPE)
    r = p.communicate()
    stdout = r[0].decode('utf-8')
    results = []
    for line in stdout.split("\n")[1:-1]:
        name = line.split()[0]
        sr = SnapSearchResult(name)
        results.append(update_result(sr))
    return results
