import geometric
from flask import Flask, request, jsonify
def HoyoverseGames(rolls):
    chance = 0.0
    if rolls < 75:
        chance = 0.6
    elif rolls >= 90:
        chance = 100.0
    else:
        chance = 0.6 + (6 * (rolls - 74))

    return chance