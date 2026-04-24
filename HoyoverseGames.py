def HoyoverseRate(roll, pitySSR=False):
    if roll < 75:
        chance = 0.006
    elif roll >= 90:
        chance = 1.0
    else:
        chance = 0.006 + (0.06 * (roll - 74))
    return chance

# Pity rule for SSR if previous is not featured then next SSR is guaranteed to be featured
def HoyoversePitySystem(roll, previousSSRcount=0, lastFeaturedRoll=None):
    featuredChance = 0.5
    #  Checks the last featured roll was 90 or more rolls ago, guaranteeing the next SSR is featured
    if lastFeaturedRoll is not None and roll - lastFeaturedRoll >= 90:
        return 1.0
    elif previousSSRcount > 0 and lastFeaturedRoll is not None and (roll - lastFeaturedRoll) >= 75:
        return 1.0
    
    return featuredChance

def hoyoverseRateCalc(roll, pityCounter=None):
    return HoyoverseRate(roll)