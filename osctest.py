import argparse
import time

from oscpy.client import OSCClient


if __name__ == "__main__":
  xr18 = OSCClient("10.0.0.99", 10024)

  #client.send_message("/ch/01/mix/fader", 0.1)
  
  # client.send_message("/fx/1/insert", 1.0)
  # client.send_message("/rtn/2/mix/fader", 0.4)
  # client.send_message("/rtn/3/mix/fader", 0.7)
  # client.send_message("/rtn/4/mix/fader", 0.6)


  # client.send_message("/fx/1/insert", 0.0)
  # client.send_message("/rtn/2/mix/fader", 0.0)
  # client.send_message("/rtn/3/mix/fader", 0.0)
  # client.send_message("/rtn/4/mix/fader", 0.0)

