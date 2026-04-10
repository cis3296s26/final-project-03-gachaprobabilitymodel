import math
import random
from collections import Counter

def gachaModel(currency: int, cost: int, rate: float, seed: int, featuredRate: float = None, checkExternal: float = None): 
    if currency < cost:
        print ("Not enough currency to pull.")
        return None
    random.seed(seed)

    rolls = currency // cost
    pulls = []
    successes = 0
    firstHit = None

    rollResults = []

    for roll in range(1, rolls + 1):
        # Get current rate based on pity system
        currentRate = rateCalculator(roll)
        
        # Check if SSR is hit
        if random.random() < currentRate:
            successes += 1
            pulls.append(roll)
            if firstHit is None:
                firstHit = roll
            
            # Check if it's the featured unit
            isFeatured = False
            featuredName = None
            
            if checkExternal:
                isFeatured, featuredName = checkExternal(roll)
                if isFeatured:
                    featuredSuccesses += 1
                    if firstFeaturedHit is None:
                        firstFeaturedHit = roll

            rollResults.append({
                "roll": roll,
                "success": True,
                "featured": isFeatured,
                "featured_name": featuredName
            })
        else:
            rollResults.append({
                "roll": roll,
                "success": False,
                "featured": False,
                "featured_name": None
            })

    # Calculate statistics
    empMean = sum(pulls) / successes if successes > 0 else 0
    theoMean = 1 / rate
    
    # Calculate average rate for variance
    avgRate = sum(rateCalculator(roll) for roll in range(1, rolls + 1)) / rolls
    theoVariance = (1 - avgRate) / (avgRate ** 2) if avgRate > 0 else 0

    empSuccessRate = successes / rolls
    featuredRateEmp = featuredSuccesses / successes if successes > 0 else 0

    pmf = {k: ((1 - rate) ** (k - 1)) * rate for k in range(1, rolls + 1)}
    cdf = {k: 1 - (1 - rate) ** k for k in range(1, rolls + 1)}
    
    return {
        "total_rolls": rolls,
        "successes": successes,
        "featured_successes": featuredSuccesses,
        "first_success_at": firstHit,
        "first_featured_at": firstFeaturedHit,
        "success_positions": pulls,
        "featured_positions": [r["roll"] for r in rollResults if r.get("is_featured")],
        "empirical_mean": empMean,
        "theoretical_mean": theoMean,
        "theoretical_variance": theoVariance,
        "empirical_success_rate": empSuccessRate,
        "featured_rate_empirical": featuredRateEmp,
        "roll_details": rollResults
    }

