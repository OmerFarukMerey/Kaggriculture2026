"""Observed-state mechanics shared by the original production and market policies.

The copied deterministic rules live in _engine.py. Opponent market scenarios are
explicitly conditional: listed rival commodity orders have funding and stock,
not access to the opponent's private state. Own actions use exact engine limits.
"""
from copy import deepcopy
from . import _engine as rules

PRODUCTS = tuple(rules.PRODUCTS)
CROP_INFO = rules.CROPS
ANIMAL_INFO = rules.ANIMALS
SEED_PRICE = {item: p['seed'] for item, p in CROP_INFO.items()}
ANIMAL_COST = {item: p['cost'] for item, p in ANIMAL_INFO.items()}
MARKET_PARAMS = rules.MARKET_PARAMS
_PRICE_PARAMS = object()
_PRICE_COLUMNS = {}
_PRICE_CACHE = {}


def price(item, inventory, market_params=None):
    """Exact integer engine quote; compile curve constants once per observation."""
    global _PRICE_PARAMS, _PRICE_COLUMNS, _PRICE_CACHE
    params = market_params if market_params is not None else MARKET_PARAMS
    if params is not _PRICE_PARAMS:
        _PRICE_PARAMS = params
        _PRICE_COLUMNS = {}
        _PRICE_CACHE = {}
        for name, p in params.items():
            base, target = p['base'], p['T']
            below, above = p['below_func'], p['above_func']
            _PRICE_COLUMNS[name] = (
                base, p['I0'], target, below,
                p['below_target'] * base / rules._shape(below, target, target),
                above, p['above_target'] * base / rules._shape(above, target, target))
    key = (item, inventory)
    cached = _PRICE_CACHE.get(key)
    if cached is not None:
        return cached
    base, initial, target, below, low_amp, above, high_amp = _PRICE_COLUMNS[item]
    value = (base + low_amp * rules._shape(below, initial - inventory, target)
             if inventory < initial else
             base - high_amp * rules._shape(above, inventory - initial, target))
    result = max(1, int(round(value)))
    _PRICE_CACHE[key] = result
    return result


