from flask import Flask, request, jsonify
from Average import Average
from Median import median
from geometric import gachaModel
from FGO import FGOrate
from Umamusume import UMArate
import random

app = Flask(__name__)

GAMES = {
    "fgo": {"name": "Fate/Grand Order", "base_rate": 0.01, "cost_per_pull": 3},
    "uma": {"name": "Uma Musume", "base_rate": 0.03, "cost_per_pull": 150},
    "hoyverse": {"name": "Honkai: Star Rail", "base_rate": 0.06, "cost_per_pull": 160},
}

@app.route("/")
def home():
    with open("ui.html") as f:
        return f.read()
    
# Game selection
@app.route("/select_game/<game_id>")
def select_game(game_id):
    game = GAMES.get(game_id)
    if not game:
        return "Game not found", 404
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
        return "Game not found", 404
    pulls = currency // game["cost_per_pull"] + tickets
    return jsonify({"game": game["name"], "total_pulls": pulls})

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
        result = gachaModel(
            currency=currency if currency > 0 else game["cost_per_pull"],
            cost=game["cost_per_pull"],
            rate=rate,
            seed=random.randint(1, 10000)
        )
        
        # Extract success positions from result
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
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)