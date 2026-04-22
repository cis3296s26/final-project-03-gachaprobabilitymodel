from flask import Flask, request, jsonify, render_template
from Average import Average
from Median import median
from geometric import gachaModel
from FGO import FGOrate, check_fgo_featured, FGORateCalc
from Umamusume import UMArate, check_uma_featured, UMARateCalc
from HoyoverseGames import HoyoverseRate, HoyoversePitySystem, hoyoverseRateCalc
from Histogram import GachaSimulation
import random


app = Flask(__name__)

GAMES = {
    "fgo": {
        "name": "Fate/Grand Order",
        "base_rate": 0.01,
        "cost_per_pull": 3,
        "rate_fn": FGORateCalc,
        "featured_fn": check_fgo_featured,
        "game_type": "fgo"
    },
    "uma": {
        "name": "Uma Musume",
        "base_rate": 0.03,
        "cost_per_pull": 150,
        "rate_fn": UMARateCalc,
        "featured_fn": check_uma_featured,
        "game_type": "uma"
    },
    "genshin": {
        "name": "Genshin Impact",
        "base_rate": 0.006,
        "cost_per_pull": 160,
        "rate_fn": hoyoverseRateCalc,
        "featured_fn": None,
        "game_type": "hoyoverse"
    },
    "hsr": {
        "name": "Honkai: Star Rail",
        "base_rate": 0.006,
        "cost_per_pull": 160,
        "rate_fn": hoyoverseRateCalc,
        "featured_fn": None,
        "game_type": "hoyoverse"
    },
    "zzz": {
        "name": "Zenless Zone Zero",
        "base_rate": 0.006,
        "cost_per_pull": 150,
        "rate_fn": hoyoverseRateCalc,
        "featured_fn": None,
        "game_type": "hoyoverse"
    },
}

@app.route("/")
def home():
    return render_template("ui.html")

@app.route("/select_game/<game_id>")
def select_game(game_id):
    game = GAMES.get(game_id)

    if not game:
        return jsonify({"error": "Game not found"}), 404

    return jsonify(game)

# Currency input and pull calculation
@app.route("/currency", methods=["POST"])
def currency_route():
    data = request.get_json()

    game_id = data.get("game")
    currency = int(data.get("currency", 0))
    tickets = int(data.get("tickets", 0))

    game = GAMES.get(game_id)

    if not game:
        return jsonify({"error": "Game not found"}), 404

    pulls = currency // game["cost_per_pull"] + tickets

    return jsonify({
        "game": game["name"],
        "total_pulls": pulls
    })

# Main probability calculation 
@app.route("/calculate", methods=["POST"])
def calculate():
        data = request.get_json()
        game_id = data.get("game")
        currency = int(data.get("currency", 0))
        tickets = int(data.get("tickets", 0))
        game = GAMES.get(game_id)
        if not game:
            return jsonify({"error": "Game not found"}), 404
        
        # Calculate total pulls
        total_pulls = currency // game["cost_per_pull"] + tickets
        rate = game["base_rate"]
        
        # Use gachaModel to simulate the pulls
        if total_pulls == 0:
            success_positions = []
        else:
            result = gachaModel(
                currency=total_pulls * game["cost_per_pull"],
                cost=game["cost_per_pull"],
                rate=rate,
                seed=random.randint(1, 10000)
            )
            success_positions = result.get("success_positions", []) if result else []
        
        # Calculate statistics
        if success_positions:
            avg_pulls = Average(success_positions)
            median_pulls = median(success_positions)
            probability = (len(success_positions) / total_pulls * 100) if total_pulls > 0 else 0
        else:
            avg_pulls = 0
            median_pulls = 0
            probability = 0
        
        return jsonify({
                "game": game["name"],
                "total_pulls": total_pulls,
                "probability": round(probability, 2),
                "average_pulls": round(avg_pulls, 2),
                "median_pulls": round(median_pulls, 2)
            })

@app.route("/histogram", methods=["POST"])
def histogram():
    data     = request.get_json()
    game_id  = data.get("game", "genshin")
    currency = int(data.get("currency", 3200))
    seed     =  random.randint(1, 10000)

    if game_id not in GAMES:
        return jsonify({"error": f"Unknown game '{game_id}'"}), 400

    cfg = GAMES[game_id]
    sim = GachaSimulation(seed=seed)
    result = sim.simulate_histogram(
        currency=currency,
        cost=cfg["cost_per_pull"],
        rate_fn=cfg["rate_fn"],
        featured_fn=cfg["featured_fn"],
        game_type=cfg["game_type"],
    )
    return jsonify(result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
