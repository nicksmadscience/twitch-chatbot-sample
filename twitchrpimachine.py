

# TODO: do I seriously have to subscribe to webhooks on top of IRC and PubSub?  I'll do it if I have to I guess

# TODO: consider setting custom events up in a configuration file
# event type (chat string, follow, sub, etc.)
# thing you want to happen, which I guess could be code?  


# TODO: websocket for interfacing with outside stuff, e.g. devops-style git push event?
#          TO CLARIFY: make an overlay or IRL event happen when I "git push"


# TODO: flashy thing for new subscriber.  I think I need to generate a new key combo for this one
#          TO CLARIFY: by what means should I be notified of a new subscriber?



# TODO: LOG EVERYTHING
#            - that arrives via IRC
#            - that arrives via PubSub
#            - that arrives via Webhooks



# TODO: stick to just PubSub?  undocumented event types might exist
#            e.g. Hype Train https://pastebin.com/WLK1frBZ



# ALL EVENTS I WANT TO TRACK
# New follower
# New subscription
# Raid
# Bits
# Chanel points
# Hype train


# CHANNELS BY WHICH STUFF COMES IN

# Webhooks
    # New Followers (possibly only route?  would like to avoid webhooks if i'd just need them for follows and there's some undocumented other way)

# PubSub
    # Points
    # Bits
    # Subs
    # Hype train

# Chat / IRC
    # Raid



# TODO: log everything!



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
import datetime
import urllib2
from oscpy.client import OSCClient

# websockets
import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web
import socket

from threading import Thread
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
PORT_NUMBER = 8081

from twitchrpimachine_countdown import countdownClass



# constant-y stuff

with open("secrets.json") as secrets_file:
    secrets = json.loads(secrets_file.read())


relay_raidlight   = 0
relay_raidpulse   = 1
relay_redlight    = 2
relay_yellowlight = 3
relay_bluelight   = 5
relay_chime       = 4
relay_fogmachine  = 6

led_raid     = 8
led_bits     = 9
led_sub      = 10
led_host     = 11
led_points   = 12
led_follow   = 13
led_onair    = 14



# TODO: eventually what I wanna do is keep a record of everyone who triggered each event
# (at least with the competing dog buttons) and how many times they did each thing

count = {"red": 0, "blue": 0, "redteam": "ANGULAR", "blueteam": "REACT", "period": "1"}
# countdown = {"active": False, "startTime": 0, "endTime": 0}

countdown = countdownClass("none", 0, 0) # set initial timer to one that immediately expires


# awesomeBunchOfCountdowns = {"omfg": countdownClass("butts", 2, 2)}



# TODO: doesn't need to be just 'count'!  System-wide status could be kept in a single dict


# Keep the count persistent between sessions
with open("count.json", "rb") as count_file:
    count = json.loads(count_file.read())

print (count)







######## HACKERY ########

sevensegment = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)




######## IRC / CHAT ########


HOST="irc.chat.twitch.tv"
PORT=6667
readbuffer=""

with open("secrets.json") as secrets_file:
    secrets = json.loads(secrets_file.read())

s=socket.socket( )
s.connect((HOST, PORT))
print ("connected")
s.send("PASS " + secrets["irc_oauth"] + "\r\n")
s.send("NICK nicksmadscience\r\n")
s.send("JOIN #nicksmadscience\r\n")




####### OSC #######


xr18 = OSCClient("10.0.0.99", 10024)




def isRaiding(raiderName = "(unknown)"):
    try:
        turnOnRelay(relay_raidlight)
        print ("a")
    except:
        traceback.print_exc()

    try:
        turnOnRelay(relay_fogmachine)
        print ("b")
    except:
        traceback.print_exc()

    try:
        requests.get("http://10.0.0.44:8081/preset/totd")
        print ("c")
    except:
        traceback.print_exc()

    try:
        requests.get("http://10.0.0.220:8081/titleplay/nms-raid-alert.html/{\"raidernameHandler\": \"" + str(raiderName) + "\"}/theripper")
        print ("d")
    except:
        traceback.print_exc()

    try:
        requests.get("http://10.0.0.220:8081/videoplay/webm/alert-raid.webm/noloop/theripper")
        print ("e")
    except:
        traceback.print_exc()

    try:
        requests.get("http://10.0.0.220:8081/videoplay/webm/alert-raid-fullscreen.webm/noloop/nc1in")
        print ("f")
    except:
        traceback.print_exc()

    try:
        time.sleep(5)
        print ("g")
    except:
        traceback.print_exc()

    turnOffRelay(relay_fogmachine)
    try:
        print ("h")
        time.sleep(10)
    except:
        traceback.print_exc()

    try:
        print ("i")
        turnOffRelay(relay_raidlight)
    except:
        traceback.print_exc()

    try:
        print ("j")
        requests.get("http://10.0.0.44:8081/preset/nms")
    except:
        traceback.print_exc()

    print ("k")





