#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

import ekg
import main

domain = "http://woox.pl/API/api.php?"

def gg_reminder():
        interval = ["7", "3", "1"]
        for i in interval:
                getReminder = urllib.urlopen(domain + "time=" + i + "&method=gg")
                constReminder = getReminder.read()
                if constReminder != "":
                        sendMessage = main.SendMessage()
                        sendMessage.setUid(constReminder)
                        sendMessage.setMsg("Za %s dni/dzień stracisz ważność konta shell, aby dalej korzystać z konta, proszę o wpłatę, dane do przelewu sprawdzisz wysyłając do mnie wiadomość o treści !acc transfer\nJeśli nie chcesz dalej korzystać poinformuj o tym swojego admina.\nBrak informacji ze strony użytkownika lub wpłaty dzien po upływie terminu oznacza kasacje konta wraz z danymi." % i)
                        sendMessage.sendMessageByUid()

ekg.timer_bind(86400, gg_reminder)