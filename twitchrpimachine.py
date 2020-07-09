import sys
import time
import serial
import websocket
import thread
import json
import pprint
import traceback
from threading import Thread

with open("secrets.json") as secrets_file:
    secrets = json.loads(secrets_file.read())


# {"type":"MESSAGE","data":{"topic":"channel-bits-events-v1.105293178","message":"{\"data\":{\"user_name\":\"theotherlonestar\",\"channel_name\":\"nicksmadscience\",\"user_id\":\"85403751\",\"secrets["id"]\":\"105293178\",\"time\":\"2020-07-08T17:59:58.014403227Z\",\"chat_message\":\"Cheer1\",\"bits_used\":1,\"total_bits_used\":1,\"context\":\"cheer\",\"badge_entitlement\":{\"new_version\":0,\"previous_version\":0},\"badge_tier_entitlement\":{\"Badge\":{\"new_version\":0,\"previous_version\":0},\"Emoticons\":null}},\"version\":\"1.0\",\"message_type\":\"bits_event\",\"message_id\":\"da62dd7c-957a-5433-b14d-42fb0773e45b\"}"}}

# print ("id: " + secrets["id"])
# print ("key: " + secrets["key"])



# you will need to go into /dev and find the relay card's serial port
relayCardSerial = '/dev/ttyACM0'

#Open port for communication    
serPort = serial.Serial(relayCardSerial, 9600, timeout=1)

# SETUP
serPort.write("gpio set 5\r") # turn off the yellow strobe
serPort.write("gpio set 6\r") # turn off the green strobe





# Request from client to server
listenToEvents = {
  "type": "LISTEN",
  "data": {

    "topics": ["channel-points-channel-v1."+secrets["id"], "channel-bits-events-v2."+secrets["id"], "channel-subscribe-events-v1."+secrets["id"] ],
    "auth_token": secrets["key"]
  }
}



def on_message(ws, message):
    global serPort

    print message

    if message.find("channel-bits-events") != -1:
        print "OH HECK IT'S BITS O'CLOCK"
        serPort.write("gpio clear 5\r") # turn on the yellow strobe
        time.sleep(10)
        serPort.write("gpio set 5\r") # turn off the yellow strobe
    elif message.find("77f991d8-a75c-4273-91b6-259e25009617") != -1:
        print "OH HECK IT'S CHIME O'CLOCK"
        serPort.write("gpio clear 0\r") # turn on the chime
        time.sleep(0.5)
        serPort.write("gpio set 0\r") # turn off the chime
    elif message.find("6dcaa344-0bae-40f8-b2ff-baa3ace98cd3") != -1:
        print "OH HECK IT'S FOG O'CLOCK"
        serPort.write("gpio clear 6\r") # turn on the fog machine
        time.sleep(5)
        serPort.write("gpio set 6\r") # turn off the fog machine


        

def on_error(ws, error):
    pprint.pprint(json.loads(error))

def on_close(ws):
    print "### closed ###"

def on_open(ws):
    def run(*args):
        ws.send(json.dumps(listenToEvents))
        while True:
            try:
                time.sleep(1)
            except KeyboardInterrupt:
                ws.close()
        # for i in range(30000):
            # time.sleep(1)
            # ws.send("Hello %d" % i)
        # time.sleep(1)
        # ws.close()
        print "thread terminating..."
    thread.start_new_thread(run, ())



ws = websocket.WebSocketApp("wss://pubsub-edge.twitch.tv",
                                on_message = on_message,
                                on_error = on_error,
                                on_close = on_close)


def pingManager():
    global ws

    while True:
        time.sleep(4.0 * 60.0)
        ws.send("""{"type": "PING"}""")
        












# if __name__ == "__main__":


websocket.enableTrace(True)

ws.on_open = on_open

pingManagerThread = Thread(target=pingManager)
pingManagerThread.daemon = True
pingManagerThread.start()

ws.run_forever()