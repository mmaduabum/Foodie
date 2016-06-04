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


def twilio_to_dic(incoming_message):
    list_of_fields = incoming_message.replace('&', "','").replace("=", "':'").split(',')
    dic = {}
    for field in list_of_fields:
        p = field.split(':')
        dic[p[0]] = p[1].replace("+", " ")
    return dic
