#!/bin/env python3

"""
https://cgit.kde.org/krunner.git/plain/src/data/org.kde.krunner1.xml
https://api.kde.org/frameworks/krunner/html/runnercontext_8cpp_source.html#l00374
https://techbase.kde.org/Development/Tutorials/Plasma4/AbstractRunner

"""
'''
qdbus org.kde.krunner /App org.kde.krunner.App.querySingleRunner kshell ls:/etc/pa
qdbus --literal org.manjaro.shell.krunner /krunner org.kde.krunner1.Match "ls:/etc/pac"
'''
'''
lire ~/.config/kshell.sh

# creer 2 funtions par plugin
### ls: ###
run_ls (){
  dolphin $1
}
match_ls(){
  # retourne une liste
}

main(){
  kshell.sh ls match        (match_ls)
  kshell.sh ls run /etc/    (run_ls /etc/)
}
'''

from pathlib import Path
import subprocess
from dataclasses import dataclass
import dbus.service
from dbus.mainloop.glib import DBusGMainLoop
import gi
from gi.repository import GLib


DBusGMainLoop(set_as_default=True)

objpath = "/krunner"
iface = "org.kde.krunner1"


class Runner(dbus.service.Object):
    def __init__(self):
        """ set dbus and load alpm """
        dbus.service.Object.__init__(self, dbus.service.BusName("org.manjaro.shell.krunner", dbus.SessionBus()), objpath)
        # read config match_*** functions """
        self.config = f"{Path.home()}/.config/krunnershell.sh"
        self.actions = ()
        self.prefix = ""
        with open(self.config, "r") as file_in:
            for line in file_in:
                if line.startswith('match_'):
                    name = line[6:].rsplit('(', 1)[0]
                    if name:
                        self.actions += (name,)
        print(self.actions)

    '''def _setrelevance(self, pkg: Package, query: str)->float:
        """ list order, display only top 10/20 by relevance """
        mini = 0.01
        relevance = mini
        name = pkg.get_name()
        if query == name:
            relevance = 1
        elif name.startswith(query) and not "-i18n" in name:
            relevance = 0.4
        else:
            relevance = 0.2 if query in name else mini
            if "-i18n" in name:
                relevance = mini
        return relevance'''

    @dbus.service.method(iface, in_signature='s', out_signature='a(sssida{sv})')
    def Match(self, query: str):
        """ get the matches and returns a packages list """
        self.prefix = ""
        query = query.strip().lower()
        print(f"match: {query}...")
        if not self.actions or not ":" in query:
            return []

        #TEST plugin without datas
        #return [tuple([n, n, "", 32, 0.5, {"subtext": ""}]) for n in self.actions]

        self.prefix = query.split(':', 1)[0]
        if self.prefix not in self.actions:
            return []
        query = query[len(self.prefix)+1:].strip()

        out, _ = subprocess.Popen(
            f"bash -c 'source {self.config} && match_{self.prefix} \"{query}\"'",
            shell=True, text=True,
            stdout=subprocess.PIPE
        ).communicate()
        print(f"stdout cmd: match_{self.prefix} \"{query}\" : {out}")

        if "||" in out:
            #if title != to run
            #split line and set [0] in data and [1] in titre
            ret = []
            for node in out.splitlines():
                data = node.split("||", 1)
                ret.append(tuple([data[0], data[1], "", 32, 0.8, {"subtext": ""}]))
            return ret
        else:
            return [tuple([node, node, "", 32, 0.8, {"subtext": ""}]) for node in out.splitlines()]

    @dbus.service.method(iface, in_signature='ss')
    def Run(self, data: str, _action_id: str):
        """ click on item, run command """
        pid = subprocess.Popen(f"bash -c 'source {self.config} && run_{self.prefix} {data}'", shell=True).pid
        #pid = subprocess.Popen(f"xdg-open \"{data}\"", shell=True).pid



runner = Runner()
loop = GLib.MainLoop()
loop.run()