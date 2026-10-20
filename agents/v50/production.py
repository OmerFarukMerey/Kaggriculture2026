"""Compatible route selection and small physical repairs for v50.

The route tapes are treated as measured physical plans.  They are never edited:
``act`` returns a fresh action plus the selected original tape for downstream
market planning.
"""

from __future__ import annotations
from copy import deepcopy

from .mechanics import (
    ANIMAL_INFO,
    CROP_INFO,
    PRODUCTS,
    rules,
    price,
    town_consumption,
)


# Portable stock does not constrain farm-layout compatibility. The market
# controller funds future seed/animal placements from actual private inventory.
_MANDATORY_ORDERS = frozenset(("HIRE", "BUY_LAND"))
_MOVES = frozenset(("NORTH", "SOUTH", "EAST", "WEST"))


def _get(value, key, default=None):
    if isinstance(value, dict):
        return value.get(key, default)
    return getattr(value, key, default)


def _step(observation):
    explicit = _get(observation, "step", None)
    if explicit is not None:
        return int(explicit)
    return int(_get(observation, "day", 0) or 0) * 24 + int(
        _get(observation, "hour", 0) or 0
    )


def _command(value):
    if not isinstance(value, (list, tuple)) or not value:
        return ["PASS"]
    return list(value)


def _copy_action(action):
    action = action or {}
    return {
        "farmer": _command(action.get("farmer", ["PASS"])),
        "hands": [_command(command) for command in (action.get("hands", []) or [])],
        "market": [list(order) for order in (action.get("market", []) or [])],
    }


def _canonical(action):
    """The irreversible physical prefix used to partition route continuations."""
    action = action or {}
    farmer = tuple(_command(action.get("farmer", ["PASS"])))
    hands = tuple(tuple(_command(command)) for command in (action.get("hands", []) or []))
    orders = []
    for order in action.get("market", []) or []:
        if isinstance(order, (list, tuple)) and order and order[0] in _MANDATORY_ORDERS:
            orders.append(tuple(order))
    return farmer, hands, tuple(orders)


def _tile(farm, position):
    if not isinstance(position, (list, tuple)) or len(position) < 2:
        return "LOCKED"
    x, y = int(position[0]), int(position[1])
    tiles = farm.get("tiles", []) or []
    if y < 0 or y >= len(tiles) or x < 0 or x >= len(tiles[y]):
        return "LOCKED"
    return tiles[y][x]


def _shed_adjacent(position, board_size):
    if not isinstance(position, (list, tuple)) or len(position) < 2:
        return False
    half = board_size // 2
    return (int(position[0]), int(position[1])) in (
        (half - 1, half - 1),
        (half, half - 1),
        (half - 1, half),
        (half, half),
    )


def _info_number(info, key, default):
    value = info.get(key, default)
    return float(value if value is not None else default)


def _can_apply(command, tile, inventory, private, position, board, day):
    """Whether a native command has useful work before scheduling a repair."""
    op = command[0]
    planted = isinstance(tile, dict) and tile.get("kind") == "PLANT"
    animal = isinstance(tile, dict) and tile.get("animal") in ANIMAL_INFO
    if op in _MOVES:
        dx, dy = rules.FARMER_MOVES[op]
        return 0 <= position[0] + dx < board and 0 <= position[1] + dy < board
    if op == "WATER":
        return planted and not tile["watered_today"]
    if op == "FEED":
        return animal and not tile["fed_today"] and inventory.get("WHEAT", 0) > 0
    if op == "CARE":
        return animal and not tile["cared_today"]
    if op == "COLLECT_FERTILIZER":
        return animal and tile.get("fertilizer_available", False)
    if op == "HARVEST":
        return ((animal or (planted and day - tile["planted_day"] >=
                            CROP_INFO[tile["crop"]]["first_yield_day"]))
                and tile.get("yield_units", 0) > 0)
    if op == "PLANT":
        return tile is None and len(command) > 1 and private["seeds"].get(command[1], 0) > 0
    if op in ("BUILD_COOP", "BUILD_PASTURE"):
        return tile is None
    if op == "DIG":
        return isinstance(tile, dict) and not animal
    if op == "FERTILIZE":
        return planted and inventory.get("FERTILIZER", 0) > 0
    if op == "DROP":
        return bool(inventory) and _shed_adjacent(position, board)
    if op == "PICKUP":
        return (len(command) > 1 and _shed_adjacent(position, board)
                and private["shed"].get(command[1], 0) > 0)
    if op == "PLACE" and len(command) > 1 and inventory.get(command[1], 0) > 0:
        if command[1] in ANIMAL_INFO:
            return (isinstance(tile, dict) and not animal
                    and tile.get("kind") == ANIMAL_INFO[command[1]]["structure"])
        return _shed_adjacent(position, board)
    return False


