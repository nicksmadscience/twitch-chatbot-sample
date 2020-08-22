import socket, time, datetime, requests, json, websocket
from threading import Thread

UDP_IP = "10.0.0.200"
UDP_PORT = 1234
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)



# def reverse_bit(num):
#     # print (num)
#     # print (format(num, '08b'))
#     result = 0
#     for i in range(0, 8):
#         result = (result << 1) + (num & 1)
#         num >>= 1
    
#     # print (format(result, '08b'))



#     return result



# def flipVertical(_string):
#     jam = ""
#     for i in _string:
#         jam += chr(reverse_bit(ord(i)))

#     return jam


# def flipHorizontal(_string):
#     jam = ""
#     length = len(_string)
#     for i in range(0, length):
#         jam += _string[length - 1 - i]

#     return jam




# def flip(_string):
#     return flipVertical(flipHorizontal(_string))



# zero  = chr(0b01111110)
# zero += chr(0b11111111)
# zero += chr(0b11000011)
# zero += chr(0b11111111)
# zero += chr(0b01111110)

# one  = chr(0b00000011)
# one += chr(0b11111111)
# one += chr(0b11111111)
# one += chr(0b01100011)

# two  = chr(0b01110011)
# two += chr(0b11111011)
# two += chr(0b11001111)
# two += chr(0b11000111)
# two += chr(0b01100011)

# three  = chr(0b01111110)
# three += chr(0b11111111)
# three += chr(0b11011011)
# three += chr(0b11011011)
# three += chr(0b01000010)

# four  = chr(0b11111111)
# four += chr(0b11111111)
# four += chr(0b00011000)
# four += chr(0b00011000)
# four += chr(0b11111000)
# four += chr(0b11110000)

# five  = chr(0b11001110)
# five += chr(0b11011110)
# five += chr(0b11011011)
# five += chr(0b11011011)
# five += chr(0b11111011)

# six  = chr(0b01001110)
# six += chr(0b11011011)
# six += chr(0b11011011)
# six += chr(0b11111111)
# six += chr(0b01111110)

# seven  = chr(0b11110000)
# seven += chr(0b11111000)
# seven += chr(0b11001100)
# seven += chr(0b11000110)
# seven += chr(0b11000011)

# eight  = chr(0b01100110)
# eight += chr(0b01111110)
# eight += chr(0b11001101)
# eight += chr(0b11011001)
# eight += chr(0b01111110)
# eight += chr(0b01100110)

# nine = flip(six)

# colon  = chr(0b01100110)
# colon += chr(0b01100110)


# skinny_zero  = chr(0b01111100)
# skinny_zero += chr(0b10000010)
# skinny_zero += chr(0b01111100)

# skinny_one  = chr(0b00000010)
# skinny_one += chr(0b11111110)
# skinny_one += chr(0b01000010)

# skinny_two  = chr(0b01100010)
# skinny_two += chr(0b10010010)
# skinny_two += chr(0b10001110)

# skinny_three  = chr(0b01111100)
# skinny_three += chr(0b10010010)
# skinny_three += chr(0b10010010)

# skinny_four  = chr(0b11111110)
# skinny_four += chr(0b00010000)
# skinny_four += chr(0b11110000)

# skinny_five  = chr(0b10001100)
# skinny_five += chr(0b10010010)
# skinny_five += chr(0b11110010)

# skinny_six  = chr(0b10001100)
# skinny_six += chr(0b10010010)
# skinny_six += chr(0b01111100)

# skinny_seven  = chr(0b01111110)
# skinny_seven += chr(0b10000000)
# skinny_seven += chr(0b10000000)

# skinny_eight  = chr(0b01101100)
# skinny_eight += chr(0b10010010)
# skinny_eight += chr(0b01101100)

# skinny_nine  = chr(0b01111100)
# skinny_nine += chr(0b10010010)
# skinny_nine += chr(0b01100010)

