import shutil
from os.path import exists
from os import remove

def load_dict():
    path = 'data/wordle-answers-alphabetical.txt'
    session = 'data/session.txt'
    if(exists(session)):
        with open(session) as f:
            answers = f.read().splitlines()
        return answers
    else:
        with open(path) as f:
            answers = f.read().splitlines()
            session_copy = shutil.copy(path, session)
        return answers

def write_dict(contents):
    session = 'data/session.txt'
    with open(session, "w") as f:
        f.truncate(0)
        for x in contents:
            f.write(x + "\n")

def solve(guess):
    answers = load_dict()
    for element in guess:
        if None in element:
            answers = [x for x in answers if element[0] not in x]
        elif len(element) == 3:
            answers = [x for x in answers if element[0] != x[element[1]]]
            answers = [x for x in answers if element[0] in x]
        else:
            answers = [x for x in answers if element[0] == x[element[1]]]

    write_dict(answers)
    print("Possible answers:\n")
    for ans in answers:
        print(f"* {ans}\n")
            

def process_chars(word):
    word = word.lower()
    guess = []
    print(f"You entered: {word}\n")
    print("For each letter, enter one of the following: \n\t'b' - black (not in word)\n\t'y' - yellow (in word, incorrect position)\n\t'g' - green (correct position)\n")
    for i in range(0, len(word)):
        valid = False
        while not valid:
            status = input(f"Enter the color of the letter '{word[i]}': ")
            if status.lower() == 'b':
                guess.append((word[i], None))
                valid = True
            elif status.lower() == 'y':
                guess.append((word[i], i, 'not'))
                valid = True
            elif status.lower() == 'g':
                guess.append((word[i], i))
                valid = True
            else:
                print("Invalid. Please choose 'b', 'y', or 'g'.")
    solve(guess)

def main():
    tmp_file = 'data/session.txt'
    if exists(tmp_file):
        remove(tmp_file)

    n_guess = 1

    while n_guess <= 6:
        attempt = input("Enter the word you guessed, or -q to quit: ")
        if attempt.lower() != "-q":
            process_chars(attempt)
        else:
            exit()
        n_guess += 1

main()