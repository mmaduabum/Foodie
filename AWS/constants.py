DB = 'monica.db'
FROM = "From"
MSG = "Body"
SPOOKY_INDEX = 4
US = "+16508351609"
BEAKS = "+16464630213"
HOST_NAME = ""
USER_PORT_NUMBER = 80
HUB_PORT_NUMBER = 3758
#FB_PORT_NUMBER = 3759
#FB_VERIFY_TOKEN = emOXsW5llap4VJW6c1Ke
TWILIO_SIGNATURE = "x-twilio-signature"
HUB_SIGNATURE = "x-hub-signature"
CMD = "command"
USER = "user"
RSP = "response"
SWITCH_ID = "switch"
SWITCH_NAME = "name"
SWITCH_STATUS = "status"
FOLLOW_TIME = "kunle"
VALID_CMDS = ["follow", "unfollow", "add", "remove", "status", "list", "setname", "setdefault"]
ARGS = "arguments"
DEFAULT_ERROR_MESSAGE = "Sorry, there was an error in your command."
FOLLOW_MSGS = ["You are now following switch ", "You are already following switch ", "You must add a switch to your switch list before following"]
UNFOLLOW_MSGS = ["You are not following switch ", "You are no longer following switch ", "You must first add this switch to your switch list: "]
ADD_MSGS = ["You have added the following switch to your switch list: ", "This switch is already in your list: "]
REMOVE_MSGS = ["You must first add this switch to your switch list before removing it: ", "You have removed the following switch from your switch list: "]
STATUS_MSGS = ["Currently your device, ", "You must first add this switch to your switch list before using the status command"]
LIST_MSGS = ["Your switch list is: "]
SETNAME_MSGS = []
SETDEF_MSGS = []
DEFAULT_SWITCH = 1
DEFAULT_TIME = 10
TEXT_FLAG = 1
