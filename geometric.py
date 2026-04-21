import math
import random
import Average
import Median
from collections import Counter

def gachaModel(
    currency: int,
    cost: int,
    rate: float,
    seed: int,
    featuredRate: float = None,
    checkExternal = None
):
    if currency < cost:
        print("Not enough currency to pull.")
        return None

    random.seed(seed)

    rolls = currency // cost
    pulls = []
    successes = 0
    firstHit = None
    featuredSuccesses = 0
    firstFeaturedHit = None
    rollResults = []

    for roll in range(1, rolls + 1):
        currentRate = rateCalculator(roll)

        if random.random() < currentRate:
        # Check if SSR is hit
            successes += 1
            pulls.append(roll)

            if firstHit is None:
                firstHit = roll

            isFeatured = False
            featuredName = None

            if featuredRate is not None:
                if random.random() < featuredRate:
                    isFeatured = True
                    featuredName = "Featured Unit"
                    featuredSuccesses += 1
                    if firstFeaturedHit is None:
                        firstFeaturedHit = roll
                else:
                    isFeatured = False
                    featuredName = "Off rate Unit"

            elif checkExternal is not None:
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

    empMean = Average(pulls) if successes > 0 else 0
    empMedian = Median(pulls) if successes > 0 else 0
    theoMean = 1 / rate

    rates = [rateCalculator(roll) for roll in range(1, rolls + 1)]
    avgRate = Average(rates) if len(rates) > 0 else 0
    theoVariance = (1 - avgRate) / (avgRate ** 2) if avgRate > 0 else 0
    
    # Calculate variance
    theoVariance = (1 - rate) / (rate ** 2) if rate > 0 else 0

    empSuccessRate = successes / rolls if rolls > 0 else 0
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
        "featured_positions": [r["roll"] for r in rollResults if r.get("featured")],
        "empirical_mean": empMean,
        "empirical_median": empMedian,
        "theoretical_mean": theoMean,
        "theoretical_variance": theoVariance,
        "empirical_success_rate": empSuccessRate,
        "featured_rate_empirical": featuredRateEmp,
        "pmf": pmf,
        "cdf": cdf,
        "roll_details": rollResults
    }
