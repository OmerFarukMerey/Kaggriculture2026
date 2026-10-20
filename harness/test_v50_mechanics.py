"""Observable engine boundaries relied on by the original v50 controller."""
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'agents'))
from v50.mechanics import execute_market, project_units, rules
from v50.market import MarketController


class MechanicsBoundaryTests(unittest.TestCase):
    def setUp(self):
        self.farm = rules._new_farm(10, 3000)
        self.private = rules._new_private()
        self.inventory = {item: 10000 for item in rules.PRODUCTS}

    def test_shared_quote_is_fixed_before_either_sale_commits(self):
        self.private['shed']['MILK'] = 2
        result = execute_market([['SELL', 'MILK', 2]], [['SELL', 'MILK', 2]],
                                self.farm, self.private, self.inventory)
        # Both first units quote160; both next units quote156 after two sales.
        self.assertEqual(result['money'], 3316)
        self.assertEqual(result['inventory']['MILK'], 10004)

    def test_floor_sale_pays_without_increasing_shared_supply(self):
        self.private['shed']['MILK'] = 4
        self.inventory['MILK'] = 11000
        result = execute_market([['SELL', 'MILK', 4]], [], self.farm,
                                self.private, self.inventory)
        self.assertEqual(result['money'], 3004)
        self.assertEqual(result['inventory']['MILK'], 11000)
        self.assertEqual(result['net']['MILK'], 0)

    def test_insufficient_seeds_cancel_every_plant_of_that_crop(self):
        self.farm['hands'] = [[3, 4]]
        self.private['inventories'].append({})
        self.private['seeds']['WHEAT'] = 1
        obs = {'step': 0, 'player': 0, 'farms': [self.farm, rules._new_farm(10, 3000)],
               'private': self.private}
        action = {'farmer': ['PLANT', 'WHEAT'], 'hands': [['PLANT', 'WHEAT']], 'market': []}
        farm, private = project_units(obs, action)
        self.assertIsNone(farm['tiles'][4][4])
        self.assertIsNone(farm['tiles'][4][3])
        self.assertEqual(private['seeds']['WHEAT'], 1)

    def test_implicit_single_pickup_is_funded_before_unit_execution(self):
        from kaggle_environments import make
        env = make('kaggriculture', configuration={'episodeSteps': 720, 'seed': 7139}, debug=False)
        env.reset(2)
        route = [{'farmer': ['PASS'], 'hands': [], 'market': []} for _ in range(719)]
        route[1] = {'farmer': ['PICKUP', 'WHEAT'], 'hands': [], 'market': []}
        controller = MarketController()
        action = controller.act(env.state[0].observation, env.configuration, route[0], route)
        env.step([action, route[0]])
        env.step([route[1], route[0]])
        self.assertEqual(env.state[0].observation.private.inventories[0].get('WHEAT'), 1)

    def _competing_sale(self, step):
        from kaggle_environments import make
        env = make('kaggriculture', configuration={'episodeSteps': 720, 'seed': 7142}, debug=False)
        env.reset(2)
        idle = {'farmer': ['PASS'], 'hands': [], 'market': []}
        if step:
            env.step([idle, idle])
        for state in env.state:
            state.observation.private.shed['MILK'] = 10
        route = [{'farmer': ['PASS'], 'hands': [], 'market': []} for _ in range(719)]
        route[step]['market'] = [['BUY_SEED', 'WHEAT', 1]]
        route[step + 1]['farmer'] = ['WEST']
        route[step + 2]['farmer'] = ['PLANT', 'WHEAT']
        action = MarketController().act(env.state[0].observation, env.configuration, route[step], route)
        rival = dict(idle, market=[['SELL', 'MILK', 10]])
        env.step([action, rival])
        return env.state[0].observation

    def test_small_town_drain_does_not_assume_rival_has_no_supply(self):
        observation = self._competing_sale(0)
        self.assertEqual(observation.private.shed['MILK'], 0)
        self.assertEqual(observation.farms[0].money, 4401)
        self.assertEqual(observation.private.seeds['WHEAT'], 1)

    def test_sale_queue_preserves_simultaneous_quote_before_fixed_purchase(self):
        observation = self._competing_sale(1)
        # Purchasing the seed first realizes only 4307 after the rival sells.
        self.assertEqual(observation.farms[0].money, 4430)
        self.assertEqual(observation.private.seeds['WHEAT'], 1)


if __name__ == '__main__':
    unittest.main()
