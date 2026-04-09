def FGO(rolls):

    chance_per_pull = 3
    featured_rate = 0.75

    if rolls >= 200:
        featured_chance = 100
    else:
        featured_chance = 100 - (100 - featured_rate) ** rolls
        unit_chance = 100 - (100 - chance_per_pull) ** rolls

    return {
        "featured SSR probability": featured_chance,
        "other SSR probability": unit_chance
    }