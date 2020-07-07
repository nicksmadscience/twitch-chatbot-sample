import sys
import time
import serial
import websocket
import thread
import json

with open("secrets.json") as secrets_file:
    secrets = json.loads(secrets_file.read())

print ("id: " + secrets["id"])
print ("key: " + secrets["key"])



# you will need to go into /dev and find the relay card's serial port
relayCardSerial = '/dev/ttyACM0'

#Open port for communication    
serPort = serial.Serial(relayCardSerial, 19200, timeout=1)

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
sampleListenRequest = {
  "type": "LISTEN",
  # "nonce": "boobs lol",
  "data": {
    "topics": ["channel-bits-events-v1." + secrets["id"]],
    "auth_token": secrets["key"]
  }
}


def on_message(ws, message):
    print "(msg) " + message

def on_error(ws, error):
    print "(err)" + error

def on_close(ws):
    print "### closed ###"

def on_open(ws):
    def run(*args):
        while True:
            ws.send(json.dumps(sampleListenRequest))
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