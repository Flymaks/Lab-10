import json, time
import requests
import pyttsx3, pyaudio, vosk



class Speech:
    def __init__(self):
        self.speaker = 0
        self.tts = pyttsx3.init('sapi5')

    def set_voice(self, speaker):
        self.voices = self.tts.getProperty('voices')
        for count, voice in enumerate(self.voices):
            if count == 0:
                print('0')
                id = voice.id
            if speaker == count:
                id = voice.id
        return id

    def text2voice(self, speaker=0, text='Готов'):
        self.tts.setProperty('voice', self.set_voice(speaker))
        self.tts.say(text)
        self.tts.runAndWait()


class Recognize:
    def __init__(self):
        model = vosk.Model('model_small')
        self.record = vosk.KaldiRecognizer(model, 16000)
        self.stream()

    def stream(self):
        pa = pyaudio.PyAudio()
        self.stream = pa.open(format=pyaudio.paInt16,
                         channels=1,
                         rate=16000,
                         input=True,
                         frames_per_buffer=8000)


    def listen(self):
        while True:
            data = self.stream.read(4000, exception_on_overflow=False)
            if self.record.AcceptWaveform(data) and len(data) > 0:
                answer = json.loads(self.record.Result())
                if answer['text']:
                    yield answer['text']


def speak(text):
    speech = Speech()
    speech.text2voice(speaker=1, text=text)


def get_random_user():
    response = requests.get("https://randomuser.me/api/")
    data = response.json()
    user = data["results"][0]
    return {
        "name": f"{user['name']['first']} {user['name']['last']}",
        "country": user['location']['country'],
        "picture": user['picture']['large']
    }

def save_image(current_user):
    filename=f"{current_user['name']}_photo.jpg"
    response = requests.get(current_user['picture'])
    with open(filename, "wb") as f:
        f.write(response.content)

def main():
    current_user = 0
    rec = Recognize()
    text_gen = rec.listen()
    rec.stream.stop_stream()
    speak('Starting')
    time.sleep(0.5)
    rec.stream.start_stream()
    for text in text_gen:
        if text == "закрыть":
            speak('Bye bye')
            break
        elif text == "создать":
            current_user = get_random_user()
            speak("User was created")
        elif text == "имя":
            if current_user:
                speak(f"name is: {current_user['name']}")
            else:
                speak("First you need create a user")
        elif text == "страна":
                if current_user:
                    speak(f"Country is: {current_user['country']}")
                else:
                    speak("First you need create a user")
            
        elif text == "анкета":
            if current_user:
                speak("form:")
                speak(f"name: {current_user['name']}")
                speak(f"country: {current_user['country']}")
            else:
                speak("First you need create a user")
            
        elif text == "сохранить":
            if current_user:
                save_image(current_user)
                speak(f"image was saved as {current_user['name']}_photo.jpg")
            else:
                speak("First you need create a user")
        else:
            print(text)
            speak("command not recognized")

if __name__ == "__main__":
    main()