import sh
from twilio.rest import TwilioRestClient
import sys
import messager
import sqlite3
import urllib
import constants as c


def twilio_to_dic(incoming_message):
    list_of_fields = incoming_message.split('&')
    dic = {}
    for field in list_of_fields:
        p = field.split('=')
        dic[p[0]] = urllib.unquote(p[1].replace("+", " "))
    return dic


def get_command(sender, msg):
    commands = {}
    commands[c.USER] = sender
    words = msg.split()
    command = words[0]
    if command not in c.VALID_CMDS:
        return None
    commands[c.CMD] = command
    commands[c.ARGS] = words[1:] 

    return commands


def follow_response(dic):
    response = dic[c.RSP]
    if c.SWITCH_TIME in dic and c.SWITCH_ID in dic:
        response += dic[c.SWITCH_ID] + " for " + dic[c.SWITCH_TIME]

    return response

def unfollow_response(dic):
    response = dic[c.RSP]
	if c.SWITCH_ID in dic:
		response += dic[c.SWITCH_ID]

def add_response(dic):
    response = dic[c.RSP]
	response += dic[str(c.SWITCH_ID]

def remove_response(dic):
    pass

def status_response(dic):
    pass

def list_response(dic):
    pass

def setname_response(dic):
    pass

def setdefault_response(dic):
    pass


def build_response(sender, response_dic):
    if response_dic is None:
        return c.DEFAULT_ERROR_MESSAGE
    response = ""
    command = response_dic[c.CMD]
    
    return response 