####### WEBSERVER #######


# PROCESS FOR ADDING NEW HTTP GET REQUESTS
# 1. add a requestHandler_xxx function, e.g. def requestHandler_butts(_get): (where _get) is the full HTTP GET request text
# 2. function should return 1. the ContentType (e.g. "text/plain"), 2. the response text
# 3. add said function to httpRequests, e.g. ('butts': requestHandler_butts)

def requestHandler_index(_get):
    return "text/plain", "TWITCH RPI MACHINE GO"

def requestHandler_count(_get):
    global count
    return "text/plain", json.dumps(count)

def requestHandler_startCountdown(_get):
    global countdown # TODO: once again not sure how to avoid a global

    name    = _get[2]
    minutes = int(_get[3])
    seconds = int(_get[4])

    try:
        countdown = countdownClass(name, minutes, seconds)
    except Exception as e:
        return "text/plain", traceback.format_exc(e)
    else:
        return "text/plain", "Started"


    return "text/plain", json.dumps(countdown)



def requestHandler_countdownStatus(_get):
    global countdown

    return "text/plain", json.dumps(countdown)


def requestHandler_marquee(_get):
    """Initiate a scrolling marquee event."""
    global clients

    print (urllib2.unquote(_get[2]))

    for client in clients:
        client.write_message(json.dumps({"messagetype": "marquee", "message": urllib2.unquote(_get[2])}))

    return "text/plain", str(_get)


def requestHandler_RaidSimulator(get):
    """Simulate a Twitch raid event."""
    global clients

    try:
        print("******* OKAY this is the part where I'm calling isRaiding from the HTTP GET raid simulator!")
        isRaiding("(test)")

    except Exception as e:
        return "text/plain", traceback.format_exc(e)
    else:
        return "text/plain", "Started"


# sample title requests to make

# http://10.0.0.220:8081/titleplay/tracebox.html/%7B%22textBoxUpdater%22:%20%22Welcome%20to%20Nicks%20Mad%20Science,%20a%20place%20of%20wonder%20and%20magic.%22%7D
# http://10.0.0.220:8081/titleplay/nms-raidalert.html/%7B%22raidernameHandler%22:%20%22joeblow%22%7D
# http://10.0.0.220:8081/videoplay/webm/alert-new-follower.webm


# TODO - ALERTS




def requestHandler_titlePlay(get):
    """Fire off a Titlemaker title inside OBS."""
    global clients

    try:
        for client in clients:
            client.write_message(json.dumps({"messagetype": "titleplay", "url": get[2], "message": urllib2.unquote(get[3]), "instance": get[4]}))
    except:
        return "text/plain", traceback.format_exc()
    else:
        return "text/plain", "ok"



def requestHandler_videoPlay(get):
    """Play a fullscreen video inside OBS / the player."""

    global clients

    # TODO: once again, more DRY-related issues here
    try:
        for client in clients:
            client.write_message(json.dumps({"messagetype": "videoplay", "type": get[2], "url": get[3], "looping": get[4], "instance": get[5]}))
    except:
        return "text/plain", traceback.format_exc()
    else:
        return "text/plain", "ok"



def requestHandler_dogtrick(get):
    """Tell dogtrickplayer to issue a verbal command to Mouse."""

    global clients

    # TODO: once again, more DRY-related issues here
    try:
        for client in clients:
            client.write_message(json.dumps({"messagetype": "dogtrick", "trick": get[2]}))
    except:
        return "text/plain", traceback.format_exc()
    else:
        return "text/plain", "ok"




