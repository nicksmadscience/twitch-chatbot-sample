# irc.chat.twitch.tv
# 6667
# Your nickname must be your Twitch username / handle
# Your password should be an OAuth token. You can get your OAuth token here (Thanks Andrew Bashore!)
# http://www.twitchapps.com/tmi/
# An example "password" using this method would be "oauth:asdasd234asd234ad234asds23" without quotes.


import sys
import socket
import string
from threading import Thread
import inspect
from parse import *
from parse import compile
import random
import json
import traceback
import time

import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web
import socket

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

      
    def on_message(self, message):
        print 'message received:  %s' % message

        if message == "deathcounter":
            with open("deathcounter.txt", "rb") as deathcounter_file:
                deathcounter = int(deathcounter_file.read())

            deathcounter += 1
            print "death counter: " + str(deathcounter)

            with open("deathcounter.txt", "wb") as deathcounter_file:
                deathcounter_file.write(str(deathcounter))

            for client in clients:
                client.write_message(json.dumps({"messagetype": "deathcounter", "animation": "explode", "deathcounter": str(deathcounter)}))
        elif message == "water deathcounter":
            with open("deathcounter.txt", "rb") as deathcounter_file:
                deathcounter = int(deathcounter_file.read())

            deathcounter += 1
            print "death counter: " + str(deathcounter)

            with open("deathcounter.txt", "wb") as deathcounter_file:
                deathcounter_file.write(str(deathcounter))

            for client in clients:
                client.write_message(json.dumps({"messagetype": "deathcounter", "animation": "water", "deathcounter": str(deathcounter)}))
        elif message == "refresh deathcounter":
            with open("deathcounter.txt", "rb") as deathcounter_file:
                deathcounter = int(deathcounter_file.read())

            for client in clients:
                client.write_message(json.dumps({"messagetype": "deathcounter", "animation": "explode", "deathcounter": str(deathcounter)}))
        elif message == "decrement deathcounter":
            with open("deathcounter.txt", "rb") as deathcounter_file:
                deathcounter = int(deathcounter_file.read())

            deathcounter -= 1
            print "death counter: " + str(deathcounter)

            with open("deathcounter.txt", "wb") as deathcounter_file:
                deathcounter_file.write(str(deathcounter))

            for client in clients:
                client.write_message(json.dumps({"messagetype": "deathcounter", "animation": "reverse", "deathcounter": str(deathcounter)}))
        elif message == "twelve":
            for client in clients:
                client.write_message(json.dumps({"messagetype": "oneshot", "video": "twelverlay.webm"}))
        elif message == "themoyouknow":
            for client in clients:
                client.write_message(json.dumps({"messagetype": "oneshot", "video": "themoyouknow.webm"}))
        elif message == "ohshit":
            for client in clients:
                client.write_message(json.dumps({"messagetype": "oneshot", "video": "one shot- oh shiiiiiiiiiiit.webm"}))
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

p = compile(":{}!{}@{}.tmi.twitch.tv PRIVMSG #{} :{}")
# ":nicksmadscience!nicksmadscience@nicksmadscience.tmi.twitch.tv PRIVMSG #nicksmadscience :fwewewef"


def generateNewColor():
    return "rgb(%d, %d, %d)" % (int(random.random() * 128 + 128), int(random.random() * 128 + 128), int(random.random() * 128 + 128))

usersInChat = {}
chatLineNumber = 0

go = True
while go:
    try:
        readbuffer=readbuffer+s.recv(1024)
        temp=string.split(readbuffer, "\n")
        readbuffer=temp.pop( )

        for line in temp:
            chatLineNumber += 1
            line = string.rstrip(line)

            if line.find("PING") != -1:
                s.send("PONG %s\r\n" % line[1])
                print "pong"

            elif line.find("PRIVMSG") != -1:
                messageDeconstructed = p.parse(line)

                try:
                    username = messageDeconstructed[0]
                except:
                    for client in clients:
                        client.write_message("[omg exception]")
                    message = "[omg exception]"

                message = messageDeconstructed[4]

                if username not in usersInChat:
                    color = generateNewColor()
                    usersInChat[username] = {"color": color}
                else:
                    color = usersInChat[username]["color"]

                line = json.dumps({"messagetype": "chat", "color": color, "username": username, "message": message, "messageWithUsernameIfAny": username + ": " + message, "messageType": "privmsg", "chatLineNumber": chatLineNumber})#"<p class='chatline' style='color: %s'>%s: %s</p>" % (color, username, message)
            else:
                line = json.dumps({"messagetype": "chat", "color": "gray", "username": "[none]", "message": line, "messageWithUsernameIfAny": line, "messageType": "info", "chatLineNumber": chatLineNumber})

            print line

            # try:
            #     line=string.rstrip(line).split("PRIVMSG #nicksmadscience :")[1] # see if it's a PRIVMSG; if so, just send the message contents; otherwise, send the whole string
            # except IndexError:
            #     line = string.rstrip(line)
            

            for client in clients:
                client.write_message(line)

            # for wordoftheday in wordsoftheday:
            #     print line
    except KeyboardInterrupt:
        go = False
    except:
        traceback.print_exc()

    time.sleep(0.1)

        





