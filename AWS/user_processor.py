import sh
from twilio.rest import TwilioRestClient
import sys
import messager
import sqlite3
import time
import BaseHTTPServer
import twilio_parser as parser
import constants as c



"""Listen on port 80 for incoming user command"""
def accept_command():
    server_class = BaseHTTPServer.HTTPServer
    parrot = server_class((c.HOST_NAME, c.USER_PORT_NUMBER), UserHandler)
    parrot.serve_forever()
    parrot.server_close()


"""Notify the user on the status of the command"""
def respond_to_user(user, response):
    messager.send_message(user, response)


def process_follow(cmd_dic, platform):
    pass

def process_unfollow(cmd_dic, platform):
    pass

def process_add(cmd_dic, platform):
    pass

def process_remove(cmd_dic, platform):
    pass

def process_status(cmd_dic, platform):
    pass

def process_list(cmd_dic, platform):
    pass

def process_setname(cmd_dic, platform):
    pass

def process_setdefault(cmd_dic, platform):
    pass


"""execute the user's command"""
def process_command(cmd_dic, platform=False):
    processors = [process_follow, process_unfollow, process_add, process_remove, process_status, process_list, process_setname, process_setdefault]
    command = cmd_dic[c.CMD]
    for cmd, proc in zip(c.VALID_CMDS, processors):
        if cmd == command:
            return proc(cmd_dic, platform)


class UserHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    #we dk
    def do_HEAD(s):
        pass

    #handle get request
    def do_GET(s):
        pass

    #handle Twilio Post
    def do_POST(s):
        if c.TWILIO_SIGNATURE in s.headers:
            http_in = s.rfile.read(int(s.headers.getheader('Content-Length')))
            twilio_dic = parser.twilio_to_dic(http_in)
            user = twilio_dic[c.FROM]
            commands = parser.get_command(user, twilio_dic[c.MSG])
            resp_dic = process_command(commands) if commands is not None else None
            response = parser.build_response(user, resp_dic)
            print response
            s.send_response(200)
            respond_to_user(user, response)
            #s.wfile.write(response) --fuck twilio
        else:
            assert(False)



if __name__ == "__main__":
    accept_command()
