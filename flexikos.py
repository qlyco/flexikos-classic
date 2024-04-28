import os
import json
import random
from collections import Counter
import requests

tile_counts: dict = {
  "A": 9, "B": 2, "C": 2, "D": 4, "E": 12, "F": 2, "G": 3, "H": 2, "I": 9,
  "J": 1, "K": 1, "L": 4, "M": 2, "N": 6, "O": 8, "P": 2, "Q": 1, "R": 6,
  "S": 4, "T": 6, "U": 4, "V": 2, "W": 2, "X": 1, "Y": 2, "Z": 1
}

tiles: list = []
hand: list = []
words: dict = {}
answers: list = []
score: int = 0

def init():
  global words, tiles

  res: requests.Response = requests.get("https://app-data.fly.dev/api/v2/seed")

  if res.status_code == 200:
    seed: str = res.json()["seed"]
    random.seed(seed)
  else:
    os.exit(-1)

  with open("words.json") as word_list:
    words = json.load(word_list)

  for letter, count in tile_counts.items():
    tiles.extend([letter] * count)

  random.shuffle(tiles)

def draw():
  global tiles, hand

  tiles = hand + tiles
  hand = []

  if len(tiles) > 12:
    hand, tiles = tiles[:(12-len(hand))], tiles[(12-len(hand)):]
  elif len(tiles) <= 12:
    hand, tiles = tiles[:(len(tiles)-len(hand))], tiles[(len(tiles)-len(hand)):]

def verify(guess: str):
  global words, hand

  valid_tiles: list = hand
  count: Counter = Counter(valid_tiles)

  valid: bool = all(count[k] - v >= 0 for k, v in Counter(guess).items())

  if guess in list(words.keys()) and valid:
    for letter in guess:
      hand.remove(letter)
    return True
  else:
    return False

def has_move():
  global words, hand

  valid_tiles: list = hand
  count: Counter = Counter(valid_tiles)

  for word in words.keys():
    if all(count[k] - v >= 0 for k, v in Counter(word).items()):
      return True

  return False

def game():
  global score

  guess: str = ""

  draw()

  while True:
    print("TILES: " + str(hand) + " (" + str(len(tiles)) + " tiles left)")
    print("Score: " + str(score) + " pts")

    if not has_move():
      print("\nNo more moves.\n")
      break

    guess = input("\nType in your word: ")

    if guess == "/exit":
      break

    if guess.isalpha() and verify(guess.upper()):
      answers.append(guess.upper())
      score += words[guess.upper()]
      print("\n" + guess.upper() + " = " + str(words[guess.upper()]) + " pts\n")
      draw()
    else:
      print("\nInvalid word.\n")

def main():
  init()
  game()

if __name__ == "__main__":
  main()
