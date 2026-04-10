import random
def UMArate(rolls):

    chance = 0.03

    if rolls >= 200:
        return 1.0

    return chance

def check_uma_featured(roll, SSRcount = 0, guaranteed = False):
    featuredChance = 0.225  # 22.5% chance for featured. 
                            # 3% * 0.75% is the chance of getting the fatured item
    
    if guaranteed:
        isFeatured = True
    else:
        isFeatured = random.random() < featuredChance

    character = "Featured SSR" if isFeatured else "Off-rate SSR"

    return isFeatured, character

def UMARateCalc(roll, pityCounter=None):
    return UMArate(roll)