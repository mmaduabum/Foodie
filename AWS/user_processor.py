import sh
from twilio.rest import TwilioRestClient
import sys
import messager
import sqlite3
import time
import BaseHTTPServer
import twilio_parser as parser


HOST_NAME = ""
PORT_NUMBER = 80
TWILIO_SIGNATURE = "x-twilio-signature"
FROM = "'From'"
MSG = "'Body'"
SPOOKY_INDEX = 4


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
        if TWILIO_SIGNATURE in s.headers:
            http_in = s.rfile.read(int(s.headers.getheader('Content-Length')))
            dic = parser.twilio_to_dic(http_in)
            print dic[MSG]
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
    parrot = server_class((HOST_NAME, PORT_NUMBER), UserHandler)
    parrot.serve_forever()
    parrot.server_close()
