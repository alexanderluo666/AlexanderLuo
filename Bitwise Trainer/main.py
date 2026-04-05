import random, json ;from datetime import datetime #random for generation, datetime for records, and json for saving
import os

FILENAME = "scores.json"

def instructions(start_name):
    print(f"Hello {start_name}! \n")
    print("Welcome to Bitwise Trainer! \n")
    print("Here, we can learn about Bitwise calculations! \n")
    print("You can also save your progress and high score to challenge yourself! \n")
    print("The symbols are & and, ^ xor, | or, << left shift, >> right shift \n")
    print("If you want to quit, just type 'exit'! \n")

DATA_FILE = "data.json"

def add_new_name():

    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w") as f:
            json.dump({"player_names": [], "high_score": 0}, f)


    with open(DATA_FILE, "r") as f:
        data = json.load(f)


    if not data["player_names"]: 
        name = input("Welcome! Enter your primary display name: \n")
        data["player_names"].append(name)
        with open(DATA_FILE, "w") as f:
            json.dump(data, f, indent=4)
    
    return data["player_names"]


all_names = add_new_name()
current_name = all_names[0]
print(f"--- Logged in as: {current_name} --- \n")



def save_score(new_score): #for saving progress using json library, FILENAME is defined at the front
    if os.path.exists(FILENAME):
            with open(FILENAME, "r") as f:
                try:
                    data = json.load(f)
                except json.JSONDecodeError: #prevents errors of decoding
                    data = []
    else: data = []

    dt = datetime.now().strftime("%Y-%m-%d %H:%M")

    data.append({"score": new_score, "date": dt})


    for labels in data:
        labels.pop("status", None) # Clean old labels
    
    if data:
        data[0]["status"] = "ALL-TIME HIGH SCORE"

    data.sort(key=lambda x: x['score'], reverse=True) #sorting using lambda, reverse to get descending order
    

    
    with open(FILENAME, "w") as f:
        json.dump(data[:10], f, indent=4) #only best 10 are displayed to reduce memory usage

def bitwise_trainer():
    score = 0
    name = input("Please enter your name:\n")
    while True:
        ops = ['&', '|', '^']
        generation1,generation2 = random.randint(0,255),random.randint(0,255)
        operator = random.choice(ops)

        if operator == '&': real_ans = (generation1 & generation2) & 0xFF
        elif operator == '|': real_ans = (generation1 | generation2) & 0xFF
        else: real_ans = (generation1 ^ generation2) & 0xFF
        # & 0xFF added so that the answer does not exceed 8-bit binary number limit

        print(f"Question: {generation1} {operator} {generation2}")
        print(f"Binary A: {bin(generation1)[2:].zfill(8)}") #zfill 8 to get 8bit binary(example:00000010)
        print(f"Binary B: {bin(generation2)[2:].zfill(8)}")

        user_input = input("Your answer (in Decimal): ")

        if user_input.lower() == 'exit': #.lower() converts characters into lowercased ones
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
    save_score(score)


instructions(current_name)
bitwise_trainer()
