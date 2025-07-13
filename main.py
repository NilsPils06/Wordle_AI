import json
import random
import sys
from colorama import Back, Style


def getWords():
    file = open("words.json")
    data = json.load(file)
    words = data["words"]

    return words


def getRandomWord(words):
    index = random.randint(0, len(words) - 1)

    return words[index]


def displayGuess(word, guess):
    out = ["", "", "", "", ""]
    for i in range(len(guess)):
        if guess[i] == word[i]:
            out[i] = Back.GREEN + guess[i] + Style.RESET_ALL
    for i in range(len(guess)):
        if guess[i] in word and out[i] != guess[i]:
            out[i] = Back.YELLOW + guess[i] + Style.RESET_ALL
        else:
            out[i] = guess[i]
    out = "".join(out)
    print(out)


def main():
    print("Welcome to Wordle CLI!")
    print("You have 6 attempts to guess a 5 letter word.")
    words = getWords()
    word = getRandomWord(words)
    guess = ""
    i = 0
    while True:
        if i >= 6:
            print("Sorry, you've used all your attempts. The word was:", word)
            return
        while len(guess) != 5 or guess not in words:
            guess = input()
            sys.stdout.write("\033[F")  # Ga 1 regel omhoog
            sys.stdout.write("\033[K")  # Wis de hele lijn
        displayGuess(word, guess)
        guess = ""
        i += 1
        if guess == word:
            break

    print("Congratulations! You've guessed the word:", word)
    print("You took", i, "attempts to guess the word.")


if __name__ == "__main__":
    main()
