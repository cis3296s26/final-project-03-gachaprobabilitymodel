from flask import Flask, request, jsonify, render_template
import geometric

app = Flask(__name__)

GAMES = {
    "fgo": {
        "name": "Fate/Grand Order",
        "base_rate": 0.01,
        "cost_per_pull": 3
    },
    "uma": {
        "name": "Uma Musume",
        "base_rate": 0.03,
        "cost_per_pull": 150
    }
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

@app.route("/currency", methods=["POST"])
def currency():
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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
