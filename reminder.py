#!/usr/bin/python2.7
# -*- coding: ISO-8859-2 -*-

import ekg
import urllib

domain = "http://woox.pl/API/api.php?"

def autoReminder():
        interval = ["7", "3", "1"]
        for i in interval:
                getReminder = urllib.urlopen(domain + "time=" + i)
                constReminder = getReminder.read()
                if constReminder != "":
                        constReminder = constReminder.split('|')
                        for x in constReminder:
                                ekg.command("msg gg:" + x + " Za " + i + " dni/dzień stracisz ważność konta shell, aby dalej korzystać z konta, proszę o wpłatę, dane do przelewu sprawdzisz wysyłając do mnie wiadomość o treści !acc transfer\nJeśli nie chcesz dalej korzystać poinformuj o tym swojego admina.\nBrak informacji ze strony użytkownika lub wpłaty dzien po upływie terminu oznacza kasacje konta wraz z danymi.")

ekg.timer_bind(86400, autoReminder)