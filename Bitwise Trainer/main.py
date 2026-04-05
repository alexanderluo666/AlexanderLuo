import random, json, os;from datetime import datetime
SCORES = "scores.json"
DATA = "data.json"
#import to use libraries, random for generating num; json and os for saving

def instructions(player_id): # Add the ID as an input
    with open(DATA, "r") as D:
        data = json.load(D)
    
    # Find the specific profile that matches the active_id
    user = next((p for p in data["profiles"] if p["id"] == player_id), None)
    name = user["display_name"] if user else "Guest"
    
    print(f"\nHello {name}! (ID: {player_id})")
    print("Welcome to Bitwise Trainer! \n")
    print("Here, we can learn about Bitwise calculations! \n")
    print("You can also save your progress and high score to challenge yourself! \n")
    print("The symbols are & and, ^ xor, | or, << left shift, >> right shift \n")
    print("If you want to quit, just type 'exit'! \n")
    with open(DATA, "r") as D:
        data = json.load(D)
    
    

def add_new_name(new_name):

    if not os.path.exists(DATA):
        with open(DATA, "w") as D:
            json.dump({"profiles": []}, D, indent=4)

    with open(DATA, "r") as D:
        data = json.load(D)


    name_exists = any(p['display_name'].lower() == new_name.lower() for p in data["profiles"])
    
    if name_exists:
        confirm = input(f"The name '{new_name}' is already taken. Use it anyway? (y/n): ")
        if confirm.lower() != 'y':
            new_name = input("Please enter a different name: ")

    

    new_id = len(data["profiles"]) + 1
    new_profile = {
        "id": new_id,
        "display_name": new_name,
        "high_score": 0
    }
    
    data["profiles"].append(new_profile)
    
    with open(DATA, "w") as D:
        json.dump(data, D, indent=4)
    
    print(f"Profile created! Your ID is #{new_id}")
    return new_id



def save_score(player_id, new_score): 
    if os.path.exists(SCORES):
        with open(SCORES, "r") as S:
            try:
                score_data = json.load(S)
            except:
                score_data = []
    else:
        score_data = []

    dt = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    # Save the score LINKED to the ID
    score_data.append({
        "user_id": player_id, 
        "score": new_score, 
        "date": dt
    })

    # Sort and keep top 10
    score_data.sort(key=lambda x: x['score'], reverse=True)
    
    with open(SCORES, "w") as S:
        json.dump(score_data[:10], S, indent=4)



def question_system(player_id): #for number generation
    score = 0
    while True:
        possible_operators = ['&', '|', '^','<<','>>']
        generation1,generation2 = random.randint(0,255),random.randint(0,255)
        if generation1 == generation2: generation2 = random.randint(0,255)
        
        operator = random.choice(possible_operators)

        if operator == '&': real_ans = (generation1 & generation2) & 0xFF
        elif operator == '|': real_ans = (generation1 | generation2) & 0xFF
        elif operator == '^': real_ans = (generation1 ^ generation2) & 0xFF
        elif operator == '<<': real_ans = (generation1 << random.randint(0,4)) &0xFF
        else: real_ans = (generation1 << random.randint(0,4)) &0xFF
        # & 0xFF added so that the answer does not exceed 8-bit binary number limit
        # replaced generation 2 with random.randint(0,4) for <<,>>, to get smaller results
        print(f"Question: {generation1} {operator} {generation2}")
        print(f"Binary A: {bin(generation1)[2:].zfill(8)}") 
        print(f"Binary B: {bin(generation2)[2:].zfill(8)}")
        #zfill 8 to get 8bit binary(example:00000010)
        
        user_input = input("Your answer (in Decimal) / exit: ")

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
    save_score(player_id,score) #when exit is typed, save_score gets used



def show_leaderboard():
    with open(DATA, "r") as D:
        profiles = json.load(D)["profiles"]
    
    with open(SCORES, "r") as S:
        scores = json.load(S)

    print("\n--- GLOBAL TOP 10 ---")
    for s in scores:

        user = next((p for p in profiles if p["id"] == s["user_id"]), None)
        
        name = user["display_name"] if user else "Unknown"
        id_tag = f"#{s['user_id']}"
        
        print(f"[{id_tag}] {name}: {s['score']} pts ({s['date']})")



active_id = add_new_name(input("Please enter your name: "))
instructions(active_id)
question_system(active_id)
