import random
def FGOrate(rolls):

    chance = 0.01

    if rolls >= 330:
        return 1.0

    return chance

def check_fgo_featured(roll, SSRcount = 0, guaranteed = False):
    featuredChance = 0.8  # 80% chance for featured
    
    if guaranteed:
        isFeatured = True
    else:
        isFeatured = random.random() < featuredChance

    character = "Featured SSR" if isFeatured else "Off-rate SSR"

    return isFeatured, character

def FGORateCalc(roll, pityCounter=None):
    return FGOrate(roll)