import sh
from twilio.rest import TwilioRestClient
import sys
import messager as m
import sqlite3
import time
from time_utils import timestamp_to_seconds
import BaseHTTPServer
import twilio_parser as parser
import constants as c


def sanitize(cmds):
    if cmds is None: return True
    args = cmds[c.ARGS]
    bad = ";!@#$%^&*()-_<>.,\\/\"{}[]~"
    for a in args:
        if (not set(a).isdisjoint(bad)):
            return False
    return True


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
    rsp_dic = None
    args = cmd_dic[c.ARGS]
    user = cmd_dic[c.USER]
    current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
    #no time specified. one time follow
    if len(args) > 0:
        rsp_dic = {c.CMD : cmd_dic[c.CMD]}
        switch = args[0]
        repeat = "select fetty_flag from map where user_id == " + user + " and switch_id == " + str(switch) + ";"
        data = cursor.execute(repeat).fetchall()
        rsp_dic[c.RSP] = c.FOLLOW_MSGS[0]
        rsp_dic[c.SWITCH_ID] = switch
        #add switch first
        if len(data) == 0:
            add_default = "insert into map (switch_id, user_id, switch_name, sub_timeout, fetty_flag) values (" + \
                             str(switch) + ", " + user + ", null, null, 1);"
            #add time if needed
            if len(args) == 2:
                minutes = args[1]
                add_default = 'insert into map (switch_id, user_id, switch_name, sub_timeout, fetty_flag) values (' + switch + \
                     ', ' + user + ', null, ' + 'DATETIME("' + current_time + '", "+' + minutes + ' minutes"), 1);'
                rsp_dic[c.FOLLOW_TIME] = minutes

            cursor.execute(add_default)
            conn.commit()

        #set fetty flag or flag and time
        else:
            if str(data[0][0]) != "1":
                update = 'update map set fetty_flag = 1  where user_id == ' + user + ' and switch_id == ' + str(switch) + ';'
                
                if len(args) == 2:
                    minutes = args[1]
                    update = 'update map set fetty_flag = 1, sub_timeout = DATETIME("' + current_time + '", "+' + minutes + ' minutes")' + \
                            ' where user_id == ' + user + ' and switch_id == ' + str(switch) + ';'
                    rsp_dic[c.FOLLOW_TIME] = minutes

                cursor.execute(update)
                conn.commit()
            #user is already following
            else:
                rsp_dic[c.RSP] = c.FOLLOW_MSGS[1]

    cursor.close()
    conn.close()
    return rsp_dic


def process_unfollow(cmd_dic, platform, conn, cursor):
    response_dic = {}
    args = cmd_dic[c.ARGS]
    #This command must have at least 1 argument
    if len(args) == 0:
        response_dic = None
    else:
        switch = args[0]
        user = cmd_dic[c.USER]
        check = "select * from switches where switch_id == " + switch + ";"
        a = cursor.execute(check)
        data = a.fetchall()
        #This is a valid switch id
        if len(data) > 0:
            response_dic[c.SWITCH_ID] = switch
            response_dic[c.CMD] = cmd_dic[c.CMD]
            unique = "select * from map where switch_id == " + switch + " and user_id == " + user + " and fetty_flag == 1;"
            results = cursor.execute(unique).fetchall()
            #There is a map from switch to user with an on flag
            if len(results) > 0:
                cursor.execute("update map set fetty_flag = 0, sub_timeout = null where switch_id == "+switch+" and user_id == "+user+";")
                conn.commit()
                response_dic[c.RSP] = c.UNFOLLOW_MSGS[1]
            # there is no (switch, id) pair in map being followed
            else:
                unique = "select * from map where switch_id == " + switch + " and user_id == " + user  + ";"
                results = cursor.execute(unique).fetchall()
                #There is a switch to user pair in map, need to follow it before they can unfollow it
                if len(results) > 0:
                    response_dic[c.RSP] = c.UNFOLLOW_MSGS[0]
                #so tell them to add it before they can unfollow it
                else:
                    response_dic[c.RSP] = c.UNFOLLOW_MSGS[2]
        #The supplied switch id is not a valid switch id
        else:
            response_dic = None
    cursor.close()
    conn.close()
    return response_dic

