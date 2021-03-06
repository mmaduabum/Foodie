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
    if c.FOLLOW_TIME in dic and c.SWITCH_ID in dic:
        response += str(dic[c.SWITCH_ID]) + " for " + str(dic[c.FOLLOW_TIME]) + " minutes"
    if c.FOLLOW_TIME not in dic and c.SWITCH_ID in dic:
        response += str(dic[c.SWITCH_ID])

    return response

def unfollow_response(dic):
    response = dic[c.RSP]
    if c.SWITCH_ID in dic:
	response += dic[c.SWITCH_ID]

    return response

def add_response(dic):
    response = dic[c.RSP]
    if c.SWITCH_ID in dic:
    	response += dic[c.SWITCH_ID]
    return response

def remove_response(dic):
    response = dic[c.RSP]
    if c.SWITCH_ID in dic:
        response += dic[c.SWITCH_ID]

    return response

def status_response(dic):
    response = dic[c.RSP]
    if c.SWITCH_ID and c.SWITCH_STATUS in dic:
        state = "on" if int(dic[c.SWITCH_STATUS]) == 1 else "off"
        response += dic[c.SWITCH_ID] + " is " + state
    return response   

def list_response(dic):
    response = dic[c.RSP]
    if c.SWITCH_ID in dic and c.BEAKS_FEATURE in dic and c.ihateyouguys in dic:
        fettys = dic[c.ihateyouguys]
        switches = dic[c.SWITCH_ID]
        times = dic[c.BEAKS_FEATURE]
        for switch, t, f in zip(switches, times, fettys):
            response += str(switch)
            if t is not None: response += ": following for " + str(t) + " minutes\n"
            elif int(f) == 1: response += ": following\n"
            else: response += "\n"

    return response

def setname_response(dic):
    response = dic[c.RSP]
    if c.SWITCH_ID and c.SWITCH_NAME in dic:
        response += dic[c.SWITCH_ID] + "can now be addressed as " + dic[c.SWITCH_NAME]

    return response

def setdefault_response(dic):
    response = dic[c.RSP]
    if c.SWITCH_ID in dic:
        response += str(dic[c.SWITCH_ID])
    
    return response

def help_response(dic):
    response = dic[c.RSP]
    return response


def build_response(sender, response_dic):
    if response_dic is None:
        return c.DEFAULT_ERROR_MESSAGE
    response = "Hey! We are processing your request"
    command = response_dic[c.CMD]
    parsers = [follow_response, unfollow_response, add_response, remove_response, status_response, list_response, setname_response, setdefault_response, help_response]
    for parser, cmd in zip(parsers, c.VALID_CMDS):
        if command == cmd:
            return parser(response_dic)
                
    return response 
