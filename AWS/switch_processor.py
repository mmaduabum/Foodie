import sh
from twilio.rest import TwilioRestClient
import sys
import messager
import sqlite3
import constants as c
import json
import time
import BaseHTTPServer
from time_utils import timestamp_to_seconds


"""update the database on state changes for any switches that
have changed state or any user's whose subscribtion has ended"""
def update_subscriptions(conn,cursor):
    current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
    subs_check = "select user_id, switch_id, sub_timeout from map where sub_timeout is not null;"
    subs = cursor.execute(subs_check)
    for sub in subs:
        user = str(sub[0])
        switch = str(sub[1])
        end_time = sub[2]
        #check datatime
        end = timestamp_to_seconds(end_time)
        now = timestamp_to_seconds(current_time)
        if now > end:
            update_map = 'update map set fetty_flag = 0, sub_timeout = null where switch_id == ' + switch +" and user_id == " + user  + ';'
            cursor.execute(update_map)
            conn.commit()


"""Listen on port 3658 for incoming status from the Pi"""
def accept_command():
    server_class = BaseHTTPServer.HTTPServer
    parrot = server_class((c.HOST_NAME, c.HUB_PORT_NUMBER), UserHandler)
    parrot.serve_forever()
    parrot.server_close()

def notify_user(u_id,medium,state, switch_id):
	msg = "Your switch, " + switch_id
	if (int(state) == 1):
	    msg += " is now on"
	else:
	    msg += " is now off"
	if (int(medium) == c.TEXT_FLAG):
	    messager.send_message(u_id, msg)

def process_switch(switch_id,state, conn, cursor):
    switch_id = str(switch_id)
    state = str(state)
    check = "select * from switches where switch_id == " + switch_id + ";"
    a = cursor.execute(check)
    data = a.fetchall()
    #This is a valid switch id
    if len(data) > 0:
    	state_check = "select state from switches where switch_id == " + switch_id + ";"
        a = cursor.execute(state_check)
        cur_state = a.fetchall()[0][0]
        #This is a valid switch id
        if cur_state != state:
            # get all users following that switch
            users_check = "select * from map where switch_id == " + switch_id + " and fetty_flag == 1;" 
            users = cursor.execute(users_check).fetchall()
            for u in users:
                u_id = str(u[1])
                tmstp = u[3]
                medium_check = "select platform_id from users where user_id == " + u_id + ";" 
                medium = cursor.execute(medium_check).fetchall()[0][0]
                notify_user(u_id,medium,state, switch_id)
                if (tmstp == None):
                    update_map = 'update map set fetty_flag = 0 where switch_id == ' + switch_id +" and user_id == " + u_id + ';'
                    cursor.execute(update_map)
                    conn.commit

        update = 'update switches set state = '+state+' where switch_id == ' + switch_id + ';'
        cursor.execute(update)
        conn.commit()




class UserHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_HEAD(s):
        s.send_response(200)
        pass

    #handle get request
    def do_GET(s):
        s.send_response(200)
        pass

    #handle Twilio Post
    def do_POST(s):
        conn = sqlite3.connect(c.DB)
        cursor = conn.cursor()
        update_subscriptions(conn,cursor)
        http_in = s.rfile.read(int(s.headers.getheader('Content-Length'))) #json
        hub_dic = json.loads(http_in)
        for switch_id in hub_dic:
            process_switch(switch_id, hub_dic[switch_id], conn, cursor)
        cursor.close()
        conn.close()

if __name__ == "__main__":
    sys.stderr = open("otherlog.txt", "a+")
    accept_command()

