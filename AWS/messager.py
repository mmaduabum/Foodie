from twilio.rest import TwilioRestClient 
import secret_tokens as tokens 


def send_message(num="+16464630213", msg="msg not specified"):
    # put your own credentials here 
    client = TwilioRestClient(tokens.ACCOUNT_SID, tokens.AUTH_TOKEN) 
    client.messages.create(to=num, from_="+16508351609", body=msg) 
