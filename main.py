from ollama import chat
import pyttsx3

username = input("Enter Your Name: ")
# message history will contain all of the messages between user and TARS
# first content line is the starting prompt that tells TARS how to act
message_history = [
    {
        "role": "system",
        "content":
            "You are a helpful assistant named TARS. "
            f"My name is {username} so please refer to me by it"
            "You are to be like TARS from the movie interstellar."
            "Keep answers short and to the point."
            "Honesty: 90%"
            "Humor: 75%"
    }
]


def tars_response():
    try:
        # use ollama chat method to get the ai response
        response = chat(model="llama3.2", messages=message_history)
        # filter response to get message
        tars_message = response["message"]["content"]
        # adds tars response to the message history for context
        message_history.append({"role": "assistant", "content": tars_message})
        print(f"\nTARS: {tars_message}")
        #pyttsx5 basic tts block
        engine = pyttsx3.init()
        engine.say(tars_message)
        engine.runAndWait()

    except Exception as e:
        print(f"\nError: {e}\n")


def user_prompt():
    user_prompt = input("\nYou: ").lower()
    # adds user prompts to the message history for ai context
    message_history.append(
        {"role": "user", "content": f"{user_prompt.capitalize()}."})
    return user_prompt


def main():
    while True:
        prompt = user_prompt()
        if "exit" in prompt:
            print(f"\nTars: Goodbye {username}!")
            break
        tars_response()


if __name__ == "__main__":
    main()
