import random


def generate_random_token():

    chars = '1234567890'
    password = ""
    for i in range(25):
        password += random.choice(chars)
    return password