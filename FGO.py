def FGO(rolls):

    chance_per_pull = 1
    featured_rate = 0.8

    if rolls >= 330:
        featured_chance = 100
    else:
        featured_chance = 100 - (100 - featured_rate) ** rolls
        unit_chance = 100 - (100 - chance_per_pull) ** rolls

    return {
        "featured SSR probability": featured_chance,
        "other SSR probability": unit_chance
    }