def requestHandler_resetDogCounter(get):
    """Reset red and blue dog counter to zero."""
    global clients, count

    count = {"red": 0, "blue": 0}

    try:

        json.dump(count, open("count.json", "wb"))

        for client in clients:
            client.write_message(json.dumps({"messagetype": "dogbutton", "count": count}))

    except:
        return "text/plain", traceback.write_exc()
    else:
        return "text/plain", "ok"



def requestHandler_spookymode(get):
    global clients, xr18

    try:
        xr18.send_message("/fx/1/insert", [1.0])
        xr18.send_message("/rtn/2/mix/fader", [0.4])
        xr18.send_message("/rtn/3/mix/fader", [0.7])
        xr18.send_message("/rtn/4/mix/fader", [0.6])

        # requests.get("http://10.0.0.44:8081/preset/totd")

    except:
        return "text/plain", traceback.write_exc()
    else:
        return "text/plain", "ok"


def requestHandler_notspookymode(get):
    global clients, xr18

    try:

        xr18.send_message("/fx/1/insert", [0.0])
        xr18.send_message("/rtn/2/mix/fader", [0.0])
        xr18.send_message("/rtn/3/mix/fader", [0.0])
        xr18.send_message("/rtn/4/mix/fader", [0.0])
        # requests.get("http://10.0.0.44:8081/preset/nms")

    except:
        return "text/plain", traceback.write_exc()
    else:
        return "text/plain", "ok"


def requestHandler_scene_startingsoonbrb(get):
    try:
        xr18.send_message("/ch/01/mix/fader", [0.75])
        xr18.send_message("/ch/03/mix/fader", [0.75])
        xr18.send_message("/ch/10/mix/fader", [0.0])
        xr18.send_message("/ch/13/mix/fader", [0.0])

    except:
        return "text/plain", traceback.write_exc()
    else:
        return "text/plain", "ok"


def requestHandler_scene_mics_on(get):
    try:
        xr18.send_message("/ch/01/mix/fader", [0.75])
        xr18.send_message("/ch/03/mix/fader", [0.75])
        xr18.send_message("/ch/10/mix/fader", [0.75])
        xr18.send_message("/ch/13/mix/fader", [0.75])

    except:
        return "text/plain", traceback.write_exc()
    else:
        return "text/plain", "ok"


def requestHandler_scene_farewell(get):
    try:
        xr18.send_message("/ch/01/mix/fader", [0.0])
        xr18.send_message("/ch/03/mix/fader", [0.75])
        xr18.send_message("/ch/10/mix/fader", [0.0])
        xr18.send_message("/ch/13/mix/fader", [0.0])

    except:
        return "text/plain", traceback.write_exc()
    else:
        return "text/plain", "ok"


def requestHandler_fog_on(get):
    try:
        turnOnRelay(relay_fogmachine)

    except:
        return "text/plain", traceback.write_exc()
    else:
        return "text/plain", "ok"



def requestHandler_fog_off(get):
    try:
        turnOffRelay(relay_fogmachine)

    except:
        return "text/plain", traceback.write_exc()
    else:
        return "text/plain", "ok"



def requestHandler_all_strobes_on(get):
    try:
        turnOnRelay(relay_raidlight)
        turnOnRelay(relay_redlight)
        turnOnRelay(relay_yellowlight)
        turnOnRelay(relay_bluelight)

    except:
        return "text/plain", traceback.write_exc()
    else:
        return "text/plain", "ok"



def requestHandler_all_strobes_off(get):
    try:
        turnOffRelay(relay_raidlight)
        turnOffRelay(relay_redlight)
        turnOffRelay(relay_yellowlight)
        turnOffRelay(relay_bluelight)

    except:
        return "text/plain", traceback.write_exc()
    else:
        return "text/plain", "ok"



# def requestHandler_showtime(get):
#     try:
#         # bleh

#     except:
#         return "text/plain", traceback.write_exc()
#     else:
#         return "text/plain", "ok"