# skinny_colon = chr(0b00101000)

# skinny_a  = chr(0b00111110)
# skinny_a += chr(0b00101000)
# skinny_a += chr(0b00111110)

# skinny_p  = chr(0b00111000)
# skinny_p += chr(0b00101000)
# skinny_p += chr(0b00111110)


# # def set_bit(v, index, x):
# #   """Set the index:th bit of v to 1 if x is truthy, else to 0, and return the new value."""
# #   mask = 1 << index   # Compute mask, an integer with just bit 'index' set.
# #   v &= ~mask          # Clear the bit indicated by the mask (if x is False)
# #   if x:
# #     v |= mask         # If x was True, set the bit indicated by the mask.
# #   return v            # Return the result, we're done.




# # def flipVertical(_byte):
# #   newjam = 0
# #   for i in range(0, 8):
# #       newjam = set_bit(newjam, i, )


# def digit(_number):
#     if _number == 0:
#         return zero
#     elif _number == 1:
#         return one
#     elif _number == 2:
#         return two
#     elif _number == 3:
#         return three
#     elif _number == 4:
#         return four
#     elif _number == 5:
#         return five
#     elif _number == 6:
#         return six
#     elif _number == 7:
#         return seven
#     elif _number == 8:
#         return eight
#     elif _number == 9:
#         return nine

# def skinny_digit(_number):
#     if _number == 0:
#         return skinny_zero
#     elif _number == 1:
#         return skinny_one
#     elif _number == 2:
#         return skinny_two
#     elif _number == 3:
#         return skinny_three
#     elif _number == 4:
#         return skinny_four
#     elif _number == 5:
#         return skinny_five
#     elif _number == 6:
#         return skinny_six
#     elif _number == 7:
#         return skinny_seven
#     elif _number == 8:
#         return skinny_eight
#     elif _number == 9:
#         return skinny_nine


# while True:
#     omfg = ""

#     omfgtime = datetime.datetime.now()
#     hour = omfgtime.hour
#     minute = omfgtime.minute
#     second = omfgtime.second
#     print (hour, minute, second)

#     # hour = 23

#     if hour == 0:
#         displayhour = 12
#         am = True
#     elif hour == 12:
#         displayhour = 12
#         am = False
#     elif hour < 12:
#         displayhour = hour
#         am = True
#     else:
#         displayhour = hour - 12
#         am = False

#     if displayhour >= 10:
#         omfg += flip(skinny_one) + chr(0) + flip(skinny_digit(displayhour - 10))
#     else:
#         omfg += flip(skinny_digit(displayhour))

#     omfg += chr(0) + flip(skinny_colon) + chr(0)

#     if minute >= 10:
#         omfg += flip(skinny_digit(int(minute / 10))) + chr(0) + flip(skinny_digit(minute % 10))
#     else:
#         omfg += flip(skinny_zero) + chr(0) + flip(skinny_digit(minute))

    

#     omfg += chr(0) + flip(skinny_colon) + chr(0)

#     if second >= 10:
#         omfg += flip(skinny_digit(int(second / 10))) + chr(0) + flip(skinny_digit(second % 10))
#     else:
#         omfg += flip(skinny_zero) + chr(0) + flip(skinny_digit(second))

#     if am:
#         omfg += chr(0) + flip(skinny_a)
#     else:
#         omfg += chr(0) + flip(skinny_p)

#     for i in range(len(omfg), 32):
#         omfg += chr(0)

#     if omfgtime.hour <= 10 or omfgtime.hour >= 21:
#         omfg += chr(1)
#     else:
#         omfg += chr(15)

#     # sock.sendto(omfg, ("10.0.0.213", 1234))
#     sock.sendto(omfg, (UDP_IP, UDP_PORT))
#     time.sleep(1.0)


import PIL
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw

# from twitch import TwitchClient
import pprint

font = ImageFont.truetype("slkscr.ttf",10)

