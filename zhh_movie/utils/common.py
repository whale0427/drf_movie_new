import random

def random_number(number):
    rn=""
    for _ in range(number):
        rn+=str(random.randint(1,9))
    return rn