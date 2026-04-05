import random, json, os;from datetime import datetime
SCORES = "scores.json"
DATA = "data.json"
#import to use libraries, random for generating num; json and os for saving

def instructions(start_name):
    print(f"Hello {start_name}! \n")
    print("Welcome to Bitwise Trainer! \n")
    print("Here, we can learn about Bitwise calculations! \n")
    print("You can also save your progress and high score to challenge yourself! \n")
    print("The symbols are & and, ^ xor, | or, << left shift, >> right shift \n")
    print("If you want to quit, just type 'exit'! \n")



def add_new_name(): #for saving user using json library

    if not os.path.exists(DATA):
        with open(DATA, "w") as f:
            json.dump({"player_names": [], "high_score": 0}, f)


    with open(DATA, "r") as f:
        data = json.load(f)


    if not data["player_names"]: 
        name = input("Welcome! Enter your primary display name: \n")
        data["player_names"].append(name)
        with open(DATA, "w") as f:
            json.dump(data, f, indent=4)
    
    return data["player_names"]



def save_score(new_score): #for saving progress using json library
    if os.path.exists(SCORES):
            with open(SCORES, "r") as f:
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
    

    
    with open(SCORES, "w") as f:
        json.dump(data[:10], f, indent=4) #only best 10 are displayed to reduce memory usage



def generation(): #for number generation
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



all_names = add_new_name()
current_name = all_names[0]
print(f"--- Logged in as: {current_name} --- \n")

instructions(current_name)
generation()