# TODO: make capitalization consistent
httpRequests = {'': requestHandler_index,
                'count': requestHandler_count,
                'startCountdown': requestHandler_startCountdown,
                'countdownStatus': requestHandler_countdownStatus,
                'marquee': requestHandler_marquee,
                'titleplay': requestHandler_titlePlay,
                'videoplay': requestHandler_videoPlay,
                'resetdogcounter': requestHandler_resetDogCounter,
                'spookymode': requestHandler_spookymode,
                'notspookymode': requestHandler_notspookymode,
                'scene_startingsoonbrb': requestHandler_scene_startingsoonbrb,
                'scene_mics_on': requestHandler_scene_mics_on,
                'scene_farewell': requestHandler_scene_farewell,
                'fog_on': requestHandler_fog_on,
                'fog_off': requestHandler_fog_off,
                'all_strobes_on': requestHandler_all_strobes_on,
                'all_strobes_off': requestHandler_all_strobes_off,
                'RaidSimulator': requestHandler_RaidSimulator,
                'dogtrick': requestHandler_dogtrick}



#This class will handles any incoming request from
#the browser 
class myHandler(BaseHTTPRequestHandler):
    
    #Handler for the GET requests
    def do_GET(self):
        elements = self.path.split('/')

        responseFound = False
        for httpRequest, httpHandler in httpRequests.iteritems():
            # print elements[1] + " == " + httpRequest
            if elements[1] == httpRequest: # in other words, if the first part matches
                contentType, response = httpHandler(elements)
                responseFound = True

                self.send_response(200)
                self.send_header("Access-Control-Allow-Origin", "*")
                self.send_header('Content-type', contentType)
                self.end_headers()

                self.wfile.write(response)
        if not responseFound:
            contentType, response = requestHandler_index('/')

            self.send_response(200)
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header('Content-type', contentType)
            self.end_headers()

            self.wfile.write(response)
            
        return


def http():
    server = HTTPServer(('', PORT_NUMBER), myHandler)
    print ('Started httpserver on port ' , PORT_NUMBER)

    server.serve_forever()

httpThread = Thread(target=http)
httpThread.daemon = True
httpThread.start()






####### WEBSOCKET #######



clients = [] # https://stackoverflow.com/questions/11695375/tornado-identify-track-connections-of-websockets


# def sendFullStatus():
#     global clients




class WSHandler(tornado.websocket.WebSocketHandler):
    global clients, count, countdown

    def open(self):
        print ('new connection')
        clients.append(self)
        print (clients)

        # TODO: make a send-dog-button-count function
        # TODO: devise a system for data that needs to be sent on every new connection
        self.write_message(json.dumps({"messagetype": "dogbutton", "count": count}))
        # self.write_message(json.dumps({"messagetype": "countdown", "status": countdown}))

      
    def on_message(self, message):  # when the script receives a message from the web browser
        print ('message received:  %s' % message)

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
        print ('connection closed')
        clients.remove(self)
 
    def check_origin(self, origin):
        return True



application = tornado.web.Application([
    (r'/ws', WSHandler),
])

 
def socket():
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(6789)
    # myIP = socket.gethostbyname(socket.gethostname())
    # print '*** Websocket Server Started at %s***' % myIP
    tornado.ioloop.IOLoop.instance().start()

socketThread = Thread(target=socket)
socketThread.daemon = True
socketThread.start()



def sendPeriodicUpdates():
    """a li'l standalone thread that sends all system status-es every five seconds"""
    global count, countdown, clients

    while True:
        time.sleep(5)

        for client in clients:
            client.write_message(json.dumps({"messagetype": "dogbutton", "count": count}))
            # client.write_message(json.dumps({"messagetype": "countdown", "status": countdown}))

sendPeriodicUpdatesThread = Thread(target=sendPeriodicUpdates)
sendPeriodicUpdatesThread.daemon = True
sendPeriodicUpdatesThread.start()


# TODO: class countdownManager, which can have members self.timers = []


import PIL
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw
import socket

font = ImageFont.truetype("slkscr.ttf",10)

