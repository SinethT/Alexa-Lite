from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import speech_recognition as sr
import wikipedia
import pyttsx3
import pyjokes
import re
import datetime
import sys

try:
    import pywhatkit
except:
    sys.exit("Make sure you are connected to the Internet!")


recognizer = sr.Recognizer()
engine = pyttsx3.init()

# Setting voice: female voice
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[1].id)

geolocator = Nominatim(user_agent="Alexa")


def main():
    run_command(get_command())


# Talking
def talk(text):
    engine.say(text)
    engine.runAndWait()


# Checking if command started with "Alexa":
def wake_up(command):
    if re.search(r"^\balexa\b.+$", command, re.IGNORECASE):
        return True
    else:
        return False


def vid(command):
    # Checking if a video/song
    if matches := re.search(r"^\bplay \b(.+)", command, re.IGNORECASE):
        # Extracting the video/song: Play on youtube
        pywhatkit.playonyt(matches.group(1))
        talk("playing" + matches.group(1))
        return True
    else:
        return False


def time(command):
    # Checking if asked for the time:
    if re.search(
        r"^(\bwhat's\b|\bwhat is\b|\btell\b)(\b me\b|\b us\b)?(\b the\b)?(\b current\b)?\b time\b(\b now\b)?(\b please\b)?$",
        command,
        re.IGNORECASE,
    ):
        # Getting the current time: in str format
        time = datetime.datetime.now().strftime("%I:%M %p")
        print(time)
        talk("The current time is " + time)
        return True
    else:
        return False


def date(command):
    day_endings = {1: "st", 2: "nd", 3: "rd", 21: "st", 22: "nd", 23: "rd", 31: "st"}
    # Getting the date:
    weekday, day, month, year = (
        datetime.datetime.now().strftime("%A,%d,%B,%Y").split(",")
    )

    # Checking if asked for the date:
    if re.search(
        r"^(\bwhat's\b|\bwhat is\b|\btell\b)(\b me\b|\b us\b)?(\b the\b)?(\b current \b)?(\btoday's\b)? (\bdate\b|\bmonth\b|\byear\b)(\b please\b)?$",
        command,
        re.IGNORECASE,
    ):
        # Print & Talk: the date
        print(
            f"{weekday} {str(day)+'th' if not day in day_endings.keys() else str(day) + day_endings[day]} of {month} {year}"
        )
        talk(
            f"{weekday} {str(day)+'th' if not day in day_endings.keys() else str(day) + day_endings[day]} of {month} {year}"
        )
        return True
    else:
        return False


def joke(command):
    # Checking if a joke:
    if re.search(
        r"^(\btell|\bsay)(s\b)?(\b me\b|\b us\b)?(\b a\b|\b an\b|\b the\b|\b some\b)?.+\bjoke(s\b)?(\b please\b)?$",
        command,
        re.IGNORECASE,
    ):
        # Get the joke:
        joke = pyjokes.get_joke()
        # Print & Talk:
        print(joke)
        talk(joke)
        return True
    else:
        return False


def aerial_distance(command):
    # Checking if  a distance:
    if matches := re.search(
        r"^(?:\bwhat's\b|\bwhat is\b|\btell\b)(?:\b me\b|\b us\b)?(?:\b the\b)?(?:\b arial\b|\b aerial\b)?\b distance \b(?:\bbetween\b|\bfrom\b) (.+) (?:\band\b|\bto\b) (.+)(?:\b please\b)?$",
        command,
        re.IGNORECASE,
    ):
        try:
            # Extracting the user input:
            # Locating the locations:
            location1 = geolocator.geocode(matches.group(1))
            location2 = geolocator.geocode(matches.group(2))
        except:
            talk("Error occured while processing... Try again...")
            sys.exit("Error! Try Again...")
        # Getting longitude & latitude:
        place1 = (location1.latitude, location1.longitude)
        place2 = (location2.latitude, location2.longitude)
        # Getting the aerial distance: in km
        distance = geodesic(place1, place2).km
        print(
            f"The aerial distance between {matches.group(1)} and {matches.group(2)} = {distance} km"
        )
        talk(
            f"The aerial distance between {matches.group(1)} and {matches.group(2)} is {distance:.2f} kilometres"
        )
        return True
    else:
        return False


def wiki(command):
    # Checking if asked for an info:
    if matches := re.search(
        r"^(?:\bwho\b|\bwhat\b) (?:\bis\b|\bare\b) (.+)", command, re.IGNORECASE
    ):
        try:
            # Searching in wikipedia:
            print(wikipedia.summary(matches.group(1), 3))
            talk(wikipedia.summary(matches.group(1), 3))
            return True
        except:
            # Searching in google:
            pywhatkit.search(matches.group(1))
            return True
    else:
        return False


def get_command():
    errors = 0
    while True:
        try:
            # Acessing the mic:
            with sr.Microphone() as source:
                print("listening...")
                # Speech recognizing:
                command = recognizer.recognize_google(recognizer.listen(source))
                if not wake_up(command):
                    raise ValueError
                break
        except:
            talk("Sorry, I can't understand that")
            # Exiting if "errors" == 2:
            if errors == 2:
                talk("Try Again later...")
                sys.exit("Try again later...")
            # Increasing "errors" by 1:
            errors += 1
            print("Try Again...")
            talk("Try Again...")

    # Returning without "alexa":
    return command.replace(command[:6], "")


def run_command(command):
    if not vid(command):
        if not time(command):
            if not date(command):
                if not joke(command):
                    if not aerial_distance(command):
                        if not wiki(command):
                            # Performing a google search:
                            pywhatkit.search(command)


if __name__ == "__main__":
    main()
