import math
import random
from collections import Counter
from typing import Optional, List, Dict, Any, Tuple

from geometric import gachaModel, rateCalculator, GachaHistogram as GeometricHistogram
from FGO import FGOrate, check_fgo_featured, FGORateCalc
from Umamusume import UMArate, check_uma_featured, UMARateCalc
from HoyoverseGames import HoyoverseRate, HoyoversePitySystem, hoyoverseRateCalc
from app import GAMES, currency as appCurrency


try:
    from app import app
    import requests
except ImportError:
    requests = None

class GachaSimulation:
    def __init__(self, seed: int = None):
        self.seed = seed
        random.seed(self.seed)

    self._simulation_map = {
            "fgo": {
                "rate_func": FGOrate,
                "featured_func": check_fgo_featured,
                "calc_func": FGORateCalc
            },
            "uma": {
                "rate_func": UMArate,
                "featured_func": check_uma_featured,
                "calc_func": UMARateCalc
            },
            "genshin": {
                "rate_func": HoyoverseRate,
                "featured_func": self._hoyoverse_featured_wrapper,
                "pity_func": HoyoversePitySystem
            }
        }

    def simulateCurrency(self, game_id: str, currency: int, tickets: int = 0) -> Optional[Dict]:
        game = GAMES.get(game_id)
        if not game:
            print("Game not found in {game_id} GAMES dictionary.")
            return None

        pulls = currency // game["cost_per_pull"] + tickets
        
        print(f"Game: {game['name']}")
        print(f"Total pulls: {pulls} ({currency} currency + {tickets} tickets)")
        print(f"Base rate: {game['base_rate']*100:.1f}%")

        simulationFunc = self.simulationMap.get(game_id, self.simulateDefault)
        result = simulationFunc(currency, game)
    def simulateDefault(self, currency: int, game: Dict) -> Optional[Dict]:
        return gachaModel(
            currency=currency,
            cost=game["cost_per_pull"],
            rate=game["base_rate"],
            seed=self.seed if self.seed else random.randint(1, 999999),
            featuredRate=None
        )

