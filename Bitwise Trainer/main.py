import random, time

def instructions():
    print("Hello there! \n")
    print("Welcome to Bitwise Trainer! \n")
    print("Here, we can learn about Bitwise calculations! \n")
    print("You can also save your progress and high score to challenge yourself! \n")
    print("Hope to see you soon! \n")
    print("The symbols are & and, ^ xor, | or, << left shift, >> right shift \n")

def bitwise_trainer():
    while True:
        score = 0 
        ops = ['&', '|', '^']
        generation1,generation2 = random.randint(0,255),random.randint(0,255)
        operator = random.choice(ops)
        
        if operator == '&': real_ans = generation1 & generation2
        elif operator == '|': real_ans = generation1 | generation2
        else: real_ans = generation1 ^ generation2


instructions()
bitwise_trainer()