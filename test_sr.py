from RealtimeSTT import AudioToTextRecorder
import pyautogui

def process_text(text):
    print(text)

if __name__ == '__main__':
    print("Wait until it says 'speak now'")
    recorder = AudioToTextRecorder(spinner=False, language="en", device="cpu")

    while True:
        recorder.text(process_text)