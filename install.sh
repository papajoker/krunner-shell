#!/usr/bin/bash

echo "ps -faux  | grep -E 'krunner'"

sed "s|%{BASE_DIR}|$HOME|g" resources/org.manjaro.shell.krunner.service  > $HOME/.local/share/dbus-1/services/org.manjaro.shell.krunner.service
# cp resources/pamac-shell.service /usr/lib/systemd/user/
 cp -v  resources/plasma-runner-ushell.desktop $HOME/.local/share/kservices5/
 cp -v plugin/krunner_shell.py $HOME/.local/share/kservices5/
 chmod +x $HOME/.local/share/kservices5/krunner_shell.py

if [[ "$1" == "-l" ]]; then
     rm $HOME/.local/share/dbus-1/services/org.manjaro.shell.krunner.service
     rm $HOME/.local/share/kservices5/krunner_shell.py
    # rm /usr/lib/systemd/user/shell-krunner.service
    echo "python plugin/krunner_pamac.py # load dbus server in other terminal"
    #python plugin/krunner_shell.py &
fi

if [[ "$1" == "-r" ]]; then
     rm -v $HOME/.local/share/dbus-1/services/org.manjaro.shell.krunner.service
     rm -v $HOME/.local/share/kservices5/plasma-runner-ushell.desktop
    # rm -v /usr/lib/systemd/user/shell-krunner.service
     rm -v $HOME/.local/share/kservices5/krunner_shell.py
    ps -aux | grep 'krunner'
fi

kquitapp5 krunner
#kstart5 krunner
#qdbus org.kde.krunner /App org.kde.krunner.App.querySingleRunner usershell ls:/etc/pa
#qdbus --literal org.manjaro.shell.krunner /krunner org.kde.krunner1.Match "ls:/etc/pac"

