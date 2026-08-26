import random
import os

number = random.randint(1, 100)

guess = input("Guess a number between 1 and 100: ")
guess = int(guess)
if guess == number:
    print ("you won!!")
else:
     print ("you lost!! The number was", number)