def town_consumption(observation, step=None, expected=False):
    """Per-turn demand from revealed shops; optional mean of unrevealed draws.

    Standard competition calendar only: shops every3 days (at most8), purchases
    every4 turns, town center every24 turns. Draws are uniform with replacement.
    """
    step = int(observation['step']) if step is None else int(step)
    known = observation.get('town', {}).get('unlocked_shops', [])
    opened = min(8, max(0, step // 72))
    shops = known[:opened]
    demand = {item: 0.0 for item in PRODUCTS}
    if step % 4 == 0:
        for shop in shops:
            items = rules.SHOPS[shop]
            for item in items:
                demand[item] += 2 if len(items) == 1 else 1
        missing = max(0, opened - len(shops)) if expected else 0
        if missing:
            weight = missing / len(rules.SHOPS)
            for items in rules.SHOPS.values():
                for item in items:
                    demand[item] += weight * (2 if len(items) == 1 else 1)
    if step % 24 == 0:
        for item in PRODUCTS:
            if item != 'FERTILIZER':
                demand[item] += 1
    return demand


def project_units(observation, action, configuration=None, *, flows=None):
    """Apply farmer then hands, including atomic crop-level PLANT suppression.

    Optional flows is used only by the offline real-engine profile generator.
    It measures actual harvest/collection and productive feed/fertilizer use,
    not purchases, artificial round trips, or destruction of cargo on DROP.
    """
    cfg = configuration or {}
    farm = deepcopy(observation['farms'][int(observation['player'])])
    private = deepcopy(observation['private'])
    turns = int(rules.get(cfg, 'turnsPerDay', 24))
    board = int(rules.get(cfg, 'boardSize', 10))
    capacity = int(rules.get(cfg, 'shedCapacity', 100))
    day = int(observation['step']) // turns
    actions = [action.get('farmer', ['PASS']), *(action.get('hands') or [])]
    needed = {}
    for command in actions:
        if isinstance(command, list) and len(command) >= 2 and command[0] == 'PLANT':
            needed[command[1]] = needed.get(command[1], 0) + 1
    blocked = {crop for crop, count in needed.items() if count > private['seeds'].get(crop, 0)}
    for actor, command in enumerate(actions):
        if isinstance(command, list) and len(command) >= 2 and command[0] == 'PLANT' and command[1] in blocked:
            continue
        before = None
        if flows is not None and actor < len(private['inventories']):
            before = dict(private['inventories'][actor])
        rules._apply_unit_action(farm, private, actor, command, board, day, turns, capacity)
        if before is not None and command:
            after = private['inventories'][actor]
            if command[0] in ('HARVEST', 'COLLECT_FERTILIZER'):
                for item, quantity in after.items():
                    gain = quantity - before.get(item, 0)
                    if gain > 0:
                        out = flows['yield']
                        out[item] = out.get(item, 0) + gain
            elif command[0] in ('FEED', 'FERTILIZE'):
                item = 'WHEAT' if command[0] == 'FEED' else 'FERTILIZER'
                used = before.get(item, 0) - after.get(item, 0)
                if used > 0:
                    out = flows['inputs']
                    out[item] = out.get(item, 0) + used
    return farm, private


def execute_market(orders, rival_orders, farm, private, inventory, market_params=None,
                   configuration=None):
    """Execute all slots with simultaneous pre-commit quotes, then own limits.

    Rival commodity orders are conditional scenarios with sufficient cash and
    stock. Rival fixed purchases consume their index but have no shared effect.
    Net reports our ACTUAL shared inventory impact: floor-price sales add zero.
    Arguments are not mutated; no town consumption or end-of-day deposit occurs.
    """
    cfg = configuration or {}
    limit = max(1, int(rules.get(cfg, 'maxMarketOrdersPerTurn', 10)))
    capacity = int(rules.get(cfg, 'shedCapacity', 100))
    board = int(rules.get(cfg, 'boardSize', 10))
    hire_mult = int(rules.get(cfg, 'farmHandCostMult', 1))
    own = dict(farm)
    own['hands'] = list(farm['hands'])
    own['unlocked_quadrants'] = list(farm['unlocked_quadrants'])
    if any(o and o[0] == 'BUY_LAND' for o in orders[:limit]):
        own['tiles'] = [list(row) for row in farm['tiles']]
    stock = {'shed': dict(private['shed']), 'seeds': dict(private['seeds']),
             'inventories': list(private['inventories'])}
    market = {'inventory': dict(inventory), 'params': market_params}
    net = {item: 0 for item in PRODUCTS}
    executed = []
    fixed_spend = 0.0
    queues = (orders[:limit], rival_orders[:limit])
    for slot in range(max(len(queues[0]), len(queues[1]))):
        current = [rules._parse_order(q[slot]) if slot < len(q) else None for q in queues]
        for side, order in enumerate(current):
            if order is None:
                continue
            op = order['type']
            if op in ('HIRE', 'BUY_LAND'):
                if side == 0:
                    before = own['money']
                    if op == 'HIRE':
                        rules._do_hire(own, stock, board, hire_mult)
                    else:
                        rules._do_buy_land(own, board)
                    fixed_spend += before - own['money']
                    if before != own['money']:
                        executed.append([slot, op, None, 1])
                current[side] = None
            elif side == 1 and (op not in ('SELL', 'BUY_PRODUCT') or order['item'] not in PRODUCTS):
                current[side] = None
        while current[0] is not None or current[1] is not None:
            quoted = [None, None]
            for side, order in enumerate(current):
                if order is None:
                    continue
                if order['remaining'] <= 0:
                    current[side] = None
                    continue
                op, item = order['type'], order['item']
                if op == 'SELL' and item in PRODUCTS:
                    quote = price(item, market['inventory'][item], market_params)
                elif op == 'BUY_PRODUCT' and item in ('WHEAT', 'FERTILIZER'):
                    quote = price(item, market['inventory'][item] - 1, market_params)
                elif op == 'BUY_SEED' and item in SEED_PRICE:
                    quote = SEED_PRICE[item]
                elif op == 'BUY_ANIMAL' and item in ANIMAL_COST:
                    quote = ANIMAL_COST[item]
                else:
                    current[side] = None
                    continue
                quoted[side] = (op, item, quote)
            committed = False
            for side, quote in enumerate(quoted):
                if quote is None:
                    continue
                op, item, value = quote
                before = market['inventory'].get(item, 0)
                if side == 0:
                    ok = rules._commit_unit(op, item, value, own, stock, market, capacity)
                    if ok:
                        if item in net:
                            net[item] += market['inventory'][item] - before
                        if op in ('BUY_SEED', 'BUY_ANIMAL'):
                            fixed_spend += value
                        if executed and executed[-1][0] == slot:
                            executed[-1][3] += 1
                        else:
                            executed.append([slot, op, item, 1])
                else:
                    ok = True
                    if op == 'SELL' and value > 1:
                        market['inventory'][item] += 1
                    elif op == 'BUY_PRODUCT':
                        market['inventory'][item] -= 1
                if ok:
                    current[side]['remaining'] -= 1
                    committed = True
                else:
                    current[side] = None
            if not committed:
                break
    return {'money': own['money'], 'shed': stock['shed'], 'seeds': stock['seeds'],
            'inventory': market['inventory'], 'net': net, 'fixed_spend': fixed_spend,
            'farm': own, 'private': stock, 'executed': executed}
