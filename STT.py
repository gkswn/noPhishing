import speech_recognition as sr

r = sr.Recognizer()
harvard = sr.AudioFile('C:\\Users\\안한주\\Desktop\\노피싱\\중앙지검.wav')

with harvard as source:
    audio = r.record(source)

print(r.recognize_google(audio,language='ko-KR'))