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
    
    self._hoyo_last_featured = None
    self._hoyo_lost_50_50 = False

    self._simulation_map = {
            "fgo": {
                "rate_func": FGOrate,
                "featured_func": check_fgo_featured,
                "calc_func": FGORateCalc,
                "needs_state": False
            },
            "uma": {
                "rate_func": UMArate,
                "featured_func": check_uma_featured,
                "calc_func": UMARateCalc,
                "needs_state": False
            },
            "genshin": {
                "rate_func": HoyoverseRate,
                "featured_func": self._hoyoverse_featured_wrapper,
                "pity_func": HoyoversePitySystem,
                "needs_state": True
            },
            "hsr": {
                "rate_func": HoyoverseRate,
                "featured_func": self._hoyoverse_featured_wrapper,
                "pity_func": HoyoversePitySystem,
                "needs_state": True
            },
            "zzz": {
                "rate_func": HoyoverseRate,
                "featured_func": self._hoyoverse_featured_wrapper,
                "pity_func": HoyoversePitySystem,
                "needs_state": True
            }
        }
    # Wrapper to handle Hoyoverse 50/50 tracking and pity system for featured SSRs
    def _hoyoverse_featured_wrapper(self, roll):
        featured_chance = HoyoversePitySystem(
            roll, 
            ssr_count,
            self._hoyo_last_featured
        )
        
        is_featured = random.random() < featured_chance
        
        if is_featured:
            self._hoyo_last_featured = roll
            if featured_chance == 1.0:
                character = "Featured SSR (Pity Guarantee)"
            else:
                character = "Featured SSR (50/50 Win)"
        else:
            character = "Off-rate SSR (50/50 Loss)"
        
        return is_featured, character
    

    def simulateCurrency(self, game_id: str, currency: int, tickets: int = 0) -> Optional[Dict]:
        game = GAMES.get(game_id)
        if not game:
            print("Game not found in {game_id} GAMES dictionary.")
            return None

        pulls = currency // game["cost_per_pull"] + tickets
        
        print(f"Game: {game['name']}")
        print(f"Total pulls: {pulls} ({currency} currency + {tickets} tickets)")
        print(f"Base rate: {game['base_rate']*100:.1f}%")

        game_config = self._simulation_map.get(game_id)
        
        if game_config:
            # Use game-specific simulation
            result = self.simulateConfig(game_config, currency, game)
        else:
            # Use default simulation
            result = self.simulateDefault(currency, game)
        
        return result
    # Simulation that uses specific rates and has external rulings
    def simulateConfig(self, currency: int, game: Dict) -> Optional[Dict]:
        if game_config.get("needs_state", False):
            self._hoyo_last_featured = None
            self._hoyo_lost_50_50 = False
        
        def custom_rate_calculator(roll: int) -> float:
            """Use the game's own rate calculation function"""
            return game_config["rate_func"](roll)
        
        result = gachaModel(
            currency=currency,
            cost=game["cost_per_pull"],
            rate=game["base_rate"],
            seed=self.seed if self.seed else random.randint(1, 999999),
            featuredRate=None,  
            checkExternal=game_config["featured_func"],  
            custom_rate_calculator=custom_rate_calculator
        )
        
        return result
    # Default simulation using base rate without special extra checks
    def simulateDefault(self, currency: int, game: Dict) -> Optional[Dict]:
        return gachaModel(
            currency=currency,
            cost=game["cost_per_pull"],
            rate=game["base_rate"],
            seed=self.seed if self.seed else random.randint(1, 999999),
            featuredRate=None,
            checkExternal=None
        )

