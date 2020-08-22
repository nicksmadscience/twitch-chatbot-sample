import threading
import datetime


class countdownClass:
    def __init__(self, name, duration_minutes, duration_seconds):

        # assert type(_startTime) == "datetime"

        self.name      = name
        self.endTime   = datetime.datetime.now() + datetime.timedelta(minutes = duration_minutes, seconds = duration_seconds)
        # print ("endTime type: " + str(type(self.endTime)))

    def timeLeft(self):
        """Returns the amount of time left in this countdown in string format."""

        currentTime = datetime.datetime.now()

        if self.endTime < currentTime:
            return False
        else:
            roffle = self.endTime - currentTime
            # print ("roffle type: " + str(type(roffle)))
            return str(roffle)[2:7]






