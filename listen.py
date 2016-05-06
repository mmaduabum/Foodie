import sh
from twilio.rest import TwilioRestClient

FROM = "'From'"
MSG = "'Body'"
SPOOKY_INDEX = 4
ACCOUNT_SID = "AC73e950f31868a3b24506e58cbb1585d9"
AUTH_TOKEN = "e5ecf02cc2def042420962c7bb4345df"
US = "+16508351609"

def reply_to_sender(dic):
    msg = dic[MSG].replace("+", " ")
    sender = dic[FROM][SPOOKY_INDEX:]
    client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)
    response = "Thanks for your reply! you said ' " + msg + "'. see you soon!"
    client.messages.create(to=sender, from_=US, body=response)


def do_stuff(reply):
    #couldnt find a lib to parse the http data. This function makes it into a dictionary
    list_of_fields = reply.replace('&', "','").replace("=", "':'").split(',')
    dic = {}
    for field in list_of_fields:
        p = field.split(':')
        dic[p[0]] = p[1]
    reply_to_sender(dic)

#listen on port 80 in loop. probably a better way to do this
while True:
    reply = str(sh.nc('-l', '-w', '1', '80'))
    do_stuff(reply)

