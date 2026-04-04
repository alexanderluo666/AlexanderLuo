import random, time

def instructions():
    print("Hello there! \n")
    print("Welcome to Bitwise Trainer! \n")
    print("Here, we can learn about Bitwise calculations! \n")
    print("You can also save your progress and high score to challenge yourself! \n")
    print("Hope to see you soon!")
    print("The symbols are &, ^, |, <<, >>")

def bitwise_trainer():
    while True:
        score = 0 
        ops = ['&', '|', '^']

instructions()