class ProductionController:
    """Select an economically useful, prefix-compatible physical route.

    A controller is intentionally per player. Compatibility is committed one
    action at a time, including unit commands, hiring, and land expansion.
    Portable stock purchases and ordinary trades do not split otherwise
    compatible production plans.
    """

    def __init__(self, routes, profiles):
        if not routes:
            raise ValueError("ProductionController requires at least one route")
        self.routes = routes
        self.profiles = profiles
        self.route_ids = tuple(sorted(int(route_id) for route_id in routes))
        for route_id in self.route_ids:
            if route_id not in profiles:
                raise KeyError("missing production profile for route %r" % route_id)
            if len(routes[route_id]) < 719:
                raise ValueError("route %r has fewer than 719 actions" % route_id)
        self.diagnostics = {}
        self._reset()

    def _reset(self):
        reset_count = int(self.diagnostics.get("resets", 0)) + 1
        self._compatible = list(self.route_ids)
        self._selected = None
        self._last_step = -1
        self._last_day = -1
        self._last_shops = None
        self._pending = {}
        self._couriers = {}
        self._last_result = None
        self.diagnostics.clear()
        self.diagnostics.update(
            {
                "selected_route": None,
                "compatible_routes": tuple(self.route_ids),
                "choices": [],
                "repairs": [],
                "resets": reset_count,
            }
        )

    def act(self, observation, configuration=None):
        step = _step(observation)
        if step < 0 or step >= 719:
            raise ValueError("production route requested outside actionable steps: %r" % step)
        if step < self._last_step:
            self._reset()
        elif step == self._last_step and self._last_result is not None:
            action, route_id = self._last_result
            return _copy_action(action), self.routes[route_id]

        day = int(_get(observation, "day", step // 24) or 0)
        if day != self._last_day:
            # Hired hands and all unit positions reset at dawn.  A delayed
            # command is positional, so carrying it across dawn is unsafe.
            self._pending.clear()
            self._couriers.clear()
            self._last_day = day

        town = _get(observation, "town", {}) or {}
        shops = tuple(_get(town, "unlocked_shops", []) or [])
        signatures = {route_id: _canonical(self.routes[route_id][step])
                      for route_id in self._compatible}
        reasons = []
        if self._selected is None:
            reasons.append("initial")
        if self._last_shops is not None and shops != self._last_shops:
            reasons.append("revealed_demand")
        if len(set(signatures.values())) > 1:
            reasons.append("physical_divergence")

        if reasons:
            scores = self._score_routes(observation, configuration, self._compatible)
            self._selected = max(self._compatible, key=lambda route_id: (scores[route_id], -route_id))
            ranked = sorted(scores.items(), key=lambda item: (-item[1], item[0]))[:5]
            self.diagnostics["choices"].append(
                {
                    "step": step,
                    "reason": tuple(reasons),
                    "route": self._selected,
                    "candidates": len(self._compatible),
                    "top_scores": tuple((route_id, round(score, 2)) for route_id, score in ranked),
                }
            )
        elif self._selected not in self._compatible:
            # This is an invariant failure, not an invitation to jump layouts.
            raise RuntimeError("selected route left its compatible prefix group")

        self._last_shops = shops
        selected_action = self.routes[self._selected][step]
        commitment = signatures[self._selected]
        self._compatible = [
            route_id
            for route_id in self._compatible
            if signatures[route_id] == commitment
        ]
        if not self._compatible:
            raise RuntimeError("route commitment produced an empty compatibility group")

        action = _copy_action(selected_action)
        action = self._repair_units(observation, configuration, action, step)
        self.diagnostics["selected_route"] = self._selected
        self.diagnostics["compatible_routes"] = tuple(self._compatible)
        self.diagnostics["pending_repairs"] = sum(len(queue) for queue in self._pending.values())
        self._last_step = step
        self._last_result = (_copy_action(action), self._selected)
        return action, self.routes[self._selected]

    # ------------------------------------------------------------------
    # Economic route choice

    def _score_routes(self, observation, configuration, route_ids):
        step = _step(observation)
        day = step // 24
        remaining_fraction = (24 - step % 24) / 24.0
        town_by_day = self._town_forecast(observation, step)
        rival_expected, rival_upper = self._rival_forecast(observation, day)
        market = _get(observation, "market", {}) or {}
        initial_inventory = {
            product: float((_get(market, "inventory", {}) or {}).get(product, 10000))
            for product in PRODUCTS
        }
        params = _get(market, "params", None)
        floor_inventory = {}
        for product in PRODUCTS:
            own_bound = max(
                sum(float(bucket.get(product, 0)) for bucket in self.profiles[rid]["yield"][day:])
                for rid in route_ids
            )
            rival_bound = sum(bucket.get(product, 0) for bucket in rival_upper[day:])
            low, high = 0, int(initial_inventory[product] + own_bound + rival_bound) + 1
            if price(product, high, params) <= 1:
                while low < high:
                    middle = (low + high) // 2
                    if price(product, middle, params) <= 1:
                        high = middle
                    else:
                        low = middle + 1
            floor_inventory[product] = high

        scores = {}
        for route_id in route_ids:
            profile = self.profiles[route_id]
            expected = self._scenario_margin(
                profile,
                day,
                remaining_fraction,
                initial_inventory,
                town_by_day,
                rival_expected,
                params,
                floor_inventory,
            )
            conservative = self._scenario_margin(
                profile,
                day,
                remaining_fraction,
                initial_inventory,
                town_by_day,
                rival_upper,
                params,
                floor_inventory,
            )
            # The expected visible-footprint estimate dominates, while the
            # upper rival-production case protects premium routes from a
            # milk/wool/melon glut that a point forecast would miss.
            scores[route_id] = 0.68 * expected + 0.32 * conservative
        return scores

    def _town_forecast(self, observation, start_step):
        by_day = [{product: 0.0 for product in PRODUCTS} for _ in range(30)]
        for future_step in range(start_step, 719):
            consumption = town_consumption(observation, step=future_step, expected=True)
            bucket = by_day[future_step // 24]
            for product, quantity in consumption.items():
                if product in bucket:
                    bucket[product] += float(quantity)
        return by_day

    def _rival_forecast(self, observation, current_day):
        expected = [{product: 0.0 for product in PRODUCTS} for _ in range(30)]
        upper = [{product: 0.0 for product in PRODUCTS} for _ in range(30)]
        player = int(_get(observation, "player", 0) or 0)
        farms = list(_get(observation, "farms", []) or [])
        rival = farms[1 - player] if len(farms) > 1 else {}

        for row in rival.get("tiles", []) or []:
            for tile in row or []:
                if not isinstance(tile, dict):
                    continue
                if tile.get("kind") == "PLANT" and tile.get("crop") in CROP_INFO:
                    crop = tile["crop"]
                    info = CROP_INFO[crop]
                    planted = int(tile.get("planted_day", current_day))
                    held = max(0.0, float(tile.get("yield_units", 0) or 0))
                    ongoing = bool(info.get("ongoing", False))
                    if ongoing:
                        if held:
                            expected[current_day][crop] += held
                            upper[current_day][crop] += held
                        first = int(_info_number(info, "first_yield_day", 1))
                        interval = max(1, int(_info_number(info, "interval", 1)))
                        cap = max(1, int(_info_number(info, "max_yield", 4)))
                        for number in range(cap):
                            production_day = planted + first + number * interval
                            if current_day < production_day < 30:
                                expected[production_day][crop] += 1.15
                                upper[production_day][crop] += 2.0
                    else:
                        first = int(_info_number(info, "first_yield_day", 1))
                        maximum_day = int(_info_number(info, "max_yield_day", first))
                        maximum = _info_number(info, "max_yield", max(held, 1.0))
                        harvest_day = min(29, max(current_day, planted + maximum_day))
                        # Visible one-time crops are assumed to survive to a
                        # useful harvest, but the upper case allows perfect care.
                        expected[harvest_day][crop] += max(held, 0.72 * maximum)
                        upper[harvest_day][crop] += max(held, maximum)
                    continue

                animal = tile.get("animal")
                if animal not in ANIMAL_INFO:
                    continue
                info = ANIMAL_INFO[animal]
                product = info["product"]
                held = max(0.0, float(tile.get("yield_units", 0) or 0))
                if held:
                    expected[current_day][product] += held
                    upper[current_day][product] += held
                placed = int(tile.get("placed_day", current_day))
                first = int(_info_number(info, "first_yield_day", 1))
                interval = max(1, int(_info_number(info, "interval", 1)))
                first_future = placed + first
                if first_future <= current_day:
                    elapsed = current_day - first_future
                    first_future += (elapsed // interval + 1) * interval
                for production_day in range(first_future, 30, interval):
                    # Care banks once per fed day, not once per production tick.
                    expected[production_day][product] += min(info["max_held"], 1 + 0.8 * interval)
                    upper[production_day][product] += min(info["max_held"], 1 + interval)
                for future_day in range(max(current_day, placed + 1), 30):
                    expected[future_day]["FERTILIZER"] += 0.75
                    upper[future_day]["FERTILIZER"] += 1.0
        return expected, upper

    def _scenario_margin(
        self,
        profile,
        start_day,
        first_fraction,
        initial_inventory,
        town_by_day,
        rival_supply,
        market_params,
        floor_inventory,
    ):
        inventory = dict(initial_inventory)
        margin = 0.0
        yields = profile["yield"]
        inputs = profile["inputs"]
        fixed = profile["fixed"]

        for day in range(start_day, min(30, len(yields))):
            fraction = first_fraction if day == start_day else 1.0
            for product in PRODUCTS:
                inventory[product] = max(
                    1.0, inventory[product] - town_by_day[day].get(product, 0.0)
                )

            day_inputs = inputs[day] if day < len(inputs) else {}
            day_yields = yields[day] or {}
            for product in PRODUCTS:
                consumed = max(0.0, float(day_inputs.get(product, 0.0) or 0.0)) * fraction
                if consumed:
                    midpoint = max(1.0, inventory[product] - 0.5 * consumed)
                    margin -= consumed * price(product, int(round(midpoint)), market_params)
                    inventory[product] = max(1.0, inventory[product] - consumed)

                own = max(0.0, float(day_yields.get(product, 0.0) or 0.0)) * fraction
                rival = max(0.0, float(rival_supply[day].get(product, 0.0) or 0.0)) * fraction
                if not own and not rival:
                    continue
                total = own + rival
                absorbed = min(total, max(0.0, floor_inventory[product] - inventory[product]))
                shared_midpoint = inventory[product] + 0.5 * max(0.0, absorbed - 1.0)
                quote = price(product, int(round(shared_midpoint)), market_params)
                average = (absorbed * quote + total - absorbed) / total
                # Floor-priced sales pay one but do not enter public inventory.
                # Otherwise a glut is incorrectly forecast to survive subsequent
                # shop demand long after the real market has recovered.
                margin += (own - rival) * average
                inventory[product] += absorbed

            if day < len(fixed):
                margin -= float(fixed[day] or 0.0) * fraction
        return margin

    # ------------------------------------------------------------------
    # Physical corrections

    def _repair_units(self, observation, configuration, action, step):
        player = int(observation["player"])
        original_farm = observation["farms"][player]
        original_private = observation["private"]
        farm, private = deepcopy(original_farm), deepcopy(original_private)
        positions = [farm["farmer"], *farm["hands"]]
        native = [action["farmer"], *action["hands"]]
        board = len(farm["tiles"])
        hour, day = step % 24, step // 24
        capacity = int(_get(configuration, "shedCapacity", 100))
        seed_buys = {o[1] for o in action["market"] if len(o) >= 2 and o[0] == "BUY_SEED"}
        if len(native) != len(positions):
            self._record_repair(step, "workers", ["EXPECTED", len(native) - 1],
                                ["ACTUAL", len(positions) - 1], "worker_count")
        commands = []
        for actor, position in enumerate(positions):
            original = _command(native[actor]) if actor < len(native) else ["PASS"]
            current = original
            tile = _tile(farm, position)
            inventory = private["inventories"][actor]
            queue = self._pending.get(actor, [])
            if queue and queue[0]["position"] != tuple(position):
                queue.clear()
            # Repairs consume only genuinely idle native slots. Never shift or
            # collapse movement commands and silently desynchronize a route.
            if queue and not _can_apply(original, tile, inventory, private, position, board, day):
                pending = queue[0]["command"]
                next_action = self.routes[self._selected][step + 1] if step < 718 else {}
                next_units = [next_action.get("farmer", ["PASS"]), *next_action.get("hands", [])]
                next_op = next_units[actor][0] if actor < len(next_units) else "PASS"
                if pending[0] == "PLANT" and (next_op in _MOVES or hour >= 22):
                    queue.pop(0)  # no slot for the essential first watering
                elif _can_apply(pending, tile, inventory, private, position, board, day):
                    current = queue.pop(0)["command"]
                    if current[0] == "PLANT":
                        queue.insert(0, {"position": tuple(position), "command": ["WATER"]})
            elif queue and queue[0]["command"] == original:
                queue.pop(0)
            replacement, reason, retry = self._correct_command(
                current, tile, inventory, dict(private["seeds"]), seed_buys,
                position, board, hour, step)
            if retry and hour < 22:
                entry = {"position": tuple(position), "command": list(current)}
                if not queue or queue[0] != entry:
                    queue.insert(0, entry)
            delivery = self._courier_action(
                observation, farm, private, actor, position, replacement, step, board)
            if delivery is not None:
                replacement, reason = delivery, "idle_courier"
            # Final-day cargo must physically reach the shed before the last
            # market. There is no hour23 deposit after action718.
            x, y = position
            tx, ty = min(max(x, board // 2 - 1), board // 2), min(max(y, board // 2 - 1), board // 2)
            distance = abs(x - tx) + abs(y - ty)
            cargo = any(item in PRODUCTS and quantity > 0 for item, quantity in inventory.items())
            if day == 29 and cargo and 718 - step <= distance + 2:
                replacement = (["EAST"] if x < tx else ["WEST"] if x > tx else
                               ["SOUTH"] if y < ty else ["NORTH"] if y > ty else ["DROP"])
                reason = "terminal_delivery"
                queue.clear()
            if queue:
                self._pending[actor] = queue
            else:
                self._pending.pop(actor, None)
            # Sequential exact physics gives later actors the real tile, seed,
            # and shed state, rather than the original pre-farmer snapshot.
            rules._apply_unit_action(farm, private, actor, replacement, board, day, 24, capacity)
            commands.append(replacement)
            if replacement != original:
                self._record_repair(step, actor, original, replacement, reason)
        action["farmer"], action["hands"] = commands[0], commands[1:]
        return action

    def _correct_command(
        self,
        command,
        tile,
        inventory,
        seed_budget,
        market_seed_buys,
        position,
        board_size,
        hour,
        step,
    ):
        op = command[0] if command else "PASS"

        if op == "PLANT" and len(command) >= 2:
            crop = command[1]
            if isinstance(tile, dict) and tile.get("kind") == "WEED":
                return ["DIG"], "weed_before_plant", True
            if tile is None:
                if seed_budget.get(crop, 0) > 0:
                    seed_budget[crop] -= 1
                    return command, "native", False
                # A same-turn seed buy arrives after unit actions.  Delay once
                # and consume it next turn rather than losing every atomic
                # planting request for this crop.
                if crop in market_seed_buys:
                    return ["PASS"], "seed_arrives_after_units", True
                return ["PASS"], "native_missing_seed", False
            if (
                isinstance(tile, dict)
                and tile.get("kind") == "PLANT"
                and tile.get("crop") == crop
                and not tile.get("watered_today")
            ):
                return ["WATER"], "plant_already_present", False
            return ["PASS"], "occupied_plant_site", False

        if op in ("BUILD_COOP", "BUILD_PASTURE"):
            if isinstance(tile, dict) and tile.get("kind") == "WEED":
                return ["DIG"], "weed_before_build", True
            return command, "native", False

        if op == "WATER":
            if (
                isinstance(tile, dict)
                and tile.get("kind") == "PLANT"
                and not tile.get("watered_today")
            ):
                return command, "native", False
            useful = self._late_useful(tile, inventory, position, board_size, hour, step)
            return (useful, "missed_watering_repair", False) if useful else (command, "native", False)

        if op == "FEED" and isinstance(tile, dict) and tile.get("animal"):
            if tile.get("fed_today"):
                useful = self._late_useful(tile, inventory, position, board_size, hour, step)
                return (useful, "duplicate_feed", False) if useful else (command, "native", False)
            if int(inventory.get("WHEAT", 0) or 0) <= 0:
                useful = self._late_useful(tile, inventory, position, board_size, hour, step)
                return (useful, "feed_without_carried_wheat", False) if useful else (command, "native", False)


        if op == "PASS":
            useful = self._late_useful(tile, inventory, position, board_size, hour, step)
            if useful:
                return useful, "late_useful_action", False
        return command, "native", False

    def _late_useful(self, tile, inventory, position, board_size, hour, step):
        if isinstance(tile, dict) and tile.get("kind") == "PLANT":
            if (
                not tile.get("watered_today")
                and (int(tile.get("consecutive_unwatered", 0) or 0) > 0 or hour >= 20)
            ):
                return ["WATER"]
            crop = tile.get("crop")
            info = CROP_INFO.get(crop, {})
            mature = step // 24 - int(tile.get("planted_day", 0) or 0) >= int(
                info.get("first_yield_day", 0) or 0
            )
            if (
                mature
                and int(tile.get("yield_units", 0) or 0) > 0
                and (info.get("ongoing") or step // 24 == 29
                     or step // 24 - tile.get("planted_day", 0) >= info.get("max_yield_day", 0)
                     or tile.get("yield_units", 0) >= info.get("max_yield", 0))
                and (hour >= 21 or step >= 712)
            ):
                return ["HARVEST"]
            return None

        if isinstance(tile, dict) and tile.get("animal"):
            if (
                not tile.get("fed_today")
                and int(inventory.get("WHEAT", 0) or 0) > 0
                and (int(tile.get("consecutive_unfed", 0) or 0) > 0 or hour >= 19)
            ):
                return ["FEED"]
            if (
                int(tile.get("yield_units", 0) or 0) > 0
                and (hour >= 20 or step >= 712)
            ):
                return ["HARVEST"]
            if (
                tile.get("fed_today")
                and not tile.get("cared_today")
                and hour >= 20
            ):
                return ["CARE"]
            if tile.get("fertilizer_available") and hour >= 22:
                return ["COLLECT_FERTILIZER"]
            return None

        if isinstance(tile, dict) and tile.get("kind") == "WEED":
            return ["DIG"]
        if inventory and _shed_adjacent(position, board_size) and hour >= 22:
            return ["DROP"]
        return None


    def _courier_action(self, observation, farm, private, actor, position, native, step, board):
        """Use idle windows for a delivery and return to the exact route position."""
        x, y = position
        center = (min(max(x, board // 2 - 1), board // 2),
                  min(max(y, board // 2 - 1), board // 2))
        trip = self._couriers.get(actor)

        def move_to(target):
            return (["EAST"] if x < target[0] else ["WEST"] if x > target[0] else
                    ["SOUTH"] if y < target[1] else ["NORTH"] if y > target[1] else None)

        inventory = private["inventories"][actor]
        if trip is not None and trip["returning"]:
            command = move_to(trip["home"])
            if command is not None:
                return command
            self._couriers.pop(actor)
            trip = None

        # A planned productive command always wins over starting a new detour.
        if trip is None and _can_apply(native, _tile(farm, position), inventory,
                                       private, position, board, step // 24):
            return None
        needed = {"WHEAT": 0, "FERTILIZER": 0}
        for turn in range(step + 1, min(719, (step // 24 + 1) * 24)):
            action = self.routes[self._selected][turn]
            units = [action.get("farmer", ["PASS"]), *action.get("hands", [])]
            command = units[actor] if actor < len(units) else ["PASS"]
            if command and command[0] == "FEED":
                needed["WHEAT"] += 1
            elif command and command[0] == "FERTILIZE":
                needed["FERTILIZER"] += 1
        ready = {item: quantity - needed.get(item, 0)
                 for item, quantity in inventory.items()
                 if item in PRODUCTS and quantity > needed.get(item, 0)}
        if not ready:
            return None
        distance = abs(x - center[0]) + abs(y - center[1])
        if trip is None and distance:
            # Every still-compatible continuation must leave this actor idle
            # through the full out/drop/back trip, with no dawn crossing.
            end = step + 2 * distance
            if end >= min(719, (step // 24 + 1) * 24):
                return None
            for route_id in self._compatible:
                route = self.routes[route_id]
                for turn in range(step + 1, end + 1):
                    action = route[turn]
                    units = [action.get("farmer", ["PASS"]), *action.get("hands", [])]
                    command = units[actor] if actor < len(units) else ["PASS"]
                    if command and command[0] != "PASS":
                        return None
            trip = {"home": tuple(position), "returning": False}
            self._couriers[actor] = trip
        if distance:
            return move_to(center)
        room = max(0, 100 - sum(private["shed"].values()))
        if trip is not None:
            trip["returning"] = True
        if not room:
            return None
        if ready == inventory and sum(inventory.values()) <= room:
            return ["DROP"]
        prices = observation["market"]["prices"]
        item = max(ready, key=lambda key: prices[key] * min(ready[key], room))
        return ["PLACE", item, min(ready[item], room)]

    def _record_repair(self, step, actor, before, after, reason, effective=True):
        self.diagnostics["repairs"].append(
            {
                "step": step,
                "actor": actor,
                "from": tuple(before),
                "to": tuple(after),
                "reason": reason,
                "effective": bool(effective),
            }
        )
