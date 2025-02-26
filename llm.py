
import openai
import pyttsx3
import requests
import random
import time
import json

# Define the URLs to which the POST requests will be sent
feasibility_url = 'http://127.0.0.1:8000/check_feasible_items/'  # URL to check feasibility
order_url = 'http://127.0.0.1:8000/order_items/'  # URL to place the order
llm_thinking = 'http://127.0.0.1:8000/llm_thinking/'
llm_recording = 'http://127.0.0.1:8000/llm_recording/'

from RealtimeSTT import AudioToTextRecorder
from RealtimeTTS import TextToAudioStream, SystemEngine, GTTSEngine


# Function to read 'openai_key' from the JSON file
def read_openai_key(json_file):
    try:
        # Open the JSON file
        with open(json_file, 'r') as file:
            # Load the JSON data
            data = json.load(file)
            # Access the 'openai_key' value
            openai_key = data.get("openai_key")
            return openai_key
    except FileNotFoundError:
        print(f"Error: {json_file} not found.")
    except json.JSONDecodeError:
        print(f"Error: {json_file} contains invalid JSON.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def read_system_prompts(json_file):
    with open(json_file, 'r') as file:
        data = json.load(file)
        return data["system_prompt_0"], data["system_prompt_1"]
    
system_prompts = read_system_prompts("prompts.json")

engine = SystemEngine() # replace with your TTS engine
# engine = GTTSEngine()

stream = TextToAudioStream(engine)
# engine = pyttsx3.init() # object creation
client = openai.OpenAI(api_key=read_openai_key("openai_key.json"))

def parse_order_with_llm(messages):
    resp = requests.get(llm_thinking + "set")
    system_prompt_0 = system_prompts[0]
    system_prompt_1 = system_prompts[1]

    out_1 = make_api_call(system_prompt_0, messages)
    out_2 = make_api_call(system_prompt_1, messages=[{"role": "user", "content": out_1}])
    try:
        response = eval(out_2)
    except:
        response = {"ORDER":{}, "output":out_2}
    
    order = response["ORDER"]
    done = False
    if len(order) == 0:
        out = out_2
        ai_reply = response["output"]
    else:
        payload = order
        feasibility_response = str(requests.post(feasibility_url, json={'items': payload}).json())
        # print(feasibility_response)
        messages.append({"role":"system", "content":f"""You have sent a request to the backend to check the inventory whether it is possible to\
                                                    complete that order and the return you got was {feasibility_response}. Now continue interacting with the client as previously\
                                                    given that information. Still using the "ORDER":..., "output":... format"""})
        out_3 = make_api_call(system_prompt=system_prompt_0, messages=messages)
        out_4 = make_api_call(system_prompt_1, messages=[{"role": "user", "content": out_3}])
        out = out_4
        try:
            response = eval(out_4)
        except:
            response = {"ORDER":{}, "output":out_4}
        ai_reply = response["output"]
        
        if ai_reply.upper().endswith("DONE"):
            done = True
            ai_reply = ai_reply[:-4]
        elif ai_reply.upper().endswith("DONE."):
            done = True
            ai_reply = ai_reply[:-5]
        

        if done:
            messages = []
            payload = order
            order_response = requests.post(order_url, json={'items': payload, 'tip':round(random.uniform(0, 10), 2)})
    resp = requests.get(llm_thinking + "unset")
    return out, order, ai_reply, messages, done

def make_api_call(system_prompt, messages):
    messages = [{"role": "system", "content": system_prompt}, *messages]

    # Request a chat completion from the OpenAI API based on the conversation so far
    chat_completion = client.chat.completions.create(
        messages=messages,
        model="gpt-4o",  # Specifies using the "gpt-4o" model
        # model = "gpt-4-0314",
    )
    # Extract the response text from the completion
    response_text = chat_completion.choices[0].message.content

    return response_text.strip()

recording = True

def set_recording():
    if stream.is_playing():
        stream.stop()
    resp = requests.get(llm_thinking + "unset")
    resp = requests.get(llm_recording + "set")
def unset_recording():
    resp = requests.get(llm_recording + "unset")


def chatbot_conversation():
    recorder = AudioToTextRecorder(language="en", spinner=False, model="base.en", device="cpu", on_recording_start=set_recording,\
                                    on_recording_stop=unset_recording)
    # recorder = AudioToTextRecorder(language="en", spinner=False)
    print("Here is the MENU: \n")
    ai_reply = ""
    messages = []
    done = False
    listening = True  # Add a flag to control when to listen to user input

    while True:
        user_input = ""
        
        user_input = recorder.text()
        
        if done: 
            user_input = ""
            messages = []
            time.sleep(5)
            done = False
            listening = True  # Reset listening mode when conversation restarts

        if user_input != "":
            print("User input: ", user_input)
            messages.append({"role": "user", "content": user_input})
            raw_r, order, ai_reply, messages, done = parse_order_with_llm(messages)
            messages.append({"role": "assistant", "content": raw_r})

            stream.feed(ai_reply)
            stream.play()
            print("ai reply: ", ai_reply)
            # engine.say(ai_reply)
            # engine.runAndWait()

            if done:
                print("Done!")


"""
def chatbot_conversation():
    recorder = AudioToTextRecorder(language="en", spinner=True, model="base.en", realtime_processing_pause=0.7)
    print("Here is the MENU: \n")
    print(menu)
    ai_reply = ""
    order = ""
    messages = []
    done = False
    while True:
        user_input = ""
        # Listen to user's order
        user_input = recorder.text()
        if done: 
            user_input = ""
            messages = []
            time.sleep(5)
            done = False
        # user_input = input("User: ")
        if user_input != "":
            print("User input: ", user_input)
            messages.append({"role": "user", "content": user_input})
            raw_r, order, ai_reply, messages, done = parse_order_with_llm(messages)
            messages.append({"role":"assistant", "content": raw_r})
            stream.feed(ai_reply)
            stream.play()
            # engine.say(ai_reply)
            # engine.runAndWait()
            # print(ai_reply)
            if done:
                print("Done!")
"""


if __name__ == "__main__":
    chatbot_conversation()
