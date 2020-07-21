

# TODO: do I seriously have to subscribe to webhooks on top of IRC and PubSub?  I'll do it if I have to I guess

# TODO: consider setting custom events up in a configuration file
# event type (chat string, follow, sub, etc.)
# thing you want to happen, which I guess could be code?  








import sys
import time
import serial
import websocket
import thread
import json
import pprint
import traceback
import requests
from threading import Thread
import string
from parse import *
from parse import compile
import random

import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web
import socket



# constant-y stuff


with open("secrets.json") as secrets_file:
    secrets = json.loads(secrets_file.read())


relay_raidlight   = 0
relay_raidpulse   = 1
relay_redlight    = 2
relay_yellowlight = 3
relay_bluelight   = 4
relay_chime       = 5
relay_fogmachine  = 6

led_raid     = 8
led_bits     = 9
led_sub      = 10
led_host     = 11
led_points   = 12
led_follow   = 13
led_onair    = 14




# initial setup


# irc twitch interface
HOST="irc.chat.twitch.tv"
PORT=6667
readbuffer=""

with open("secrets.json") as secrets_file:
    secrets = json.loads(secrets_file.read())

s=socket.socket( )
s.connect((HOST, PORT))
print "connected"
s.send("PASS " + secrets["irc_oauth"] + "\r\n")
s.send("NICK nicksmadscience\r\n")
s.send("JOIN #nicksmadscience\r\n")









clients = [] # https://stackoverflow.com/questions/11695375/tornado-identify-track-connections-of-websockets

class WSHandler(tornado.websocket.WebSocketHandler):
    global clients

    def open(self):
        print 'new connection'
        clients.append(self)
        print clients

      
    def on_message(self, message):  # when the script receives a message from the web browser
        print 'message received:  %s' % message

        if message == "sample message":
            # do sample thing
            pass

            for client in clients:
                client.write_message(json.dumps({"messagetype": "sample response", "animation": "explode"}))


        elif message[0:7] == "generic":
            for client in clients:
                client.write_message(json.dumps({"messagetype": "generic", "message": message[8:]}))


        # elements = ("/" + message).split('/') # to maintain ajax compatibility

        # for httpRequest, httpHandler in httpRequests.iteritems():
        #     if elements[1] == httpRequest:
        #         contentType, response = httpHandler(elements)
        #         print response

 
    def on_close(self):
        print 'connection closed'
        clients.remove(self)
 
    def check_origin(self, origin):
        return True









# Tornado web application for Twitch IRC / chat interface
application = tornado.web.Application([
    (r'/ws', WSHandler),
])

 
def socket():
    print "*** socket ***"
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(6789)
    # myIP = socket.gethostbyname(socket.gethostname())
    # print '*** Websocket Server Started at %s***' % myIP
    tornado.ioloop.IOLoop.instance().start()

socketThread = Thread(target=socket)
socketThread.daemon = True
socketThread.start()






# sample messages

# p = compile(":{}!{}@{}.tmi.twitch.tv PRIVMSG #{} :{}")
# ":nicksmadscience!nicksmadscience@nicksmadscience.tmi.twitch.tv PRIVMSG #nicksmadscience :fwewewef"

# {"type":"MESSAGE","data":{"topic":"channel-bits-events-v1.105293178","message":"{\"data\":{\"user_name\":\"theotherlonestar\",\"channel_name\":\"nicksmadscience\",\"user_id\":\"85403751\",\"secrets["id"]\":\"105293178\",\"time\":\"2020-07-08T17:59:58.014403227Z\",\"chat_message\":\"Cheer1\",\"bits_used\":1,\"total_bits_used\":1,\"context\":\"cheer\",\"badge_entitlement\":{\"new_version\":0,\"previous_version\":0},\"badge_tier_entitlement\":{\"Badge\":{\"new_version\":0,\"previous_version\":0},\"Emoticons\":null}},\"version\":\"1.0\",\"message_type\":\"bits_event\",\"message_id\":\"da62dd7c-957a-5433-b14d-42fb0773e45b\"}"}}



