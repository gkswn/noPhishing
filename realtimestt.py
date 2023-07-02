# -*- coding: utf-8 -*-

import speech_recognition as sr
import sys

r = sr.Recognizer()

with sr.Microphone() as source:
    print("Say something! : ")
    audio = r.listen(source)
print(repr(r.recognize_google(audio, language='ko-KR')))