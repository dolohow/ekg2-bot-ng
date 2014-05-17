#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

import ekg
import main
import urllib
import smtplib
from email.mime.text import MIMEText
from email.parser import Parser

domain = "http://woox.pl/API/api.php?"
interval = ["7", "3", "1"]

def gg_reminder():
    interval = ["7", "3", "1"]
    for i in interval:
        getReminder = urllib.urlopen(domain + "time=" + i + "&method=gg")
        constReminder = getReminder.read()
        if constReminder != "":
            sendMessage = main.SendMessage()
            sendMessage.setUid(constReminder)
            sendMessage.setMsg("Za %s dni/dzień stracisz ważność konta shell, aby dalej korzystać z konta, proszę o wpłatę, dane do przelewu sprawdzisz wysyłając do mnie wiadomość o treści !transfer\nJeśli nie chcesz dalej korzystać poinformuj o tym swojego admina.\nBrak informacji ze strony użytkownika lub wpłaty dzien po upływie terminu oznacza kasacje konta wraz z danymi." % i)
            sendMessage.sendMessageByUid()



def email_reminder():
    msg = open('content', 'r').read()
    s = smtplib.SMTP('localhost')
    for i in interval:
        get = urllib.urlopen(domain + "time=" + i + "&method=email").read().split(',')
        for x in get:
            if x != '':
                tmp = x.split(':')
                try:
                    s.sendmail("tacajushi@woox.pl",tmp[1], msg.format(tmp[1], tmp[0], i))
                    ekg.echo("Wysłano email z przypomnieniem do: %s" % tmp[1])
                except Exception as e:
                    ekg.echo(e)

ekg.timer_bind(86400, gg_reminder)
ekg_timer_bind(86400, email_reminder)
