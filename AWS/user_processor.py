import sh
from twilio.rest import TwilioRestClient
import sys
import messager
import sqlite3
import time
import BaseHTTPServer
import twilio_parser as parser
import constants as c




class UserHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    #we dk
    def do_HEAD(s):
        pass

    #handle get request
    def do_GET(s):
        pass

    #handle Twilio Post
    def do_POST(s):
        print "="*80
        if c.TWILIO_SIGNATURE in s.headers:
            http_in = s.rfile.read(int(s.headers.getheader('Content-Length')))
            twilio_dic = parser.twilio_to_dic(http_in)
            commands = parser.get_command(twilio_dic[c.FROM], twilio_dic[c.MSG])
            print commands
        s.send_response(200)


"""execute the user's command"""
def process_command():
	pass


"""Notify the user on the status of the command"""
def respond_to_user():
	pass


"""Listen on port 80 for incoming user command"""
def accept_command():
	pass



if __name__ == "__main__":
    server_class = BaseHTTPServer.HTTPServer
    parrot = server_class((c.HOST_NAME, c.USER_PORT_NUMBER), UserHandler)
    parrot.serve_forever()
    parrot.server_close()
