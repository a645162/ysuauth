import ntp
import datetime
import time


class time_p():
    t = None

    def NTP_GetTime(self):
        t = ntp.ntp_getTimeStamp()
        self.t = t
        return t

    def Now_P(self, timestamp=0):
        t = None

        if timestamp == 0:
            t = self.t

        if t is None:
            return time.time()

        return datetime.datetime.fromtimestamp(t)
