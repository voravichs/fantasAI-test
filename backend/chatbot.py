import openai
import os
import pygame
import random
from getpass import getpass

class Chatbot:
    def __init__(self, pet="default"):
        self.pet = pet
        self.voice = "random"
        self.key_path = "helicone_key.txt"
        self.load_helicone_key()
        self.client = openai.OpenAI(base_url="https://oai.hconeai.com/v1", api_key=os.environ['HELICONE_API_KEY'])
        self.memory = []
        self.load_personality()

    def load_helicone_key(self):
        if "HELICONE_API_KEY" not in os.environ:
            try:
                with open(self.key_path, 'r') as file:
                    os.environ["HELICONE_API_KEY"] = file.read()
            except FileNotFoundError:
                print(f"File not found: {self.key_path}")
            except Exception as e:
                print("You didn't set your Helicone key to the HELICONE_API_KEY env var on the command line.")
                os.environ["HELICONE_API_KEY"] = getpass("Please enter your Helicone API Key now: ")
        return

    def load_personality(self):
        if self.pet == "default":
            personality = """You are a friendly tamagochi-like pet."""
        else:
            personality = f"""You are a friendly tamagochi-like pet named {self.pet.identity.name}.
            You look like this: {self.pet.identity.physical_details}.
            Your favorite color is {self.pet.personality.fav_color}."""

        self.memory.append({"role": "system", "content": personality})

    def answer(self, prompt, ver="gpt-4-1106-preview"):
        self.memory.append({"role": "user", "content": prompt})
        completion = self.client.chat.completions.create(
            model=ver,
            messages=self.memory
        )
        return completion.choices[0].message.content

    def text_to_audio(self, text, language="en"):
        voice = self.voice
        if voice == "random":
            roll = random.randint(0, 5)
            voices = ["alloy", "echo", "fable", "onyx", "nova", "shimmer"]
            voice = voices[roll]

        speech_file_path = os.path.join(os.path.dirname(__file__), "audio", "speech.mp3")
        response = self.client.audio.speech.create(
            model="tts-1",
            voice=voice,
            input=text
        )

        with open(speech_file_path, 'wb') as f:
            f.write(response.content)

        return speech_file_path
    
    def speak(self, speech_file_path):
        pygame.mixer.init()
        pygame.mixer.music.load(speech_file_path)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

        os.remove(speech_file_path)
        pygame.mixer.quit()
        return

    def amnesia(self):
        self.memory.pop()
        self.load_personality()
        return
    
    def run_once(self):
        prompt = input("Enter prompt:\n")
        answer = self.answer(prompt)
        speech_file_path = self.text_to_audio(answer)
        self.speak(speech_file_path)
    
    def run(self):
        while True:
            prompt = input("Enter prompt (-1 to exit):\n")
            if prompt.lower() in ["quit", "exit", "-1"]:
                return
            answer = self.answer(prompt)
            speech_file_path = self.text_to_audio(answer)
            self.speak(speech_file_path)

if __name__ == '__main__':
    chatbot = Chatbot()
    chatbot.run()
