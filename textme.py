from twilio.rest import TwilioRestClient

token = "94d182bd558d91b553d7fa3e676dbfa4"
sid = "AC645ca8ccd2983a61e0082f5eb19bcd9f"

twilioClient = TwilioRestClient(sid, token)
num = raw_input("number: ")
fr = "+18556223691"
msg = raw_input("message: ")
myMessage = twilioClient.messages.create(body = msg, from_=fr, to=num)
