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
def respond_to_user_twilio(s, response):
    s.send_header("Content-type", "text/plain")
    s.end_headers()
    s.wfile.write(response)

def process_follow(cmd_dic, platform, conn, cursor):
    rsp_dic = {c.CMD : cmd_dic[c.CMD]}
    args = cmd_dic[c.ARGS]
    user = cmd_dic[c.USER]
    if len(args) == 0:
        repeat = "select * from map where user_id == " + user + " and switch_id == " + str(c.DEFAULT_SWITCH) + ";"
        data = cursor.execute(repeat).fetchall()
        if len(data) == 0:
            rsp_dic[c.SWITCH_ID] = c.DEFAULT_SWITCH
            rsp_dic[c.FOLLOW_TIME] = c.DEFAULT_TIME
            rsp_dic[c.RSP] = c.FOLLOW_MSGS[0]
        else:
            query = "select sub_timeout from map where user_id == " + user + " and switch_id == " + str(c.DEFAULT_SWITCH) + ";"
            end_time = cursor.execute(query).fetchall()[0][0]
            duration = c.DEFAULT_TIME - 1 #do math with end_time to find true answer
            rsp_dic[c.SWITCH_ID] = c.DEFAULT_SWITCH
            rsp_dic[c.FOLLOW_TIME] = duration
            rsp_dic[c.RSP] = c.FOLLOW_MSGS[0]
    elif len(args) == 1:
        validate = "select * from map where"  
        pass
    elif len(args) == 2:
        pass
    else:
        rsp_dic = None
    
    cursor.close()
    conn.close()
    return rsp_dic

def process_unfollow(cmd_dic, platform, conn, cursor):
    pass

def process_add(cmd_dic, platform, conn, cursor):
    response_dic = {}
    args = cmd_dic[c.ARGS]
    if len(args) == 0:
       response_dic = None
    else:
	switch = args[0]
        user = cmd_dic[c.USER]
    	check = "select * from switches where switch_id == " + switch + ";"
	a = cursor.execute(check)
	data = a.fetchall()
        if len(data) > 0:
            response_dic[c.SWITCH_ID] = switch
            response_dic[c.CMD] = cmd_dic[c.CMD]
            unique = "select * from map where switch_id == " + switch + " and user_id == " + user + ";"
            results = cursor.execute(unique).fetchall()
            if len(results) > 0:
                response_dic[c.RSP] = c.ADD_MSGS[1]
            else:
                cursor.execute("INSERT INTO map (switch_id, user_id, switch_name, sub_timeout, fetty_flag) VALUES ("+switch+","+user+",null,null,0);")
                conn.commit()
                response_dic[c.RSP] = c.ADD_MSGS[0]
        else:
            response_dic = None
    cursor.close()
    conn.close()
    return response_dic

def process_remove(cmd_dic, platform, conn, cursor):
    pass

def process_status(cmd_dic, platform, conn, cursor):
    pass

def process_list(cmd_dic, platform, conn, cursor):
    pass

def process_setname(cmd_dic, platform, conn, cursor):
    pass

def process_setdefault(cmd_dic, platform, conn, cursor):
    pass


def validate_user(user, conn, cursor, platform_id):
    check = "select * from users where user_id == " + user + ";"
    results = cursor.execute(check)
    data = results.fetchall()
    if len(data) == 0:
        add_user = "INSERT INTO users (user_id, platform_id, default_switch) VALUES (" + user + ", " + str(platform_id) + ", 1);"
        cursor.execute(add_user)
        conn.commit()

"""execute the user's command"""
def process_command(cmd_dic, platform=False):
    processors = [process_follow, process_unfollow, process_add, process_remove, process_status, process_list, process_setname, process_setdefault]
    command = cmd_dic[c.CMD]
    for cmd, proc in zip(c.VALID_CMDS, processors):
        if cmd == command:
            conn = sqlite3.connect(c.DB)
            cursor = conn.cursor()
            validate_user(cmd_dic[c.USER], conn, cursor, 1)
            return proc(cmd_dic, platform, conn, cursor)


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
            s.send_response(200)
            respond_to_user_twilio(s, response)
        else:
            assert(False)



if __name__ == "__main__":
    #sys.stderr = open("log.txt", "a")
    accept_command()
