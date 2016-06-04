import sh
from twilio.rest import TwilioRestClient
import sys
import messager
import sqlite3

sqlite_file = 'monica.db'
FROM = "'From'"
MSG = "'Body'"
SPOOKY_INDEX = 4
US = "+16508351609"
BEAKS = "+16464630213"
subscriber = BEAKS
subscribed = False
port = "80"

def crash():
    sys.exit()

conn = sqlite3.connect(sqlite_file)
c = conn.cursor()

def reply_to_sender(dic):
    msg = dic[MSG].replace("+", " ")
    sender = dic[FROM][SPOOKY_INDEX:]
    try:
        sender_number = sender[1:][:-1]
        c.execute("select u_name from user_map where user_id == " + sender_number + ";")
        conn.commit()
        sender_name = c.fetchone()[0]
    except:
        sender_name = ""
        c.execute("INSERT OR IGNORE INTO user_map ('user_id', 'u_name') VALUES (sender_number, sender_name)")
    response = "Hello " + sender_name + "! We received your message."
    # if sender_name == "":
    #     messager.send_message(sender, "If you would like to set your name, reply with: set name [your name]")
    messager.send_message(sender, response)

def get_name(dic):
    sender = dic[FROM][SPOOKY_INDEX:]
    sender_name = ""
    try:
        sender_number = sender[1:][:-1]
        c.execute("select u_name from user_map where user_id == " + sender_number + ";")
        conn.commit()
        sender_name = c.fetchone()[0]
    except:
        sender_name = ""
        c.execute("INSERT OR IGNORE INTO user_map ('user_id', 'u_name') VALUES (sender_number, sender_name)")
    response = "Hello " + sender_name + "! We received your message."
    if sender_name == "":
        messager.send_message(sender, "If you would like to set your name, reply with: set name [your name]")
    return sender_name


def handle_message(dic):
    global subscriber
    global subscribed
    msg = dic[MSG].replace("+", " ").lower()
    print msg
    sender = dic[FROM][SPOOKY_INDEX:]
    if "follow" in msg and "unfollow" not in msg:
        if subscribed:
            if sender == subscriber: messager.send_message(sender, "you are already following this device\nThis is a new line\n. THis too!")
            else: messager.send_message(sender,"Sorry, this device is currently locked")
        else:
            subscribed = True
            subscriber = sender
            messager.send_message(sender, "You are now following your device! To unfollow, reply 'unfollow'")

    elif "unfollow" in msg:
        if subscribed and sender == subscriber:
            subscribed = False
            subscriber = BEAKS
            messager.send_message(sender, "You have unfollowd this device. To refollow, reply 'follow'")
        else:
            messager.send_message(sender, "You are not following a device. To follow, reply 'follow'")

    else:
        messager.send_message(sender, "Hey there! Unfortunately, we don't recognize your request. To follow to a device, reply 'follow'")

# gets the text message content from the HTTP request
def parse_Twilio_response(incoming_message):
    #couldnt find a lib to parse the http data. This function makes it into a dictionary
    list_of_fields = incoming_message.replace('&', "','").replace("=", "':'").split(',')
    dic = {}
    for field in list_of_fields:
        p = field.split(':')
        dic[p[0]] = p[1]
    handle_message(dic)

def ram():
    #listen on port 80 in loop. probably a better way to do this
    while True:
        try:
            incoming_message = str(sh.nc('-l', '-w', '1', port))
            if "Twilio" not in incoming_message:
                msg_start = incoming_message.index("RAM") + 3
                response = incoming_message[msg_start:]
                messager.send_message(subscriber, msg=response)
            else:
                parse_Twilio_response(incoming_message)
        except Exception as e:
            f = open('crashes.txt', 'a+')
            f.write(str(e))
            f.write('\n')

def main():
    subscribed = False
    subscriber = BEAKS
    ram()

main()
