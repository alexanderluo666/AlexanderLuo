import random,datetime,json #random for generation, datetime for records, and json for saving
import json
import os

FILENAME = "scores.json"

def instructions():
    print("Hello there! \n")
    print("Welcome to Bitwise Trainer! \n")
    print("Here, we can learn about Bitwise calculations! \n")
    print("You can also save your progress and high score to challenge yourself! \n")
    print("The symbols are & and, ^ xor, | or, << left shift, >> right shift \n")
    print("If you want to quit, just type 'exit'! \n")

def save_score(new_score): #for saving progress using json library, FILENAME is defined at the front
    if os.path.exists(FILENAME):
            with open(FILENAME, "r") as f:
                data = json.load(f)
    else:
            data = [] 

    time = datetime.now().strftime("%Y-%m-%d %H:%M")
    data.append({"score": new_score, "date": time})


    with open(FILENAME, "w") as f:
        json.dump(data, f, indent=4)

def bitwise_trainer():
    score = 0
    while True:
        ops = ['&', '|', '^']
        generation1,generation2 = random.randint(0,255),random.randint(0,255)
        operator = random.choice(ops)

        if operator == '&': real_ans = generation1 & generation2
        elif operator == '|': real_ans = generation1 | generation2
        else: real_ans = generation1 ^ generation2

        print(f"Question: {generation1} {operator} {generation2}")
        print(f"Binary A: {bin(generation1)[2:].zfill(8)}") #zfill 8 to get 8bit binary(example:00000010)
        print(f"Binary B: {bin(generation2)[2:].zfill(8)}")

        user_input = input("Your answer (in Decimal): ")

        if user_input.lower() == 'exit': #.lower() converts characters into lowercased ones
            save_score(score)
            break #exits

        try:
            if int(user_input) == real_ans:
                print("Correct!\n")
                score += 1
            else:
                print(f"Wrong! The answer was {real_ans} ({bin(real_ans)[2:].zfill(8)})\n")
        except ValueError:
            print("Please enter a valid number.\n")
        finally:
            print(f"Final Score: {score}")


instructions()
bitwise_trainer()