def process_add(cmd_dic, platform, conn, cursor):
    response_dic = {}
    args = cmd_dic[c.ARGS]
    #This command must have at elast 1 argument
    if len(args) == 0:
       response_dic = None
    else:
	switch = args[0]
        user = cmd_dic[c.USER]
    	check = "select * from switches where switch_id == " + switch + ";"
	a = cursor.execute(check)
	data = a.fetchall()
        #This is a valid switch id
        if len(data) > 0:
            response_dic[c.SWITCH_ID] = switch
            response_dic[c.CMD] = cmd_dic[c.CMD]
            unique = "select * from map where switch_id == " + switch + " and user_id == " + user + ";"
            results = cursor.execute(unique).fetchall()
            #The switch has already been added
            if len(results) > 0:
                response_dic[c.RSP] = c.ADD_MSGS[1]
            #Add the switch to the database
            else:
                cursor.execute("INSERT INTO map (switch_id, user_id, switch_name, sub_timeout, fetty_flag) VALUES ("+switch+","+user+",null,null,0);")
                conn.commit()
                response_dic[c.RSP] = c.ADD_MSGS[0]
        #The supplied switch id is not a valid switch id
        else:
            response_dic = None
    cursor.close()
    conn.close()
    return response_dic

def process_remove(cmd_dic, platform, conn, cursor):
    response_dic = {}
    args = cmd_dic[c.ARGS]
    #This command must have at elast 1 argument
    if len(args) == 0:
        response_dic = None
    else:
        switch = args[0]
        user = cmd_dic[c.USER]
        check = "select * from switches where switch_id == " + switch + ";"
        a = cursor.execute(check)
        data = a.fetchall()
        #This is a valid switch id
        if len(data) > 0:
            response_dic[c.SWITCH_ID] = switch
            response_dic[c.CMD] = cmd_dic[c.CMD]
            unique = "select * from map where switch_id == " + switch + " and user_id == " + user + ";"
            results = cursor.execute(unique).fetchall()
            #There is a map from switch to user so remove it
            if len(results) > 0:
                cursor.execute("DELETE FROM map WHERE switch_id == "+switch+" and user_id == "+user+";")
                conn.commit()
                response_dic[c.RSP] = c.REMOVE_MSGS[1]
            # there is no (switch, id) pair in map, so tell them to add it before they can remove it
            else:
                response_dic[c.RSP] = c.REMOVE_MSGS[0]
        #The supplied switch id is not a valid switch id
        else:
            response_dic = None
    cursor.close()
    conn.close()
    return response_dic

def process_status(cmd_dic, platform, conn, cursor):
    response_dic = {}
    args = cmd_dic[c.ARGS]
    #This command must have at elast 1 argument
    if len(args) == 0:
        response_dic = None
    else:
        switch = args[0]
        user = cmd_dic[c.USER]
        check = "select * from switches where switch_id == " + switch + ";"
        a = cursor.execute(check)
        data = a.fetchall()
        #This is a valid switch id
        if len(data) > 0:
            response_dic[c.CMD] = cmd_dic[c.CMD]
            unique = "select * from map where switch_id == " + switch + " and user_id == " + user + ";"
            results = cursor.execute(unique).fetchall()
            #The user is following it so tell them the status
            if len(results) > 0:
                state = cursor.execute("SELECT state FROM switches WHERE switch_id == "+switch+";").fetchall()[0][0]
                conn.commit()
                response_dic[c.SWITCH_ID] = switch
                response_dic[c.RSP] = c.STATUS_MSGS[0]
                response_dic[c.SWITCH_STATUS] = str(state)
            #there is no (switch, id) pair in map, so tell them to add it before they can get the status of it
            else:
                response_dic[c.RSP] = c.STATUS_MSGS[1]
        #The supplied switch id is not a valid switch id
        else:
            response_dic = None
    cursor.close()
    conn.close()
    return response_dic

def process_list(cmd_dic, platform, conn, cursor):
    all_switches = []
    rsp_dic = {}
    user = cmd_dic[c.USER]
    data = cursor.execute("SELECT switch_id FROM map WHERE user_id == "+user+";").fetchall()
    for d in data:
        all_switches.append(d[0])
    rsp_dic[c.SWITCH_ID] = all_switches
    rsp_dic[c.CMD] = cmd_dic[c.CMD]
    rsp_dic[c.RSP] = c.LIST_MSGS[0]

    cursor.close()
    conn.close()
    return rsp_dic

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
            validate_user(cmd_dic[c.USER], conn, cursor, c.TEXT_FLAG)
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
            if sanitize(commands):
                resp_dic = process_command(commands) if commands is not None else None
                response = parser.build_response(user, resp_dic)
                s.send_response(200)
                respond_to_user_twilio(s, response)
            else:
                m.send_message(user, "Fuck off")



if __name__ == "__main__":
    sys.stderr = open("log.txt", "a+")
    accept_command()
