import sys
import logging
import getpass
from optparse import OptionParser
import sleekxmpp
from sleekxmpp.exceptions import IqError, IqTimeout
from sleekxmpp.xmlstream.stanzabase import ET, ElementBase
#Class for user register
class Register(sleekxmpp.ClientXMPP):
    #Init ClientXMPP object
    def __init__(self, jid, password):
        sleekxmpp.ClientXMPP.__init__(self, jid, password)
        self.add_event_handler("session_start", self.start)
        self.add_event_handler("register", self.register)
    #Start the user registration
    def start(self, event):
        self.send_presence()
        self.get_roster()
        self.disconnect()
    #user registration on server
    def register(self, iq):
        resp = self.Iq()
        resp['type'] = 'set'
        resp['register']['username'] = self.boundjid.user
        resp['register']['password'] = self.password
        try:
            resp.send(now=True)
            logging.info("Account ready for %s!" % self.boundjid)
        except IqError as e:
            logging.error("Could not register account: %s" % e.iq['error']['text'])
            self.disconnect()
        except IqTimeout:
            logging.error("No response")
            self.disconnect()

class Client(sleekxmpp.ClientXMPP):
    #Init ClientXMPP object
    def __init__(self, jid, password):
        sleekxmpp.ClientXMPP.__init__(self, jid, password)
        self.add_event_handler("session_start", self.start)
        # self.add_event_handler("message", self.mensajeria)

        self.register_plugin('xep_0077')
        self.register_plugin('xep_0030') # Service Discovery
        self.register_plugin('xep_0199') # XMPP Ping
        self.register_plugin('xep_0004') # Data forms
        self.register_plugin('xep_0077') # In-band Registration
        self.register_plugin('xep_0045') # Mulit-User Chat (MUC)
        self.register_plugin('xep_0096') # Jabber Search
        self.register_plugin('xep_0065')
        self.register_plugin('xep_0047', {'auto_accept': True})

        if self.connect():
            print("successful")
            self.process(block=False)
        else:
            print("No response")
    #Send the presence to the server
    def start(self, event):
        self.send_presence()
        self.get_roster()
    #Disconnect the user from the server
    def log_off(self):
        self.disconnect(wait=False)
        print("logged off")
    #Eliminate the account from the server
    def un_register(self, user):
        delete = self.Iq()
        delete['type'] = 'set'
        delete['from'] = user
        Stanza = ET.fromstring("<query xmlns='jabber:iq:register'><remove/></query>")
        delete.append(Stanza)
        try:
            delete.send(now=True)
            print("The account was eliminated")
            self.disconnect(wait=False)
            print("logged off")
        except IqError as e:
            print("An error has occurred", e)
        except IqTimeout:
            print("No response")
    #Recieve message from another client
    def recieve_msg(self, msg):
        print(str(msg['from'].user), msg['body'])
    #Send message to another client
    def send_msg(self, user, msg):
        self.send_message(mto=user,mbody=msg,mtype="chat")