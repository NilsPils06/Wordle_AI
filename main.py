import json
import random
import sys
import os
from colorama import Back, Style

STATS_FILE = "stats.json"
WORDS_FILE = "words.json"


def getWords():
    with open(WORDS_FILE) as file:
        data = json.load(file)
    return data["words"]


def getRandomWord(words):
    return random.choice(words)


def displayGuess(guess, feedback, printOut=True):
    out = ""
    for i in range(len(feedback)):
        if feedback[i] == "g":
            out += Back.GREEN + guess[i] + Style.RESET_ALL
        elif feedback[i] == "y":
            out += Back.YELLOW + guess[i] + Style.RESET_ALL
        else:
            out += guess[i]

    if printOut:
        print(out)
    else:
        return out


def getFeedback(word, guess):
    feedback = ["b"] * 5
    for i in range(5):
        if guess[i] == word[i]:
            feedback[i] = "g"
    for i in range(5):
        if guess[i] in word and feedback[i] != "g":
            feedback[i] = "y"
    return feedback


def filterWords(wordlist, guess, feedback):
    filtered = []
    for word in wordlist:
        match = True
        for i in range(5):
            if feedback[i] == "g" and word[i] != guess[i]:
                match = False
                break
            elif feedback[i] == "y":
                if guess[i] not in word or word[i] == guess[i]:
                    match = False
                    break
            elif feedback[i] == "b":
                if guess[i] in word and guess.count(guess[i]) == 1:
                    match = False
                    break
        if match:
            filtered.append(word)
    return filtered


def load_stats():
    if os.path.exists(STATS_FILE):
        with open(STATS_FILE) as f:
            return json.load(f)
    return {}


def save_stats(stats):
    with open(STATS_FILE, "w") as f:
        json.dump(stats, f, indent=4)


def get_word_score(word, stats):
    data = stats.get(word, {"wins": 0, "attempts": 1})
    return data["wins"] / data["attempts"]


def update_stats(stats, guesses, won):
    if not guesses:
        return
    first = guesses[0]
    if first not in stats:
        stats[first] = {"wins": 0, "attempts": 0}
    stats[first]["attempts"] += 1
    if won:
        stats[first]["wins"] += 1


def get_best_start_word(words, stats):
    scored = [(get_word_score(w, stats), w) for w in words]
    scored.sort(reverse=True)
    return scored[0][1] if scored else random.choice(words)


def simulateAI(word, words, stats, firstGuess):
    print("AI is trying to guess the word...")
    guess = firstGuess
    attempts = 0
    possible_words = words.copy()
    guesses = []

    while attempts < 6:
        feedback = getFeedback(word, guess)
        # print(f"Guess {attempts + 1}: {guess} → {feedback}")
        print(f"Guess {attempts + 1}: {displayGuess(guess, feedback, False)}")
        guesses.append(guess)
        if guess == word:
            print(f"AI guessed the word in {attempts + 1} attempts!")
            update_stats(stats, guesses, True)
            save_stats(stats)
            return
        possible_words = filterWords(possible_words, guess, feedback)
        guess = possible_words[0] if possible_words else ""
        attempts += 1

    print(f"AI failed to guess the word: {word}")
    update_stats(stats, guesses, False)
    save_stats(stats)


def main():
    print("Welcome to Wordle CLI!")
    print(
        "Do you want to (1) play yourself, (2) watch the AI play or (3) train the AI?"
    )
    mode = input("Enter 1, 2 or 3: ").strip()

    words = getWords()
    word = getRandomWord(words)

    if mode != "1":
        stats = load_stats()
        if mode == "2":
            firstGuess = get_best_start_word(words, stats)
            simulateAI(word, words, stats, firstGuess)
        else:
            amount = int(
                input("How many times do you want to train the AI? (in thousands): ")
            )
            for i in range(1000 * amount):
                firstGuess = (
                    get_best_start_word(words, stats)
                    if i % 10 == 0
                    else getRandomWord(words)
                )
                simulateAI(word, words, stats, firstGuess)
                word = getRandomWord(words)
        return

    print("You have 6 attempts to guess a 5 letter word.")
    guess = ""
    i = 0
    while i < 6:
        while len(guess) != 5 or guess not in words:
            guess = input()
            sys.stdout.write("\033[F")
            sys.stdout.write("\033[K")
        feedback = getFeedback(word, guess)
        displayGuess(guess, feedback)
        i += 1
        if guess == word:
            print("Congratulations! You've guessed the word in", i, "attempts.")
            return
        guess = ""
    print("Sorry, you've used all your attempts. The word was:", word)


if __name__ == "__main__":
    main()
