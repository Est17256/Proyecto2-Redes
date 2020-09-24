import sys
import logging
import getpass
from optparse import OptionParser
import sleekxmpp
from sleekxmpp.exceptions import IqError, IqTimeout
from sleekxmpp.xmlstream.stanzabase import ET, ElementBase
from proyecto2Mods import *

while True:
    print("1)Create Account")
    print("2)Log In")
    opcion = int(input("Select option"))
    if opcion == 1:
        user = input("Enter the user with @redes2020.xyz: ")
        passw = getpass.getpass("Password: ")
        xmpp = Register(user, passw)
        xmpp.register_plugin('xep_0030')
        xmpp.register_plugin('xep_0004')
        xmpp.register_plugin('xep_0066')
        xmpp.register_plugin('xep_0077')

        if xmpp.connect():
            xmpp.process(block=True)
            print("The user is ready")
        else:
            print("No response")
    elif opcion == 2:
        user = input("User: ")
        passw = getpass.getpass("Password: ")
        client = Client(user, passw)
        flag=True
        while flag== True:
            print("1)Log Off")
            print("2)Eliminate Account")
            print("3)Send msg")
            print("4)Add Contact")
            print("5)List of Contact")
            opcion = int(input("Select option"))
            if opcion == 1:
                client.log_off()
                flag=False
            elif opcion == 2:
                user = input("User: ")
                client.un_register(user)
                flag=False
            elif opcion == 3:
                user = input("chat with: ")
                msg = input("msg: ")
                client.send_msg(user, msg)
            elif opcion == 4:
                user = input("User to add: ")
                client.add_user(user)
            elif opcion == 5:
                print("Contacts list: ")
                client.contacts()
    else:
        print("An error has occurred")