# you will need to go into /dev and find the relay card's serial port
relayCardSerial = '/dev/ttyACM0'

#Open port for communication    
serPort = serial.Serial(relayCardSerial, 9600, timeout=1)



# TODO: existential crisis re: whether I should hard-code this for this specific project or make it
# nigh-infinitely expandable by way of a configuration file, and if it's the latter, at what point
# on the so-far-nonexistent project roadmap should it happen?

# TODO: config file

# def setGPIOsToDefaults():
#     for i in range(0, 8):  



# Set GPIOs to defaults


serPort.write("gpio set 0\r") # turn off the raid strobe
serPort.write("gpio set 2\r") # turn off the red strobe
serPort.write("gpio set 3\r") # turn off the yellow strobe
serPort.write("gpio set 6\r") # turn off the fog machine





# Request from client to server
listenToEvents = {
  "type": "LISTEN",
  "data": {

    "topics": ["channel-points-channel-v1."+secrets["id"], "channel-bits-events-v2."+secrets["id"], "channel-subscribe-events-v1."+secrets["id"] ],
    "auth_token": secrets["key"]
  }
}





def turnOnRelay(_relay):
    serPort.write("gpio clear " + str(_relay) + "\r")

def turnOffRelay(_relay):
    serPort.write("gpio set " + str(_relay) + "\r")

def turnOnLED(_relay):
    serPort.write("gpio set " + str(_relay) + "\r")

def turnOffLED(_relay):
    serPort.write("gpio clear " + str(_relay) + "\r")





def on_message(ws, message):
    global serPort

    print message

    if message.find("channel-bits-events") != -1:
        print "OH HECK IT'S BITS O'CLOCK"

        if message.find(string.lower("Cheer100")) != -1:
            requests.get("http://10.0.0.3/attention")
        elif message.find(string.lower("Cheer101")) != -1:
            requests.get("http://10.0.0.5/attention")


        turnOnRelay(relay_yellowlight)
        turnOnLED(led_bits)
        time.sleep(10)
        turnOffRelay(relay_yellowlight)
        turnOffLED(led_bits)

    elif message.find("c910a800-ecb3-4917-bab1-e47399dfd2d2") != -1:
        print "OH HECK IT'S YELLOW STROBE TEST O'CLOCK"
        turnOnRelay(relay_yellowlight)
        time.sleep(10)
        turnOffRelay(relay_yellowlight)

    elif message.find("77f991d8-a75c-4273-91b6-259e25009617") != -1:
        print "OH HECK IT'S CHIME O'CLOCK"
        turnOnRelay(relay_chime)
        time.sleep(0.5)
        turnOffRelay(relay_chime)

    elif message.find("6dcaa344-0bae-40f8-b2ff-baa3ace98cd3") != -1:
        print "OH HECK IT'S FOG O'CLOCK"
        turnOnRelay(relay_fogmachine)
        time.sleep(5)
        turnOffRelay(relay_fogmachine)

    elif message.find("723006a2-3caf-4a6a-9aff-3dbe94231d41") != -1:
        print "OH HECK IT'S RED LIGHT TEST O'CLOCK"
        turnOnRelay(relay_redlight)
        time.sleep(5)
        turnOffRelay(relay_redlight)

    elif message.find("channel-subscribe-events") != -1:
        print "OH HECK IT'S SUBSCRIBER O'CLOCK"
        turnOnRelay(relay_redlight)
        turnOnLED(led_raid)
        turnOnRelay(relay_fogmachine)
        time.sleep(5)
        turnOffRelay(relay_redlight)
        turnOffLED(led_raid)
        turnOffRelay(relay_fogmachine)

    elif message.find("1f1bc054-a48f-418b-b148-bfe14580bb4b") != -1:
        print "OH HECK IT'S YELLOW BUTTON A O'CLOCK"
        requests.get("http://10.0.0.3/attention")

    elif message.find("a015be4f-c7ff-4a27-b519-414a4afc02a1") != -1:
        print "OH HECK IT'S RED BUTTON B O'CLOCK"
        requests.get("http://10.0.0.5/attention")

    # TODO: implement raid once I can do chat


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
    """Sends a PING every four minutes so that we don't get the boot.
    (Requirement is to send a PING no less than once per five minutes.)"""

    global ws # TODO: should this be global?  I hear this is not best practice

    while True:
        time.sleep(4.0 * 60.0)
        ws.send("""{"type": "PING"}""")
        
