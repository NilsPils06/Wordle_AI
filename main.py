import json
import random

correct = dict()
correct["green"] = ["", "", "", "", ""]
correct["yellow"] = []
incorrect = set()


def getWords():
    file = open("words.json")
    data = json.load(file)
    words = data["words"]

    return words


def getRandomWord(words):
    index = random.randint(0, len(words) - 1)

    return words[index]


def updateCorrectLetters(word, guess):
    for i in range(len(guess)):
        c = guess[i]
        if guess[i] == word[i]:
            correct["green"][i] = c
        elif c in word:
            count = word.count(c)
            count -= correct["green"].count(c)
            count -= correct["yellow"].count(c)

            if count > 0:
                correct["yellow"].append(c)
        else:
            incorrect.add(c)


def main():
    print("Welcome to Wordle CLI!")
    words = getWords()
    word = getRandomWord(words)
    guess = ""
    while len(guess) != 5 or guess not in words:
        guess = input("Guess a 5 letter word: ")
    i = 1
    while guess != word:
        if i >= 6:
            print("Sorry, you've used all your attempts. The word was:", word)
            return
        print("Incorrect guess. Try again.")
        print("Attempt", i, "of 6.")
        updateCorrectLetters(word, guess)
        guess = ""
        print("Correct letters in green:", correct.get("green", []))
        print("Correct letters in yellow:", correct.get("yellow", []))
        print("Incorrect letters:", list(incorrect))
        while len(guess) != 5 or guess not in words:
            guess = input("Guess a 5 letter word: ")
        i += 1
    else:
        print("Congratulations! You've guessed the word:", word)
        print("You took", i, "attempts to guess the word.")


if __name__ == "__main__":
    main()
