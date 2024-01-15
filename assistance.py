from neuralintents import GenericAssistant
import speech_recognition
import pyttsx3 as tts
import sys

recogniser = speech_recognition.Recognizer()

speaker = tts.init()
speaker.setProperty('rate', 150)

todo_list = ['Go Shopping', 'Clean Room', 'Record Video']


def hello():
    speaker.say('Hello, what can i do for you?')
    speaker.runAndWait()


def quit():
    speaker.say('it was nice talking to you ngali. have a great day')
    speaker.runAndWait()
    sys.exit(0)


mappings = {
    'greetings': hello,
    'goodbye': quit()
}

assistance = GenericAssistant('intents.json', intent_methods=mappings)
assistance.train_model()

while True:
    try:
        with speech_recognition.Microphone() as mic:

            recogniser.adjust_for_ambient_noise(mic, duration=0.2)
            audio = recogniser.listen(mic)

            message = recogniser.recognize_google(audio)
            message = message.lower()

            assistance.request(message)
    except speech_recognition.UnknownValueError:
        recogniser = speech_recognition.Recognizer()