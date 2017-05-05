'''
This helper will take care of events. 

'''
from ccTalk.bus.ccTalk_Message import ccTalk_Message
from ccTalk.error_codes import ccTalk_errors
#We got a new coin. The value need to be handled
def handle_coin(coin:int, sorter:int, coin_values):
    print ("Coin:",coin,"accepted")

#We have a failure! We will send this information
def handle_error(error_code:int):
    print (ccTalk_errors[error_code])
    return ccTalk_errors[error_code]

#We have a new event. We analyse the event buffer and call the corresponding handle method
def decode_eventbuffer(handled_events:int,event_buffer):
    # We need to know how many events
    events_happened = event_buffer[0] - handled_events%256
    #As 0 is not reached we need some workaround for the turn!
    if events_happened<1:
        events_happened = 1
    events_checked = 0
    while events_checked < events_happened:
        events_checked += 1
        if event_buffer[events_checked] == 0:
            #The failure message is in part 2 of the event info
            handle_error(event_buffer[events_checked+1])
        else: handle_coin(event_buffer[events_checked], event_buffer[events_checked+1],"")
        events_checked+=1
    return events_happened