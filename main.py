import os
from ollama import chat
from pyttsx3 import speak
import json
import speech_recognition as sr
#needs numpy install for sd.rec() but doesnt need import
import sounddevice as sd


#Speech recognition usuing sr and sounddevice
def user_prompt(message_history):
    r = sr.Recognizer()
    sample_rate = 16000
    #length of recording
    duration = 6
    #records the audio from microphone using sound device
    recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='int16')
    sd.wait()
    try:
        #speech recognition takes the auido and returns the translated string 
        audio = sr.AudioData(recording.tobytes(), sample_rate, 2)
        said = r.recognize_google(audio).lower()
        #speech recognition has a hard time with the name TARS so trying to make replace cases
        if "cars" in said:
             said = said.replace("cars", "TARS")
        if "tires" in said:
             said = said.replace("tires", 'TARS')
        if "taurus" in said:
             said = said.replace("taurus", 'TARS')
        if "cards" in said:
            said = said.replace("cards", 'TARS')
        if "guitars" in said:
            said = said.replace("guitars", 'TARS')
        if "charles" in said:
            said = said.replace("charles", 'TARS')
    
        # adds user prompts to the message history for ai context
        message_history.append({"role": "user", "content": f"{said.capitalize()}."})
        print(f"\nYou: {said.capitalize()}.")
        #returns what sr translated 
        return said
    
    except Exception as e:
        print(f"{e}")


#Tars response using ollama 
def tars_response(message_history):
    try:
        # use ollama chat method to get the ai response
        response = chat(model="llama3.2", messages=message_history)
        # filter response to get message
        tars_message = response["message"]["content"]
        # adds tars response to the message history for context
        message_history.append({"role": "assistant", "content": tars_message})
        print(f"\nTARS: {tars_message}")
        # pyttsx5 basic tts speak method 
        speak(tars_message)
    except Exception as e:
        print(f"\nError: {e}\n")


#Writes all chat history to a json file
def save_message_history(message_history):
        try:
            #Writes/rewrites the history.json file to include all message history
            with open("history.json", "w") as file:
                json.dump(message_history, file, indent=4)
        except Exception as e:
            print(f"\nError: {e}\n")


#Speaks a shutdown message, saves the chat history, then exits the app
def shutdown(message_history):
    try:
        shutdown_message = "Powering down! Please dont forget to turn me back on!"
        print(f"\nTARS: {shutdown_message}")
        #tts message
        speak(shutdown_message)
        #adds tars shutdown message to message history
        message_history.append({"role": "assistant", "content": shutdown_message})
        save_message_history(message_history)
    except Exception as e:
        print(f"\nError: {e}\n")


def main():
    #If the history file already exists, read the file and store in message_history
    if os.path.exists("history.json"):
        with open("history.json", "r") as file:
            message_history = json.load(file)
    else:
        #If there is no history file, message history will start with this prompt
        # message history will contain all of the messages between user and TARS
        # first content line is the starting prompt that tells TARS how to act
        message_history = [
            {
                "role": "system",
                "content":
                "You are a helpful assistant named TARS. "
                "You are to be like TARS from the movie interstellar. "
                "Keep answers short and to the point. "
                "Honesty: 90%. "
                "Humor: 75%. "
            }
        ]

    while True:
        try:
            #User input gets appended to history
            prompt = user_prompt(message_history)
            #Look for keywords to shutdown program
            if "shutdown" in prompt or "shut down" in prompt or "powerdown" in prompt or "power down" in prompt:
                shutdown(message_history)
                break
            else:
                #tars response to your prompt
                tars_response(message_history)
                #saves json each chat in case app exits or power goes out the history will still be there
                save_message_history(message_history)
        except Exception as e:
            print("Listening...")



if __name__ == "__main__":
    main()
