import json

tile_counts: dict = {
  "A": 9, "B": 2, "C": 2, "D": 4, "E": 12, "F": 2, "G": 3, "H": 2, "I": 9,
  "J": 1, "K": 1, "L": 4, "M": 2, "N": 6, "O": 8, "P": 2, "Q": 1, "R": 6,
  "S": 4, "T": 6, "U": 4, "V": 2, "W": 2, "X": 1, "Y": 2, "Z": 1
}

tile_values: dict = {
  "A": 1, "E": 1, "I": 1, "O": 1, "U": 1, "L": 1, "N": 1, "S": 1, "T": 1, "R": 1,
  "D": 2, "G": 2,
  "B": 3, "C": 3, "M": 3, "P": 3,
  "F": 4, "H": 4, "V": 4, "W": 4, "Y": 4,
  "K": 5,
  "J": 8, "X": 8,
  "Q": 10, "Z": 10
}

def main():
  with open("wordlist.txt") as file:
    data: set = set(file)

    out: dict = {}

    for word in data:
      word = word.replace("\"", "").strip()

      if len(word) >= 3 and len(word) < 13:
        valid: bool = False
        word_val: int = 0

        for letter in word:
          if word.count(letter) <= tile_counts[letter.upper()] + 2:
            valid = True

          word_val += tile_values[letter.upper()]

        if valid:
          out[word.upper()] = word_val

    with open("words.json", "w") as words:
      json.dump(out, words)

if __name__ == "__main__":
  main()
