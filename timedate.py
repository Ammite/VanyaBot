from constants import *


def in_minutes(hour: int, minutes: int) -> int:
    return hour * 60 + minutes


def in_minutes_t(time) -> int:
    return time.hour * 60 + time.minute


def add_utc(utc, hours, minutes, day):
    if hours + utc < 24:
        hours += utc
    elif hours + utc == 24:
        hours = 0
        day = (day + 1) if day < 6 else 0
    else:
        hours = hours + utc - 24
        day = (day + 1) if day < 6 else 0

    return list([hours, minutes, day])


class Time:
    hour = int
    minute = int

    def __init__(self, hour, minute):
        self.hour = hour
        self.minute = minute

    def print(self):
        return str(self.hour) + ":" + str(self.minute)


class Period:
    time_start = Time
    time_end = Time
    subject = str
    kind = str
    room = int
    day = str

    def __init__(self, day, subject, kind, time_start, time_end, room):
        self.day = day
        self.subject = subject
        self.kind = kind
        self.time_start = to_time(time_start)
        self.time_end = to_time(time_end)
        self.room = room

    def print_period(self):
        print(self.day, self.subject, self.kind, self.time_start.print(), self.time_end.print(), self.room)


def to_time(time_string):
    h = int(time_string[0] + time_string[1])
    m = int(time_string[3] + time_string[4])
    return Time(h, m)


def in_h_m(minute):
    return int(minute / 60), minute % 60
