import random

computer_choice = random.randint(0, 100)

def ask_for_guess(msg):
  my_guess = int(input(msg))
  if my_guess < computer_choice:
    ask_for_guess("Choose a higher number: ")
  elif my_guess > computer_choice:
    ask_for_guess("Choose a lower number: ")
  else:
    print("You win")
    exit()

ask_for_guess("Choose a number: ")
