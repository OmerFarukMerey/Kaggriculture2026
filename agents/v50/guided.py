"""New market policy around an incumbent's reactive farming and stock intent.

The guide decides farming actions and desired working inventory. Its market
queue is not executed: commodity round trips are netted, ready outputs are
repriced, and cash/capacity-safe slot orders are selected against uncertain flow.
"""
from .market import MarketController
from .mechanics import PRODUCTS, execute_market, project_units


class GuidedMarketController(MarketController):
    def act(self, observation, configuration, action):
        step = int(observation['step'])
        if step <= self._last_step:
            self._reset()
        self._observe_transition(observation, step)
        configuration = configuration or {}
        farm, private = project_units(observation, action, configuration)
        market = observation['market']
        inventory, params, prices = market['inventory'], market.get('params'), market['prices']
        native = [list(order) for order in action.get('market', []) if isinstance(order, (list, tuple))]
        reference = execute_market(native, [], farm, private, inventory, params, configuration)
        shed = private['shed']
        targets = {item: int(reference['shed'].get(item, 0)) for item in ('WHEAT', 'FERTILIZER')}
        terminal = step == 718
        if terminal:
            targets = dict.fromkeys(targets, 0)
        fixed = [order for order in native if order and order[0] in
                 ('BUY_SEED', 'BUY_ANIMAL', 'HIRE', 'BUY_LAND')] if not terminal else []
        capacity = int(configuration.get('shedCapacity', 100))
        max_orders = int(configuration.get('maxMarketOrdersPerTurn', 10))
        hour = step % int(configuration.get('turnsPerDay', 24))
        carried = sum(max(0, int(q)) for bag in private['inventories'] for q in bag.values())
        buys = [['BUY_PRODUCT', item, target - int(shed.get(item, 0))]
                for item, target in targets.items() if target > int(shed.get(item, 0))]
        required_cash = self._fixed_cost(fixed + buys, farm, prices)
        needs_cash = required_cash > float(farm['money'])
        safe_storage = sum(shed.values()) + carried + sum(order[2] for order in buys) <= capacity - 4
        sales = {}
        delayed = []
        cache = {}
        for item in PRODUCTS:
            quantity = max(0, int(shed.get(item, 0)) - targets.get(item, 0))
            if not quantity:
                continue
            if self._should_delay_sale(observation, step, item, quantity, int(inventory[item]),
                                       params, needs_cash, safe_storage, cache):
                delayed.append(item)
            else:
                sales[item] = quantity
        # Native stock targets must not reserve space that the dawn cargo needs.
        if hour == 23:
            shortage = max(0, sum(shed.values()) + carried + sum(order[2] for order in buys)
                           - sum(sales.values()) - capacity)
            for item in sorted(targets, key=lambda p: prices.get(p, 0)):
                release = min(shortage, targets[item], int(shed.get(item, 0)) - sales.get(item, 0))
                if release > 0:
                    targets[item] -= release
                    sales[item] = sales.get(item, 0) + release
                    shortage -= release
        sells = [['SELL', item, quantity] for item, quantity in
                 sorted(sales.items(), key=lambda pair: (-prices.get(pair[0], 0), pair[0]))]
        orders = sells + fixed + buys
        if len(orders) > max_orders:
            # Keep physical purchases and working inputs; defer the cheapest
            # discretionary sales when more distinct products occupy the shed.
            room = max(0, max_orders - len(fixed) - len(buys))
            orders = sells[:room] + fixed + buys
        reserve = {item: min(target, int(shed.get(item, 0)) + sum(
            order[2] for order in buys if order[1] == item)) for item, target in targets.items()}
        queue, tracked, objective = self._optimize_queue(
            orders, max_orders, farm, private, inventory, params, configuration,
            reserve, carried, capacity, hour, terminal,
            any(not order for order in native) or any(self._confidence(model) >= 0.08
                                                     for model in self._flow.values()))
        self._last_step = step
        self._last_inventory = dict(inventory)
        self._last_snapshot = {'step': step, 'day': step // 24, 'hour': hour,
                               'town': {'unlocked_shops': list(observation['town']['unlocked_shops'])}}
        self._last_own_net = dict(tracked['net'])
        self.diagnostics['last'] = {'step': step, 'input_targets': targets, 'sales': sales,
                                    'delayed': delayed, 'queue': queue,
                                    'worst_score': objective[0], 'mean_score': objective[1]}
        result = dict(action)
        result['market'] = queue
        return result
