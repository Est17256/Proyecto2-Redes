import sys
import logging
import getpass
from optparse import OptionParser
import sleekxmpp
from sleekxmpp.exceptions import IqError, IqTimeout

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
#Create user function
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
    print("Creation Fail")