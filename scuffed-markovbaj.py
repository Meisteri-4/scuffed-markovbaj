#!/bin/python
from time import sleep
import markovify
import json
import os
from random import randint
import requests as re
import io
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame.mixer


class Model:
    def __init__(self):
        self.model = None
        if os.path.exists("model.json"):
            self.load_model()
        else:
            self.create_model()
            self.write_model()

    def load_model(self):
        with open("model.json") as file:
            self.model = markovify.Text.from_json(file.read())

    def create_model(self):
        with open("data.json") as file:
            data = " ".join(json.loads(file.read()))
        self.model = markovify.Text(data)
        self.model.compile()

    def write_model(self):
        # creating and compiling a model is slow so we save it to a file
        model_json = self.model.to_json()
        with open("model.json", "w") as file:
            file.write(model_json)

    def make_sentence(self, length: int):
        return self.model.make_short_sentence(length)


def main():
    url = "https://api.streamelements.com/kappa/v2/speech?voice=Brian&text="
    markov = Model()
    pygame.mixer.init()
    print("Running ...")
    freq_start = os.getenv("MARKOV_START")
    freq_end = os.getenv("MARKOV_END")
    if freq_start is None:
        freq_start = 60
    if freq_end is None:
        freq_end = 120
    while True:
        sentence = markov.make_sentence(300)
        resp = re.get(url+sentence, stream=True)
        try:
            sound_file = io.BytesIO(resp.content)
        except Exception:
            continue
        pygame.mixer.Sound(sound_file).play()
        try:
            sleep(randint(freq_start, freq_end))
        except KeyboardInterrupt:
            print()
            quit()


if __name__ == "__main__":
    main()
