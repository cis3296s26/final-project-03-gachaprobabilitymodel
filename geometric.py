import math
import random
from collections import Counter

def gachaModel(currency: int, cost: int, rate: float, seed: int): 
    if currency < cost:
        print ("Not enough currency to pull.")
    random.seed(seed)

    rolls = currency // cost
    pulls = []
    successes = 0
    firstHit = None

    for i in range (1 , rolls + 1):
        if random.random() < rate:
            int = 0