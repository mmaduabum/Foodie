#get text
#figure out how to know when to reply
#reply
from twilio.rest import TwilioRestClient 
 
# put your own credentials here 
ACCOUNT_SID = "AC73e950f31868a3b24506e58cbb1585d9"
AUTH_TOKEN = "e5ecf02cc2def042420962c7bb4345df"

 
client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN) 
 
client.messages.create(
    to="+19739705321", 
    from_="+16508351609", 
    body="Hey Mike! Good luck on the bar exam!", 
    media_url="http://farm2.static.flickr.com/1075/1404618563_3ed9a44a3a.jpg", 
)
