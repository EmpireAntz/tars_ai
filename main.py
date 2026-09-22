import os
from ollama import chat
from pyttsx3 import speak
import json

#User input currently terminal text input
def user_prompt(message_history):
    user_prompt = input("\nYou: ").lower()
    # adds user prompts to the message history for ai context
    message_history.append(
        {"role": "user", "content": f"{user_prompt.capitalize()}."})
    return user_prompt

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


if __name__ == "__main__":
    main()
