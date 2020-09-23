#!/usr/bin/env

from datetime import datetime

def clean_padding_whitespace(string):
    toreturn = " ".join(string.split())
    return toreturn

def create_datetime(month, day, time):

    ampm = "am" if "am" in time else "pm"
    time = time.replace("am", "").replace("pm", "")

    time_split = time.split(":")

    hours, minutes = (time_split[0], "00") if len(time_split) == 1 else (time_split[0], time_split[1])

    if len(hours) == 1:
        hours = "0" + hours

    return datetime.strptime(f"{datetime.now().year} {month} {day} {hours}:{minutes}{ampm}", "%Y %b %d %I:%M%p").strftime("<%Y-%m-%d %a %H:%M>")
