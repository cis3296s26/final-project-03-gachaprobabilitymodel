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
        pulls = currency // game["cost_per_pull"] + tickets
        rate = game["base_rate"]

        prob_cards =[]
        for i in range(pulls):
             chance = (1 - (1 - rate) ** (i + 1)) * 100
             prob_cards.append(chance)
        
        # Call gachaModel with proper parameters
        # gachaModel(currency, cost, rate, seed)
        result = gachaModel(
            currency=currency if currency > 0 else game["cost_per_pull"],
            cost=game["cost_per_pull"],
            rate=game["base_rate"],
            seed=random.randint(1, 10000)
        )
        
        # Extract values from result
        probability = result.get("empirical_success_rate", 0)
        avg_pulls = result.get("empirical_mean", 0)
        
        # Calculate median manually if needed
        success_positions = result.get("success_positions", [])
        median_pulls = median(success_positions) if success_positions else 0
        
        
        return jsonify({
                "game": game["name"],
                "total_pulls": pulls,
                "probability": round((1 - (1 - rate) ** pulls) * 100, 2),
                "average_pulls": round(1 / rate, 2),
                "median_pulls": 0,
                "prob_cards": prob_cards
            })
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)