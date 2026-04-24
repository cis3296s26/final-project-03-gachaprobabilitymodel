import math
import random
from typing import Optional, List, Dict, Any, Tuple

from geometric import gachaModel
from FGO import FGOrate, check_fgo_featured, FGORateCalc
from Umamusume import UMArate, check_uma_featured, UMARateCalc
from HoyoverseGames import HoyoverseRate, HoyoversePitySystem, hoyoverseRateCalc


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
    def _hoyoverse_featured_wrapper(self, roll: int) -> Tuple[bool, str]:
        featured_chance = HoyoversePitySystem(
            roll, 
            previousSSRcount=0,
            lastFeaturedRoll = self._hoyo_last_featured
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
    

    # Simulation that uses specific rates and has external rulings
    def simulateConfig(self, game_config: Dict, currency: int, game: Dict) -> Optional[Dict]:
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
    def simulate_histogram(self, currency: int, cost: int, rate_fn,
                       featured_fn=None, game_type: str = None) -> Dict:
        random.seed(self.seed)
        total_rolls = math.floor(currency / cost)

        pulls = []
        featured_positions = []

        if game_type in ("genshin", "hsr", "zzz"):
            self._hoyo_last_featured = None
            self._hoyo_lost_50_50 = False

        for roll in range(1, total_rolls + 1):
            chance = rate_fn(roll)
            if random.random() < chance:
                pulls.append(roll)

                if featured_fn:
                    if game_type in ("genshin", "hsr", "zzz"):
                        is_featured, _ = self._hoyoverse_featured_wrapper(roll)
                    else:
                        is_featured, _ = featured_fn(roll)

                    if is_featured:
                        featured_positions.append(roll)

        gaps = []
        prev = 0
        for p in pulls:
            gaps.append(p - prev)
            prev = p
        gap.sort()

        bin_size = max(1, math.floor(total_rolls / 40))
        bins = {i: 0 for i in range(1, total_rolls + 1, bin_size)}
        for i in gaps:
            bin_key = ((i - 1) // bin_size) * bin_size + 1
            bins[bin_key] = bins.get(bin_key, 0) + 1

        return {
            "bins": bins,
            "bin_size": bin_size,
            "pulls": pulls,
            "gaps": gaps,
            "featured_positions": featured_positions,
            "total_rolls": total_rolls,
        }
