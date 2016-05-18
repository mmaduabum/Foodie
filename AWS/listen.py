import sh
from twilio.rest import TwilioRestClient
import sys
import messager
import sqlite3

FROM = "'From'"
MSG = "'Body'"
SPOOKY_INDEX = 4
US = "+16508351609"


def crash():
    sys.exit()


def reply_to_sender(dic):
    msg = dic[MSG].replace("+", " ")
    sender = dic[FROM][SPOOKY_INDEX:]
    try:
        sender_number = sender[1:][:-1]
        conn = sqlite3.connect('monica.db')
        c = conn.cursor()
        c.execute("select u_name from user_map where user_id == " + sender_number + ";")
        conn.commit()
        sender_name = c.fetchone()[0]
    except:
        sender_name = "Wayne"
    response = "Hello " + sender_name + "! We received your message."
    messager.send_message(sender, response)


# gets the text message content from the HTTP request
def handle_Twilio_response(incoming_message):
    #couldnt find a lib to parse the http data. This function makes it into a dictionary
    list_of_fields = incoming_message.replace('&', "','").replace("=", "':'").split(',')
    dic = {}
    for field in list_of_fields:
        p = field.split(':')
        dic[p[0]] = p[1]
    reply_to_sender(dic)

#listen on port 80 in loop. probably a better way to do this
errors = 0
while True:
    try:
        incoming_message = str(sh.nc('-l', '-w', '1', '80'))
        if "Twilio" not in incoming_message:
            msg_start = incoming_message.index("RAM") + 3
            response = incoming_message[msg_start:]
            messager.send_message(msg=response)
        else:
            handle_Twilio_response(incoming_message)
    except Exception as e:
        #if errors > 100: crash()
        f = open('crashes.txt', 'a+')
        f.write(str(e))
        f.write('\n')
        errors += 1

