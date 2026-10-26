from groq import Groq
import json
import time
import os
import pyttsx3
import re
import webbrowser as wb

client = Groq(
    api_key = "Your Groq API Key"
)

engine = pyttsx3.init()

conversation = []

features = {

    "/exit" : "To end the conversation",
    "/save" : "To create a new file and save a conversation",
    "/load" : "To load a saved conversation",
    "/delete" : "To delete a saved conversation",
    "/history" : "To see conversation history",
    "/openW" : "To enter any website",
    "/Cmode" : "To change the model"
}

Available_models = {

    0 :"openai/gpt-oss-20b",
    1 : "openai/gpt-oss-120b",
    2 : "openai/gpt-oss-safeguard-20b",
    3 : "qwen/qwen3.8-27b",

}

select_mode = 0

def commands(user_input):

        if user_input == "/exit":

            return "exit"

        if user_input == "/help":

            for feature, use in features.items():
                print(f"{feature} : {use}")
            return

        if user_input == "/history":

            for message in conversation:
                print(f"{message['role']} : {message['content']}")
            return

        if user_input == "/save":

            file_name = input("Enter file name: ")
            with open(r"C:\Users\jhaan\OneDrive\Desktop\Python\\" + file_name + ".json", "w") as file:
                json.dump(conversation, file, indent=4)
            print("Saved to Desktop!")
            return

        if user_input == "/load":

            load_file = input("Enter file name or path: ")
            with open(load_file , 'r') as file:
                data = json.load(file)
            for message in data:
                print(f"{message['role']} : {message['content']}")
            return

        if user_input == "/delete":

            delete_file = input("Enter file name or path to delete: ")

            try:
                os.remove(delete_file)
                print(f"{delete_file} has been successfully deleted!")

            except FileNotFoundError:
                print(f"{delete_file} does not exists!")

            except Exception as e:
                print(f"An unexpected error occurred: {e}")

            return

        if user_input == "/openW":

            enter_website = input("Enter website you want to go: ").lower()
            wb.open("https://www."+ enter_website)
            return

        if user_input == "/Cmode":

            global select_mode

            for modes, use in Available_models.items():
                print(f"{modes} : {use}")

            try:
                select_mode = int(input("Enter the number of mode from above list[0 - 3]: "))

            except ValueError:
                print("Enter an integer!")
                return

            if select_mode not in Available_models:
                print("Please enter a number between 0 and 5!")
                return

            return select_mode
        
def model():
        
        conversation.append({
        "role": "user",
        "content": user_input
    })

        response = client.chat.completions.create(
        model = Available_models[select_mode],
        messages = conversation
    )
        
        answer = response.choices[0].message.content

        clean_answer = re.sub(r'[*&$#@/_\-"\(\)\[\]]', ' ', answer)
        print("Front:", answer)
        engine.say(clean_answer)
        engine.runAndWait()

        conversation.append({

            "role": "assistant",
            "content": answer
        })

Days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

while True:

    print("")
    now = time.localtime()
    print("Using model:", Available_models[select_mode])
    print(f"Year: {now.tm_year} - Day: {Days[now.tm_wday]} - Hour: {now.tm_hour} - Minute: {now.tm_min} - Seconds: {now.tm_sec}")
    user_input = input("You: ")

    result = commands(user_input)

    if result == "exit":
        break

    if user_input == "/Cmode" and isinstance(result, int):
        select_mode = result

    if user_input.startswith("/"):
        continue

    model()