matrix = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def countdownManager():
    global countdown, clients, sevensegment

    while True:
        time.sleep(1)
        timeLeft = countdown.timeLeft()
        if timeLeft is not False:
            print(timeLeft)
            
            try:
                sevensegment.sendto(timeLeft + "                   ", ("10.0.0.245", 1234)) # HACK because I'd love for this to work now
            except:
                traceback_print_exc()

            try:
                img=Image.new("RGBA", (32,8),(0,0,0))

                draw = ImageDraw.Draw(img)
                draw.text((0, -3), timeLeft, font=font)
                draw = ImageDraw.Draw(img)



                omfg = b""
                for x in range(0, 32):
                    column = 0
                    # print ("x")
                    for y in range(0, 8):
                        # print ("y")
                        # print (img.getpixel((x, y)))
                        column = column | (img.getpixel((x, y))[0] > 128) << y
                    omfg += chr(column)

                matrix.sendto(omfg, ("10.0.0.200", 1234))
            except:
                traceback.print_exc()

            for client in clients:
                client.write_message(json.dumps({"messagetype": "countdown", "timeLeft": timeLeft}))

countdownManagerThread = Thread(target=countdownManager)
countdownManagerThread.daemon = True
countdownManagerThread.start()



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


serPort.write("gpio set " + str(relay_raidlight)   + "\r")
serPort.write("gpio set " + str(relay_redlight)    + "\r")
serPort.write("gpio set " + str(relay_yellowlight) + "\r")
serPort.write("gpio set " + str(relay_bluelight)   + "\r")
serPort.write("gpio set " + str(relay_fogmachine)  + "\r")





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





def on_message(ws, message_json):
    global serPort, count, clients

    print (message_json)

    message = json.loads(message_json)

    if message_json.find("channel-bits-events") != -1:
        print ("OH HECK IT'S BITS O'CLOCK")

        requests.get("http://10.0.0.220:8081/videoplay/webm/alert-cheer-optimized.webm/noloop/theripper")



        print ("test 1")
        try:
            print ("message: " + str(message))
        except:
            traceback.print_exc()

        print ("test 2")
        try:
            print ("message[\"data\"]: " + str(message["data"]))
        except:
            traceback.print_exc()

        print ("test 3")
        try:
            print ("message[\"data\"][\"message\"]: " + str(message["data"]["message"]))
        except:
            traceback.print_exc()

        print ("test 4")
        try:
            messageInMessage = json.loads(message["data"]["message"])
            subscriberMessage = "Thanks for the bits, " + messageInMessage["user_name"] + "!"
        except:
            traceback.print_exc()
            subscriberMessage = "Thanks for the bits!"

        print ("test 1")
        try:
            messageInMessage = json.loads(message["data"]["message"].replace("\\", ""))
        except:
            traceback.print_exc()

        # {"type":"MESSAGE","data":{"topic":"channel-bits-events-v2.105293178","message":"{\"data\":{\"user_name\":\"misscocoderp\",\"channel_name\":\"nicksmadscience\",\"user_id\":\"91256946\",\"channel_id\":\"105293178\",\"time\":\"2020-09-01T19:22:28.308448802Z\",\"chat_message\":\"Cheer1 Cheer1 test\",\"bits_used\":2,\"total_bits_used\":2,\"is_anonymous\":false,\"context\":\"cheer\",\"badge_entitlement\":{\"new_version\":1,\"previous_version\":0}},\"version\":\"1.0\",\"message_type\":\"bits_event\",\"message_id\":\"44653b0f-e601-57ae-a89f-6eb0cfc972a8\"}"}}

        if message_json.find(string.lower("Cheer100")) != -1:
            print ("Cheer100 confirmed")
            requests.get("http://10.0.0.4/attention")
        elif message_json.find(string.lower("Cheer101")) != -1:
            print ("Cheer101 confirmed")
            requests.get("http://10.0.0.5/attention")
        else:
            print ("No bit alerts found")


        turnOnRelay(relay_yellowlight)
        turnOnLED(led_bits)
        time.sleep(10)
        turnOffRelay(relay_yellowlight)
        turnOffLED(led_bits)

    elif message_json.find("c910a800-ecb3-4917-bab1-e47399dfd2d2") != -1:
        print ("OH HECK IT'S YELLOW STROBE TEST O'CLOCK")
        turnOnRelay(relay_yellowlight)
        time.sleep(10)
        turnOffRelay(relay_yellowlight)

    elif message_json.find("77f991d8-a75c-4273-91b6-259e25009617") != -1:
        print ("OH HECK IT'S CHIME O'CLOCK")
        turnOnRelay(relay_chime)
        time.sleep(0.5)
        turnOffRelay(relay_chime)

    elif message_json.find("6dcaa344-0bae-40f8-b2ff-baa3ace98cd3") != -1:
        print ("OH HECK IT'S FOG O'CLOCK")
        turnOnRelay(relay_fogmachine)
        time.sleep(5)
        turnOffRelay(relay_fogmachine)

    elif message_json.find("723006a2-3caf-4a6a-9aff-3dbe94231d41") != -1:
        print ("OH HECK IT'S RED LIGHT TEST O'CLOCK")
        turnOnRelay(relay_redlight)
        time.sleep(5)
        turnOffRelay(relay_redlight)

