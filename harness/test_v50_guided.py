"""Working-inventory and funding contracts of the new guided market policy."""
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'agents'))
from v50.guided import GuidedMarketController


class GuidedMarketTests(unittest.TestCase):
    def _netting_episode(self, optimized):
        from kaggle_environments import make
        env = make('kaggriculture', configuration={'episodeSteps': 720, 'seed': 632149}, debug=False)
        env.reset(2)
        env.state[1].observation.private.shed['WHEAT'] = 50
        action = {'farmer': ['PASS'], 'hands': [],
                  'market': [['BUY_PRODUCT', 'WHEAT', 50], ['SELL', 'WHEAT', 40]]}
        if optimized:
            action = GuidedMarketController().act(env.state[0].observation, env.configuration, action)
        rival = {'farmer': ['PASS'], 'hands': [], 'market': [['SELL', 'WHEAT', 50]]}
        env.step([action, rival])
        return env.state[0].observation

    def test_netting_preserves_working_stock_without_round_trip_loss(self):
        native = self._netting_episode(False)
        optimized = self._netting_episode(True)
        self.assertEqual(native.private.shed['WHEAT'], 10)
        self.assertEqual(optimized.private.shed['WHEAT'], 10)
        self.assertGreater(optimized.farms[0].money, native.farms[0].money)

    def test_competing_sale_funds_seed_for_next_real_planting(self):
        from kaggle_environments import make
        env = make('kaggriculture', configuration={'episodeSteps': 720, 'seed': 632149}, debug=False)
        env.reset(2)
        env.state[0].observation.farms[0].money = 0
        for state in env.state:
            state.observation.market.inventory['MILK'] = 10071
        env.state[0].observation.private.shed['MILK'] = 1
        env.state[1].observation.private.shed['MILK'] = 5
        native = {'farmer': ['PASS'], 'hands': [],
                  'market': [['BUY_SEED', 'WHEAT', 1], ['SELL', 'MILK', 1]]}
        action = GuidedMarketController().act(env.state[0].observation, env.configuration, native)
        env.step([action, {'farmer': ['PASS'], 'hands': [], 'market': [['SELL', 'MILK', 5]]}])
        self.assertEqual(env.state[0].observation.farms[0].money, 1)
        env.step([{'farmer': ['PLANT', 'WHEAT'], 'hands': [], 'market': []},
                  {'farmer': ['PASS'], 'hands': [], 'market': []}])
        self.assertEqual(env.state[0].observation.farms[0].tiles[4][4]['crop'], 'WHEAT')


if __name__ == '__main__':
    unittest.main()