# client = TwitchClient(client_id='8ccs3yg3wfauwr3fj4uhph6ahek8tq')
# channel = client.channels.get_by_id(105293178)



def on_message(ws, message):
    msg = json.loads(message)
    print msg
    

def on_error(ws, error):
    pprint.pprint(json.loads(error))

def on_close(ws):
    print "### closed ###"

def on_open(ws):
    print "open"
    def run(*args):
        # ws.send(json.dumps(listenToEvents))
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


ws = websocket.WebSocketApp("wss://10.0.0.220:6789",
                                on_message = on_message,
                                on_error = on_error,
                                on_close = on_close)



websocket.enableTrace(True)

ws.on_open = on_open

print "a"

ws.run_forever()


# def wsRunForever():
#     """Literally just runs run_forever, but asynchronously (in a thread)."""
#     ws.run_forever()

# wsRunForeverThread = Thread(target=wsRunForever)  # TODO: this could be a function
# wsRunForeverThread.daemon = True
# wsRunForeverThread.start()



img=Image.new("RGBA", (32,8),(0,0,0))

draw = ImageDraw.Draw(img)
draw.text((0, -3),"05:00", font=font)
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

sock.sendto(omfg, (UDP_IP, UDP_PORT))


# while True:
#     for i in range(0, 4):  # don't flood Twitch with requests; it's cool if this updates once every half minute or so

#         # followers = client.channels.get_followers(105293178)
#         # latestfollower = followers[0]["user"]["display_name"]
#         # print (latestfollower)

#         for frame in range(0, 256):
#             img=Image.new("RGBA", (32,8),(0,0,0))

#             draw = ImageDraw.Draw(img)
#             draw.text((32 - (frame * 2), -3),"roffle roffle roffle roffle", font=font)
#             draw = ImageDraw.Draw(img)

#             omfg = b""
#             for x in range(0, 32):
#                 column = 0
#                 # print ("x")
#                 for y in range(0, 8):
#                     # print ("y")
#                     # print (img.getpixel((x, y)))
#                     column = column | (img.getpixel((x, y))[0] > 128) << y
#                 omfg += chr(column)


            # sock.sendto(omfg, (UDP_IP, UDP_PORT))
            # time.sleep(0.03)


# img.save("a_test.png")




# headers = {'Client_ID': '8ccs3yg3wfauwr3fj4uhph6ahek8tq'}

# print (requests.get('https://api.twitch.tv/helix/users/follows?to_id=105293178&api_version=5', headers=headers).text)



# url = "https://api.twitch.tv/kraken/channels/otlet 15"

# headers = {"Accept": "application/vnd.twitchtv.v3+json", "Client-ID": "8ccs3yg3wfauwr3fj4uhph6ahek8tq"}

# print (requests.get(url, headers=headers).text)










# pprint.pprint(followers)

# print (channel.get_followers())






    # omfg = flip(nine)# flip(zero) + chr(0) + flip(one) + chr(0) + flip(two) + chr(0) + flip(three) + chr(0) + flip(four)



# for i in range(0, 33):
#   omfg = ""

#   for j in range(0, i):
#       omfg += chr(255)
#   for j in range(i, 32):
#       omfg += chr(0)

# sock.sendto(omfg, (UDP_IP, UDP_PORT))
# time.sleep(0.25) 




# omfg = omfg + chr(0b00000000)
# omfg = omfg + chr(0b01000010)
# omfg = omfg + chr(0b11000011)
# omfg = omfg + chr(0b11001011)
# omfg = omfg + chr(0b11001011)
# omfg = omfg + chr(0b11001011)
# omfg = omfg + chr(0b11001011)
# omfg = omfg + chr(0b11001011)
# omfg = omfg + chr(0b01010101)
# omfg = omfg + chr(0b10101010)

# for i in range(0, 31 - len(omfg)):
#   omfg = omfg + chr(0)