# {"type":"MESSAGE","data":{"topic":"channel-subscribe-events-v1.105293178","message":"{\"benefit_end_month\":10,\"user_name\":\"misscocoderp\",\"display_name\":\"MissCocoDerp\",\"channel_name\":\"nicksmadscience\",\"user_id\":\"91256946\",\"channel_id\":\"105293178\",\"time\":\"2020-09-01T18:35:37.040205227Z\",\"sub_message\":{\"message\":\"\",\"emotes\":null},\"sub_plan\":\"1000\",\"sub_plan_name\":\"Channel Subscription (nicksmadscience)\",\"months\":0,\"cumulative_months\":1,\"context\":\"sub\",\"is_gift\":false,\"multi_month_duration\":0}"}}

    elif message_json.find("channel-subscribe-events") != -1:

        try:
            messageInMessage = json.loads(message["data"]["message"])
            subscriberMessage = messageInMessage["user_name"] + " has subscribed!"
        except:
            traceback.print_exc()
            subscriberMessage = "Thanks for subscribing!"

        print ("OH HECK IT'S SUBSCRIBER O'CLOCK")
        turnOnRelay(relay_redlight)
        turnOnLED(led_raid)
        turnOnRelay(relay_fogmachine)

        requests.get("http://10.0.0.220:8081/titleplay/nms-lower-third.html/{\"textHandler\": \"" + subscriberMessage + "\"}/theripper")
        requests.get("http://10.0.0.220:8081/videoplay/webm/alert-new-subscriber.webm/noloop/theripper")

        time.sleep(5)
        turnOffRelay(relay_redlight)
        turnOffLED(led_raid)
        turnOffRelay(relay_fogmachine)

        # eventHandler("new subscriber", "subscriber name")

    elif message_json.find("1f1bc054-a48f-418b-b148-bfe14580bb4b") != -1:
        print ("OH HECK IT'S BLUE BUTTON A O'CLOCK")
        count["blue"] += 1
        print ("blue: " + str(count["blue"]) + "  red: " + str(count["red"]))
        try:
            requests.get("http://10.0.0.4/attention")
        except Exception as e:
            traceback.print_exc(e)

        for client in clients:
            client.write_message(json.dumps({"messagetype": "dogbutton", "count": count}))

        with open("count.json", "wb") as count_file:
            count_file.write(json.dumps(count))

        teamName = count["blueteam"]
        score = count["blue"]

        requests.get("http://10.0.0.220:8081/titleplay/nms-giant-scoreboard.html/{\"teamNameUpdater\": \"" + teamName + "\", \"scoreUpdater\": \"" + str(score) + "\"}/nc1in")
        requests.get("http://10.0.0.220:8081/videoplay/webm/blur-and-lightning.webm/noloop/nc1in")


    elif message_json.find("a015be4f-c7ff-4a27-b519-414a4afc02a1") != -1:
        print ("OH HECK IT'S RED BUTTON B O'CLOCK")
        count["red"] += 1
        print ("blue: " + str(count["blue"]) + "  red: " + str(count["red"]))
        try:
            requests.get("http://10.0.0.5/attention")
        except Exception as e:
            traceback.print_exc(e)

        for client in clients:
            client.write_message(json.dumps({"messagetype": "dogbutton", "count": count}))

        with open("count.json", "wb") as count_file:
            count_file.write(json.dumps(count))

        teamName = count["redteam"]
        score = count["red"]

        # TODO: could there be a more direct way than the script calling its own webserver?
        requests.get("http://10.0.0.220:8081/titleplay/nms-giant-scoreboard.html/{\"teamNameUpdater\": \"" + teamName + "\", \"scoreUpdater\": \"" + str(score) + "\"}/nc1in")
        requests.get("http://10.0.0.220:8081/videoplay/webm/blur-and-lightning.webm/noloop/nc1in")

    elif message_json.find("a95fcc52-8ed9-4f47-93ff-07749826da39") != -1:
        print ("OH HECK IT'S YELLOW BUTTON B O'CLOCK")

        requests.get("http://10.0.0.220:8081/titleplay/nms-feedthatpup.html/{}/theripper")

        try:
            requests.get("http://10.0.0.3/attention")
        except Exception as e:
            traceback.print_exc(e)
     



