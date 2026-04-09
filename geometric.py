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
            successes += 1
            pulls.append(i)
            if firstHit is None:
                firstHit = i

    empMean = sum(pulls) / successes if successes > 0 else 0
    theoMean = 1 / rate
    theoVariance = (1 - rate) / (rate ** 2)

    empSuccessRate = successes / rolls

    pmf = {k: ((1 - rate) ** (k - 1)) * rate for k in range(1, rolls + 1)}
    cdf = {k: 1 - (1 - rate) ** k for k in range(1, rolls + 1)}
    return {
        "total_rolls": rolls,
        "successes": successes,
        "first_success_at": firstHit,
        "success_positions": pulls,
        "empirical_mean": empMean,
        "theoretical_mean": theoMean,
        "theoretical_variance": theoVariance,
        "empirical_success_rate": empSuccessRate,
        "pmf": pmf,
        "cdf": cdf
    }

