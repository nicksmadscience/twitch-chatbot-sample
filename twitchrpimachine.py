import sys
import time
import serial
import websocket
import thread
import json
import pprint
import traceback

with open("secrets.json") as secrets_file:
    secrets = json.loads(secrets_file.read())


# {"type":"MESSAGE","data":{"topic":"channel-bits-events-v1.105293178","message":"{\"data\":{\"user_name\":\"theotherlonestar\",\"channel_name\":\"nicksmadscience\",\"user_id\":\"85403751\",\"channel_id\":\"105293178\",\"time\":\"2020-07-08T17:59:58.014403227Z\",\"chat_message\":\"Cheer1\",\"bits_used\":1,\"total_bits_used\":1,\"context\":\"cheer\",\"badge_entitlement\":{\"new_version\":0,\"previous_version\":0},\"badge_tier_entitlement\":{\"Badge\":{\"new_version\":0,\"previous_version\":0},\"Emoticons\":null}},\"version\":\"1.0\",\"message_type\":\"bits_event\",\"message_id\":\"da62dd7c-957a-5433-b14d-42fb0773e45b\"}"}}

# print ("id: " + secrets["id"])
# print ("key: " + secrets["key"])



# you will need to go into /dev and find the relay card's serial port
relayCardSerial = '/dev/ttyACM0'

#Open port for communication    
serPort = serial.Serial(relayCardSerial, 9600, timeout=1)


serPort.write("gpio set 5\r") # turn off the yellow strobe



# ws = create_c onnection("wss://pubsub-edge.twitch.tv")

# for i in range(0, 10):
# 	serPort.write("gpio writeall ffffffff\r")
# 	time.sleep(0.5)
# 	serPort.write("gpio writeall 00000000\r")
# 	time.sleep(0.5)



# print "Receiving..."
# result =  ws.recv()
# print "Received '%s'" % result
# ws.close()


# Request from client to server
listenToBits = {
  "type": "LISTEN",
  "data": {
    "topics": ["channel-bits-events-v1." + secrets["id"]],
    "auth_token": secrets["key"]
  }
}


listenToPoints = {
  "type": "LISTEN",
  "data": {
    "topics": ["channel-points-channel-v1." + secrets["id"]],
    "auth_token": secrets["key"]
  }
}


# sampleBitMessage = """{u'data': {u'topic': u'channel-bits-events-v1.105293178', u'message': u'{"data":{"user_name":"theotherlonestar","channel_name":"nicksmadscience","user_id":"85403751","channel_id":"105293178","time":"2020-07-08T18:19:08.675974326Z","chat_message":"Cheer1","bits_used":1,"total_bits_used":2,"context":"cheer","badge_entitlement":{"new_version":0,"previous_version":0},"badge_tier_entitlement":{"Badge":{"new_version":0,"previous_version":0},"Emoticons":null}},"version":"1.0","message_type":"bits_event","message_id":"00dff0b8-2c17-5075-931a-ff6ecded4bf4"}'}, u'type': u'MESSAGE'}"""

# message_post_json = json.loads(sampleBitMessage)
# print message_post_json["type"]
# print message_post_json["type"]["data"]
# print message_post_json["type"]["data"]["topic"]

def on_message(ws, message):
    global serPort

    if message.find("channel-bits-events") != -1:
        print "OH HECK IT'S BIT O'CLOCK"
        serPort.write("gpio clear 5\r") # turn on the yellow strobe
        time.sleep(10)
        serPort.write("gpio set 5\r") # turn off the yellow strobe

    # message_post_json = json.loads(message) 
    # print message_post_json

    # try:
    #     if message_post_json["type"] == "MESSAGE":
    #         print "type is message"
    #         if message_post_json["type"]["data"]["topic"] == "channel-bits-events-v1.105293178":
    #             print "OH HECK IT'S BIT O'CLOCK"
    #             serPort.write("gpio clear 5\r") # turn on the yellow strobe
    #             time.sleep(10)
    #             serPort.write("gpio set 5\r") # turn off the yellow strobe
    # except:
    #     traceback.print_exc()

        

def on_error(ws, error):
    pprint.pprint(json.loads(error))

def on_close(ws):
    print "### closed ###"

def on_open(ws):
    def run(*args):
        ws.send(json.dumps(listenToBits))
        ws.send(json.dumps(listenToPoints))
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


if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("wss://pubsub-edge.twitch.tv",
                                on_message = on_message,
                                on_error = on_error,
                                on_close = on_close)
    ws.on_open = on_open

    ws.run_forever()