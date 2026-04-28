import random, json, os;from datetime import datetime
SCORES = "scores.json"
DATA = "data.json"
#import to use libraries, random for generating num; json and os for saving

def instructions(player_id): # Add the ID as an input to indicate player
    with open(DATA, "r") as D:
        data = json.load(D)
    
    # Find the specific profile that matches the active_id
    user = next((p for p in data["profiles"] if p["id"] == player_id), None)
    name = user["display_name"] if user else "Unknown"
    
    print(f"\nHello {name}! (ID: {player_id})")
    print("Welcome to Bitwise Trainer! \n")
    print("Here, we can learn about Bitwise calculations! \n")
    print("You can also save your progress and high score to challenge yourself! \n")
    print("The symbols are & and, ^ xor, | or, << left shift, >> right shift \n")
    print("If you want to quit, just type 'exit'! \n")
    with open(DATA, "r") as D:
        data = json.load(D)
    
    

def add_new_name(new_name): #creates name for profile; links with select_or_create_profile

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
            except json.JSONDecodeError:
                score_data = []
    else:
        score_data = []

    dt = datetime.now().strftime("%Y-%m-%d %H:%M")
    score_data.append({"user_id": player_id, "score": new_score, "date": dt})
    
    # Sort and keep top 10
    score_data.sort(key=lambda x: x['score'], reverse=True)
    with open(SCORES, "w") as S:
        json.dump(score_data[:10], S, indent=4)


    if os.path.exists(DATA):
        with open(DATA, "r") as D:
            user_data = json.load(D)


        for profile in user_data["profiles"]:
            if profile["id"] == player_id:

                profile["games_played"] = profile.get("games_played", 0) + 1
                

                if new_score > profile.get("high_score", 0):
                    profile["high_score"] = new_score
                    print(f"!!! NEW PERSONAL BEST: {new_score} !!!")
                break


        with open(DATA, "w") as D:
            json.dump(user_data, D, indent=4)



def question_system(player_id): #for number generation
    score = 0
    while True:
        possible_operators = ['&', '|', '^','<<','>>']
        generation1,generation2 = random.randint(0,255),random.randint(0,255)
        if generation1 == generation2: generation2 = random.randint(0,255)
        
        operator = random.choice(possible_operators)
        lrshift = random.randint(0,4)


        if operator == '&': real_ans = (generation1 & generation2) & 0xFF
        elif operator == '|': real_ans = (generation1 | generation2) & 0xFF
        elif operator == '^': real_ans = (generation1 ^ generation2) & 0xFF
        elif operator == '<<': real_ans = (generation1 << lrshift) &0xFF
        else: real_ans = (generation1 >> lrshift) &0xFF
        # & 0xFF added so that the answer does not exceed 8-bit binary number limit
        # replaced generation 2 with random.randint(0,4) for <<,>>, to get smaller results
        
        if operator == '>>' or operator == '<<':
            print(f"Question: {generation1} {operator} {lrshift}")
            print(f"Binary A: {bin(generation1)[2:].zfill(8)}") 
            print(f"Binary B: {bin(lrshift)[2:].zfill(8)}")
        else:
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
        data = json.load(D)
    
    # Sort by high score as usual
    sorted_profiles = sorted(data["profiles"], key=lambda x: x.get('high_score', 0), reverse=True)

    print("\n--- BITWISE TRAINER LEADERBOARD ---")
    for i, p in enumerate(sorted_profiles[:10], 1):
        name = p['display_name']
        score = p.get('high_score', 0)
        games = p.get('games_played', 0)
        
        # Displaying name, score, and total games side-by-side
        print(f"{i}. {name:<15} | Best: {score:>4} pts | Games: {games}")



def select_or_create_profile(): #creates profile


    if not os.path.exists(DATA):
        return add_new_name(input("First time setup! Enter your name: "))

    with open(DATA, "r") as D:
        data = json.load(D)
    
    profiles = data.get("profiles", [])

    if not profiles:
        return add_new_name(input("No profiles found. Enter your name: "))

    print("\n=== BITWISE TRAINER LOGIN ===")
    for p in profiles:
        print(f"[{p['id']}] {p['display_name']} (Best: {p.get('high_score', 0)})")
    print("[N] Create New Profile")

    while True:
        choice = input("\nSelect ID or 'N': ").strip().upper()
        
        if choice == 'N':
            return add_new_name(input("Enter new name: "))
        
        try:
            p_id = int(choice)
            if any(p['id'] == p_id for p in profiles):
                return p_id
            print("ID not found.")
        except ValueError:
            print("Please enter a number or 'N'.")



    show_leaderboard()


def main():
    try:
        show_leaderboard()
    except FileNotFoundError:
        exit
    active_id = select_or_create_profile()
    instructions(active_id)
    question_system(active_id)

    
main()