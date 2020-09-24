import sys
import logging
import getpass
from optparse import OptionParser
import sleekxmpp
from sleekxmpp.exceptions import IqError, IqTimeout
from sleekxmpp.xmlstream.stanzabase import ET, ElementBase
from proyecto2Mods import *

flag=True
while flag==True:
    print("1)Create Account")
    print("2)Log In")
    print("3)Close")
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
        flag2=True
        while flag2== True:
            print("1)Log Off")
            print("2)Eliminate Account")
            print("3)Send msg")
            print("4)Add Contact")
            print("5)List of Contact")
            print("6)create or join in a group chat")
            print("7)Send message to group chat")
            opcion = int(input("Select option"))
            if opcion == 1:
                client.log_off()
                flag2=False
            elif opcion == 2:
                user = input("User: ")
                client.un_register(user)
                flag2=False
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
            elif opcion == 6:
                group = input("name of the group with @conference.redes2020.xyz: ")
                user = input("User: ")
                client.join_room(group, user)
            elif opcion == 7:
                group = input("send to group with @conference.redes2020.xyz: ")
                msg = input("msg: ")
                client.send_group_msg(group, msg)
            else:
                print("select a valid option")
    elif opcion == 3:
        print("Bye")
        flag=False
    else:
        print("An error has occurred")