pingManagerThread = Thread(target=pingManager)
pingManagerThread.daemon = True
pingManagerThread.start()



# if __name__ == "__main__":  # TODO: This kinda broke things and I don't yet fully understand why?



# start websocket stuff

websocket.enableTrace(True)

ws.on_open = on_open


def wsRunForever():
    """Literally just runs run_forever, but asynchronously (in a thread)."""
    ws.run_forever()

wsRunForeverThread = Thread(target=wsRunForever)  # TODO: this could be a function
wsRunForeverThread.daemon = True
wsRunForeverThread.start()





p = compile(":{}!{}@{}.tmi.twitch.tv PRIVMSG #{} :{}")
# ":nicksmadscience!nicksmadscience@nicksmadscience.tmi.twitch.tv PRIVMSG #nicksmadscience :fwewewef"


def generateNewColor():
    """Much like Twitch chat itself, every username gets its own random color.  This generates said random color"""
    return "rgb(%d, %d, %d)" % (int(random.random() * 128 + 128), int(random.random() * 128 + 128), int(random.random() * 128 + 128))

usersInChat = {}     # list of all unique users in chat
chatLineNumber = 0   # Increments by one each time a new chat line comes in

go = True
while go:
    try:
        recv = s.recv(1024)

        readbuffer = readbuffer + recv
        temp       = readbuffer.split(b"\n")
        readbuffer = temp.pop()

        for line in temp:
            chatLineNumber += 1
            line = line.rstrip()

            print(line)

            if line.find(b"PING") != -1:  # TODO: should be the beginning of the string, not just a search
                s.send(b"PONG %s\r\n" % line[1])
                print("pong")

            elif line.find(b"PRIVMSG") != -1: # TODO: same thing
                messageDeconstructed = p.parse(line)

                try:
                    username = messageDeconstructed[0]
                except:
                    traceback.print_exc()
                    message = traceback.format_exc()

                message = messageDeconstructed[4]


                # commented out until I need chat functionality

                # if username not in usersInChat:
                #     color = generateNewColor()
                #     usersInChat[username] = {"color": color}
                # else:
                #     color = usersInChat[username]["color"]

                # line = json.dumps({"messagetype": "chat", "color": color, "username": username, "message": message, "messageWithUsernameIfAny": username + ": " + message, "messageType": "privmsg", "chatLineNumber": chatLineNumber})#"<p class='chatline' style='color: %s'>%s: %s</p>" % (color, username, message)

                print (message)

                if message[0:5].lower() == "cheer" or message[0:5].lower() == "corgo" or message[0:5] == "Butts":
                    print ("OMFG CHEER")


                elif message.find("is raiding") != -1:
                    print ("OMFG RAIDZ")
                    turnOnRelay(relay_raidlight)
                    turnOnRelay(relay_fogmachine)
                    requests.get("http://10.0.0.44:8081/preset/totd")
                    time.sleep(10)
                    turnOffRelay(relay_fogmachine)
                    time.sleep(10)
                    turnOffRelay(relay_raidlight)
                    requests.get("http://10.0.0.44:8081/preset/nms")


            # else:
                # line = json.dumps({"messagetype": "chat", "color": "gray", "username": "[none]", "message": line, "messageWithUsernameIfAny": line, "messageType": "info", "chatLineNumber": chatLineNumber})

            
            # print (line)


            # with open("chatlog.txt", "ab") as chatlog_file:
                # chatlog_file.write(line + "\n")

    except KeyboardInterrupt:
        go = False
    except:
        traceback.print_exc()

    time.sleep(0.1)






