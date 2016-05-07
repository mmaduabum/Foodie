import sh
from twilio.rest import TwilioRestClient
import sys
import messager

FROM = "'From'"
MSG = "'Body'"
SPOOKY_INDEX = 4
US = "+16508351609"


def crash():
    sys.exit()

def reply_to_sender(dic):
    msg = dic[MSG].replace("+", " ")
    sender = dic[FROM][SPOOKY_INDEX:]
    response = "Thanks for your reply! you said ' " + msg + "'. see you soon!"
    messager.send_message(sender, response)


def do_stuff(reply):
    #couldnt find a lib to parse the http data. This function makes it into a dictionary
    list_of_fields = reply.replace('&', "','").replace("=", "':'").split(',')
    dic = {}
    for field in list_of_fields:
        p = field.split(':')
        dic[p[0]] = p[1]
    reply_to_sender(dic)

#listen on port 80 in loop. probably a better way to do this
errors = 0
while True:
    try:
        reply = str(sh.nc('-l', '-w', '1', '80'))
        do_stuff(reply)
    except Exception as e:
        #if errors > 100: crash()
        f = open('crashes.txt', 'a+')
        f.write(str(e))
        f.write('\n')
        errors += 1

