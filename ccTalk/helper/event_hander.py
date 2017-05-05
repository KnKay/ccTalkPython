'''
This helper will take care of events. 

'''
from ccTalk.bus.ccTalk_Message import ccTalk_Message
from ccTalk.error_codes import ccTalk_errors
import time
import threading


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

def poll_loop(handled_events, poll_command, bus):
    while True:
        event_buffer = bus.send_bytes_request_message(poll_command)
        # We need to handle the events. This is only 0 on reset! Due to this we use the modulo
        if (handled_events % 256 != event_buffer[4]):
            handled_events += decode_eventbuffer(handled_events, ccTalk_Message.get_payload_from_bytes(event_buffer))
        time.sleep(0.04)

class poll_thread(threading.Thread):
    def __init__(self, stop_event, bus, validator_address, poll_command, handled_events:int = 1):
        threading.Thread.__init__(self)
        self.bus = bus
        self.validator = validator_address
        self.stopped = stop_event
        self.poll_command = poll_command
        self.handled_events = handled_events

    def run(self):
        while not self.stopped.wait(0.04):
            event_buffer = self.bus.send_bytes_request_message(self.poll_command)
            # We need to handle the events. This is only 0 on reset! Due to this we use the modulo
            if (self.handled_events % 256 != event_buffer[4]):
                self.handled_events += decode_eventbuffer(self.handled_events,
                                                     ccTalk_Message.get_payload_from_bytes(event_buffer))