def on_error(ws, error):
    pprint.pprint(json.loads(error))

def on_close(ws):
    print ("### closed ###")

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
        print ("thread terminating...")
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



                if username not in usersInChat:
                    color = generateNewColor()
                    usersInChat[username] = {"color": color}
                else:
                    color = usersInChat[username]["color"]

                line = json.dumps({"messagetype": "chat", "color": color, "username": username, "message": message, "messageWithUsernameIfAny": username + ": " + message, "messageType": "privmsg", "chatLineNumber": chatLineNumber})#"<p class='chatline' style='color: %s'>%s: %s</p>" % (color, username, message)

                print (message)

                for client in clients:
                    client.write_message(line)

                # {"type":"MESSAGE","data":{"topic":"channel-bits-events-v2.105293178","message":"{\"data\":{\"user_name\":\"misscocoderp\",\"channel_name\":\"nicksmadscience\",\"user_id\":\"91256946\",\"channel_id\":\"105293178\",\"time\":\"2020-09-01T19:22:28.308448802Z\",\"chat_message\":\"Cheer1 Cheer1 test\",\"bits_used\":2,\"total_bits_used\":2,\"is_anonymous\":false,\"context\":\"cheer\",\"badge_entitlement\":{\"new_version\":1,\"previous_version\":0}},\"version\":\"1.0\",\"message_type\":\"bits_event\",\"message_id\":\"44653b0f-e601-57ae-a89f-6eb0cfc972a8\"}"}}

                if message[0:5].lower() == "cheer" or message[0:5].lower() == "corgo" or message[0:5] == "Butts":
                    print ("OMFG CHEER")
                    # Don't actually need to handle this here because I've got PubSub


                # TODO: obviously, screen to make sure this is coming from an authorized account

                # TODO: there appears to be a "real" way to do this in IRC if enabled
                elif message.find("is raiding the channel") != -1:
                    if username == "nicksmadscience" or username == "streamelements":
                        try:
                            print("******* OKAY this is the part where I'm calling isRaiding because I saw \"is raiding\" in chat!")
                            isRaiding(message.split(" ")[0])
                        except:
                            traceback.print_exc()
                            isRaiding("(exception)")
                    else:
                        print "found text but username wasn't authorized (" + str(username) + ")"

                elif message.find("Thank you for following") != -1:
                    if username == "nicksmadscience" or username == "streamelements":
                        print ("OMFG NEW FOLLOWER")
                        requests.get("http://10.0.0.220:8081/videoplay/webm/alert-new-follower-optimized.webm/noloop/theripper")
                        requests.get("http://10.0.0.220:8081/titleplay/nms-lower-third.html/{\"textHandler\": \"" + message + "\"}/theripper")
                        turnOnRelay(relay_bluelight)
                        time.sleep(5)
                        turnOffRelay(relay_bluelight)
                    else:
                        print "found text but username wasn't authorized (" + str(username) + ")"


            # else:
                # line = json.dumps({"messagetype": "chat", "color": "gray", "username": "[none]", "message": line, "messageWithUsernameIfAny": line, "messageType": "info", "chatLineNumber": chatLineNumber})

            
            # print (line)


            with open("chatlog.txt", "ab") as chatlog_file:
                chatlog_file.write(line + "\n")

    except KeyboardInterrupt:
        go = False
    except:
        traceback.print_exc()

    time.sleep(0.1)






