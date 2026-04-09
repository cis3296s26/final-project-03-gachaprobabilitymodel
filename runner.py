import geometric
import app
import HoyoverseGames

if __name__ == "__main__":
    print("Running geometric.py...\n")
    geometric.gachaModel(currency=300, cost=3, rate=0.01, seed=42)
    
    print("Running app.py...\n")
    app.app.run(host="0.0.0.0", port=5000)
    
    print("Running hoyoverse.py...")
    HoyoverseGames.app.run(host="0.0.0.0", port=5001)