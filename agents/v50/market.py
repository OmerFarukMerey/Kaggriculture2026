"""Inventory-safe market modeling and queue optimization for v50.

Production intent is not an account ledger. Unit actions are projected with
the authoritative mechanics module, and all proposed queues are executed by
the exact ten-slot market simulator.
"""
from __future__ import annotations

from math import ceil
from typing import Any, Iterable

from .mechanics import (
    ANIMAL_COST,
    ANIMAL_INFO,
    CROP_INFO,
    PRODUCTS,
    SEED_PRICE,
    execute_market,
    price,
    project_units,
    town_consumption,
)

_INPUTS = ("WHEAT", "FERTILIZER")
_ANIMALS = tuple(ANIMAL_COST)
_LAST_STEP = 718
_PRODUCTION_CUTOFF = 695
_LAND_COST = (1000, 2000, 4000)


def _get(value: Any, key: str, default: Any = None) -> Any:
    if isinstance(value, dict):
        return value.get(key, default)
    getter = getattr(value, "get", None)
    if callable(getter):
        return getter(key, default)
    return getattr(value, key, default)


def _number(value: Any, default: int = 0) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _step(observation: Any) -> int:
    value = _get(observation, "step", None)
    if value is not None:
        return _number(value)
    return 24 * _number(_get(observation, "day", 0)) + _number(
        _get(observation, "hour", 0)
    )


def _quantity(order: Iterable[Any]) -> int:
    order = list(order)
    return max(0, _number(order[2])) if len(order) >= 3 else 0


def _commands(action: Any) -> list[list[Any]]:
    if not isinstance(action, dict):
        return []
    result = [list(action.get("farmer") or ["PASS"])]
    result.extend(list(command or ["PASS"]) for command in action.get("hands", []) or [])
    return result


def _fib(index: int) -> int:
    a, b = 1, 1
    for _ in range(max(0, index)):
        a, b = b, a + b
    return a


def _positive_map(value: Any) -> dict[str, int]:
    return {
        str(item): max(0, _number(quantity))
        for item, quantity in dict(value or {}).items()
        if _number(quantity) > 0
    }


class MarketController:
    """Build cash- and shed-feasible queues around a production policy.

    Assumptions used deliberately by the policy:

    * only post-unit shed stock may be sold this turn;
    * working-input reserves come from the selected production policy;
    * inferred opponent flow is an uncertain aggregate, never a future action
      tape.  Queue choices must also survive no-opponent and adverse-flow cases;
    * carried inventory at hour 23 is unavailable to the market and needs shed
      room for the subsequent dawn deposit.
    """

    def __init__(self) -> None:
        self.diagnostics: dict[str, Any] = {
            "resets": 0,
            "observed_transitions": 0,
            "removed_dead_orders": 0,
            "input_topups": 0,
            "delayed_sales": 0,
            "overflow_sales": 0,
            "errors": 0,
            "queue_candidates": 0,
            "flow": {},
            "last": {},
        }
        self._route_cache: dict[int, dict[str, Any]] = {}
        self._reset(count=False)

    def _reset(self, *, count: bool = True) -> None:
        if count:
            self.diagnostics["resets"] += 1
        self._last_step = -1
        self._last_inventory: dict[str, int] | None = None
        self._last_snapshot: dict[str, Any] | None = None
        self._last_own_net: dict[str, int] = {}
        self._flow = {
            item: {"mean": 0.0, "deviation": 0.0, "fit": 0.0, "count": 0}
            for item in PRODUCTS
        }

    def _observe_transition(self, observation: Any, step: int) -> None:
        market = _get(observation, "market", {}) or {}
        current = _positive_map(_get(market, "inventory", {}) or {})
        if (
            self._last_inventory is not None
            and self._last_snapshot is not None
            and self._last_step == step - 1
        ):
            drain = town_consumption(
                self._last_snapshot, step=self._last_step, expected=False
            )
            for item in PRODUCTS:
                delta = current.get(item, 0) - self._last_inventory.get(item, 0)
                sample = (
                    delta
                    - _number(self._last_own_net.get(item, 0))
                    + _number(_get(drain, item, 0))
                )
                # A single route sale can be large.  Bounding only pathological
                # observation jumps keeps one reset/glitch from owning the model.
                sample = max(-100, min(150, sample))
                model = self._flow[item]
                old_mean = float(model["mean"])
                residual = abs(sample - old_mean)
                alpha = 0.32 if model["count"] < 5 else 0.18
                model["mean"] = old_mean + alpha * (sample - old_mean)
                model["deviation"] = (1.0 - alpha) * float(
                    model["deviation"]
                ) + alpha * residual
                local_fit = 1.0 / (1.0 + residual / (2.0 + abs(old_mean)))
                model["fit"] = (1.0 - alpha) * float(model["fit"]) + alpha * local_fit
                model["count"] += 1
            self.diagnostics["observed_transitions"] += 1
        self.diagnostics["flow"] = {
            item: {
                "mean": round(float(model["mean"]), 2),
                "deviation": round(float(model["deviation"]), 2),
                "confidence": round(self._confidence(model), 3),
            }
            for item, model in self._flow.items()
        }

    @staticmethod
    def _confidence(model: dict[str, Any]) -> float:
        evidence = _number(model.get("count"))
        return min(0.82, evidence / (evidence + 8.0)) * max(
            0.0, min(1.0, float(model.get("fit", 0.0)))
        )

    def _route_analysis(self, route: list[dict[str, Any]]) -> dict[str, Any]:
        key = id(route)
        cached = self._route_cache.get(key)
        if cached is not None and cached.get("route") is route:
            return cached
        length = len(route)
        plants = {item: [0] * (length + 1) for item in SEED_PRICE}
        places = {item: [0] * (length + 1) for item in _ANIMALS}
        for turn in range(length - 1, -1, -1):
            for table in (plants, places):
                for item, values in table.items():
                    values[turn] = values[turn + 1]
            action = route[turn] if isinstance(route[turn], dict) else {}
            for command in _commands(action):
                if len(command) >= 2 and command[0] == "PLANT" and command[1] in plants:
                    if turn // 24 + CROP_INFO[command[1]]["first_yield_day"] <= 29:
                        plants[command[1]][turn] += 1
                elif len(command) >= 2 and command[0] == "PLACE" and command[1] in places:
                    if turn // 24 + ANIMAL_INFO[command[1]]["first_yield_day"] <= 29:
                        places[command[1]][turn] += 1
        cached = {"route": route, "plants": plants, "places": places}
        self._route_cache[key] = cached
        return cached

    @staticmethod
    def _future_pickups(route, step, item, horizon):
        need = 0
        for turn in range(step + 1, min(len(route), step + horizon + 1, _LAST_STEP + 1)):
            for command in _commands(route[turn]):
                if len(command) >= 2 and command[0] == "PICKUP" and command[1] == item:
                    need += max(0, _number(command[2], 1) if len(command) >= 3 else 1)
        return need

    def _reserves(self, route, step, private):
        hold, purchase = {}, {}
        for item in _INPUTS:
            # WHEAT feeding cannot create any more production after the final
            # dawn. FERTILIZER can still improve an annual crop's WATER action.
            if step >= _PRODUCTION_CUTOFF and item == "WHEAT":
                hold[item] = purchase[item] = 0
                continue
            returning = (sum(_number(inv.get(item, 0)) for inv in private["inventories"])
                         if step % 24 == 23 else 0)
            hold[item] = min(100, max(0, self._future_pickups(route, step, item, 12) - returning))
            purchase[item] = min(100, max(0, self._future_pickups(route, step, item, 1) - returning))
        return hold, purchase

    def _useful_fixed_quantity(
        self,
        op: str,
        item: str,
        requested: int,
        route: list[dict[str, Any]],
        step: int,
        private: dict[str, Any],
        analysis: dict[str, Any],
    ) -> int:
        if requested <= 0 or step >= _PRODUCTION_CUTOFF:
            return 0
        if op == "BUY_SEED" and item in SEED_PRICE:
            seeds = _positive_map(_get(private, "seeds", {}) or {})
            future = analysis["plants"][item][min(step + 1, len(route))]
            return min(requested, max(0, future - seeds.get(item, 0)))
        if op == "BUY_ANIMAL" and item in ANIMAL_COST:
            shed = _positive_map(_get(private, "shed", {}) or {})
            carried = sum(
                _number(_get(inventory, item, 0))
                for inventory in (_get(private, "inventories", []) or [])
            )
            future = analysis["places"][item][min(step + 1, len(route))]
            return min(requested, max(0, future - shed.get(item, 0) - carried))
        return requested

    @staticmethod
    def _fixed_cost(
        orders: list[list[Any]], farm: dict[str, Any], prices: dict[str, int]
    ) -> int:
        hires = _number(_get(farm, "hires_today", 0))
        quadrants = len(_get(farm, "unlocked_quadrants", []) or [])
        cost = 0
        for order in orders:
            if not order:
                continue
            op = order[0]
            if op == "HIRE":
                cost += _fib(hires)
                hires += 1
            elif op == "BUY_LAND":
                index = max(0, quadrants - 1)
                if index < len(_LAND_COST):
                    cost += _LAND_COST[index]
                    quadrants += 1
            elif len(order) >= 3:
                item, quantity = str(order[1]), _quantity(order)
                if op == "BUY_SEED":
                    cost += _number(SEED_PRICE.get(item, 0)) * quantity
                elif op == "BUY_ANIMAL":
                    cost += _number(ANIMAL_COST.get(item, 0)) * quantity
                elif op == "BUY_PRODUCT":
                    cost += max(1, prices.get(item, 1)) * quantity
        return cost

    def _sale_revenue(
        self,
        item: str,
        inventory: int,
        quantity: int,
        market_params: Any,
        cache: dict[tuple[str, int], int],
    ) -> int:
        revenue = 0
        level = inventory
        for _ in range(max(0, quantity)):
            key = (item, level)
            quote = cache.get(key)
            if quote is None:
                quote = price(item, level, market_params)
                cache[key] = quote
            revenue += quote
            if quote > 1:
                level += 1
        return revenue

    def _should_delay_sale(
        self,
        observation: Any,
        step: int,
        item: str,
        quantity: int,
        inventory: int,
        market_params: Any,
        needs_cash: bool,
        storage_safe: bool,
        cache: dict[tuple[str, int], int],
    ) -> bool:
        if (
            quantity <= 0
            or needs_cash
            or not storage_safe
            or step >= _LAST_STEP - 2
            or step % 24 == 23
        ):
            return False
        drain = town_consumption(observation, step=step, expected=False)
        revealed = max(0, _number(_get(drain, item, 0)))
        if revealed <= 0:
            return False
        # Use the same competing-supply scenario as queue selection. An absence
        # of observed flow does not establish that the rival has no stored crop.
        adverse_supply = self._adverse_quantity(item, "SELL")
        now = self._sale_revenue(item, inventory, quantity, market_params, cache)
        future_inventory = max(0, inventory - revealed + adverse_supply)
        later = self._sale_revenue(
            item, future_inventory, quantity, market_params, cache
        )
        return later >= now + max(2, quantity)

    def _rival_prediction(self) -> list[list[Any]]:
        predicted: list[list[Any]] = []
        ranked: list[tuple[float, list[Any]]] = []
        for item, model in self._flow.items():
            confidence = self._confidence(model)
            amount = float(model["mean"]) * confidence
            quantity = min(40, int(round(abs(amount))))
            if quantity <= 0 or confidence < 0.08:
                continue
            if amount > 0:
                order = ["SELL", item, quantity]
            elif item in _INPUTS:
                order = ["BUY_PRODUCT", item, quantity]
            else:
                continue
            ranked.append((abs(amount), order))
        ranked.sort(key=lambda pair: (-pair[0], pair[1][1]))
        slots = (1, 4, 7, 9)
        for index, (_, order) in zip(slots, ranked[: len(slots)]):
            while len(predicted) < index:
                predicted.append([])
            predicted.append(order)
        return predicted[:10]

    def _adverse_quantity(self, item: str, operation: str) -> int:
        model = self._flow.get(item, {})
        confidence = self._confidence(model) if model else 0.0
        mean = float(model.get("mean", 0.0))
        base = max(0.0, mean if operation == "SELL" else -mean)
        spread = float(model.get("deviation", 0.0))
        return min(30, max(5, ceil((base + 2.0 * spread) * confidence)))

    def _rival_adverse(
        self, queue: list[list[Any]], inventory: dict[str, int], market_params: Any
    ) -> list[list[Any]]:
        threats: dict[tuple[str, str], tuple[float, list[Any]]] = {}
        for order in queue[:10]:
            if len(order) < 3 or order[0] not in ("SELL", "BUY_PRODUCT"):
                continue
            operation, item = str(order[0]), str(order[1])
            if operation == "BUY_PRODUCT" and item not in _INPUTS:
                continue
            quantity = self._adverse_quantity(item, operation)
            current = inventory.get(item, 10000)
            shifted = current + quantity if operation == "SELL" else max(0, current - quantity)
            exposure = abs(price(item, shifted, market_params) - price(item, current, market_params))
            risk = exposure * max(0, _number(order[2]))
            key = operation, item
            previous = threats.get(key)
            threats[key] = ((previous[0] if previous else 0) + risk, [operation, item, quantity])
        # Opponent slots cannot move with each candidate we evaluate: doing so
        # erases the benefit of selling before a competing supply shock.
        ranked = sorted(threats.values(), key=lambda entry: (-entry[0], entry[1][1], entry[1][0]))
        return [order for _, order in ranked]

    @staticmethod
    def _queue_key(queue: list[list[Any]]) -> tuple[tuple[Any, ...], ...]:
        return tuple(tuple(order) for order in queue)

    def _candidate_queues(
        self, orders: list[list[Any]], max_orders: int, consider_empty: bool
    ) -> list[list[list[Any]]]:
        orders = [list(order) for order in orders if isinstance(order, list)]
        base = orders[:max_orders]
        sells = [order for order in base if order and order[0] == "SELL"]
        inputs = [order for order in base if order and order[0] == "BUY_PRODUCT"]
        fixed = [
            order
            for order in base
            if order and order[0] not in ("SELL", "BUY_PRODUCT")
        ]
        empty = [order for order in base if not order]
        seeds = [
            base,
            sells + fixed + inputs + empty,
            sells + inputs + fixed + empty,
            fixed + sells + inputs + empty,
            fixed + inputs + sells + empty,
            inputs + fixed + sells + empty,
            list(reversed(sells)) + fixed + inputs + empty,
        ]
        # Adjacent swaps cheaply cover most funding/capacity interactions while
        # preserving the real slot indices used by the simulator.
        for index in range(max(0, len(base) - 1)):
            swapped = list(base)
            swapped[index], swapped[index + 1] = swapped[index + 1], swapped[index]
            seeds.append(swapped)
        candidates: list[list[list[Any]]] = []
        seen: set[tuple[tuple[Any, ...], ...]] = set()
        for seed in seeds:
            variants = [seed[:max_orders]]
            without_empty = [order for order in seed if order]
            if consider_empty and len(without_empty) < max_orders:
                variants.extend(
                    without_empty[:position] + [[]] + without_empty[position:]
                    for position in range(len(without_empty) + 1)
                )
            for queue in variants:
                queue = queue[:max_orders]
                key = self._queue_key(queue)
                if key not in seen:
                    seen.add(key)
                    candidates.append(queue)
        return candidates[:96]

    def _score_queue(
        self,
        queue: list[list[Any]],
        farm: dict[str, Any],
        private: dict[str, Any],
        market_inventory: dict[str, int],
        market_params: Any,
        configuration: Any,
        reserve: dict[str, int],
        carried: int,
        shed_capacity: int,
        hour: int,
        terminal: bool,
    ) -> tuple[tuple[float, float], dict[str, Any]]:
        rival_queues = (
            [], self._rival_prediction(),
            self._rival_adverse(queue, market_inventory, market_params),
        )
        results = [
            execute_market(
                queue,
                rival,
                farm,
                private,
                market_inventory,
                market_params,
                configuration,
            )
            for rival in rival_queues
        ]
        scores: list[float] = []
        for outcome in results:
            shed = _positive_map(outcome.get("shed", {}) or {})
            missing = sum(max(0, reserve.get(item, 0) - shed.get(item, 0)) for item in _INPUTS)
            overflow = (
                max(0, sum(shed.values()) + carried - shed_capacity)
                if hour == 23
                else 0
            )
            leftovers = sum(shed.get(item, 0) for item in PRODUCTS) if terminal else 0
            # fixed_spend is route utility (seeds, animals, land, and hands), not
            # a cost to minimize.  A weight just over two makes a funded route
            # purchase preferable to keeping its cash, without valuing inputs as
            # speculative resale inventory.
            score = (
                float(outcome.get("money", 0.0))
                + 2.05 * float(outcome.get("fixed_spend", 0.0))
                - 100000.0 * missing
                - 50000.0 * overflow
                - 10000.0 * leftovers
            )
            scores.append(score)
        objective = (min(scores), sum(scores) / len(scores))
        return objective, results[1]

    def _optimize_queue(
        self,
        orders: list[list[Any]],
        max_orders: int,
        farm: dict[str, Any],
        private: dict[str, Any],
        market_inventory: dict[str, int],
        market_params: Any,
        configuration: Any,
        reserve: dict[str, int],
        carried: int,
        shed_capacity: int,
        hour: int,
        terminal: bool,
        consider_empty: bool,
    ) -> tuple[list[list[Any]], dict[str, Any], tuple[float, float]]:
        candidates = self._candidate_queues(orders, max_orders, consider_empty)
        self.diagnostics["queue_candidates"] += len(candidates)
        best_queue: list[list[Any]] = []
        best_result: dict[str, Any] = {}
        best_score = (-float("inf"), -float("inf"))
        for queue in candidates:
            objective, tracked = self._score_queue(
                queue,
                farm,
                private,
                market_inventory,
                market_params,
                configuration,
                reserve,
                carried,
                shed_capacity,
                hour,
                terminal,
            )
            if objective > best_score:
                best_score = objective
                best_queue = queue
                best_result = tracked
        return best_queue, best_result, best_score

    def act(
        self,
        observation: Any,
        configuration: Any,
        action_dict: dict[str, Any],
        full_selected_route: list[dict[str, Any]],
    ) -> dict[str, Any]:
        """Return ``action_dict`` with a feasible, simulated market queue."""
        step = _step(observation)
        if step < self._last_step:
            self._reset()
        self._observe_transition(observation, step)

        player = _number(_get(observation, "player", 0))
        farms = list(_get(observation, "farms", []) or [])
        if player < 0 or player >= len(farms):
            self.diagnostics["errors"] += 1
            raise ValueError("observation does not contain this player's farm")
        if not isinstance(action_dict, dict):
            self.diagnostics["errors"] += 1
            raise TypeError("action_dict must be a dictionary")
        if not isinstance(full_selected_route, list):
            self.diagnostics["errors"] += 1
            raise TypeError("full_selected_route must be the selected route list")

        configuration = configuration or {}
        turns_per_day = max(1, _number(_get(configuration, "turnsPerDay", 24), 24))
        shed_capacity = max(1, _number(_get(configuration, "shedCapacity", 100), 100))
        max_orders = max(
            0,
            min(10, _number(_get(configuration, "maxMarketOrdersPerTurn", 10), 10)),
        )
        hour = step % turns_per_day
        terminal = step >= _LAST_STEP

        projected_farm, projected_private = project_units(
            observation, action_dict, configuration
        )
        shed = _positive_map(_get(projected_private, "shed", {}) or {})
        carried = sum(
            sum(_positive_map(inventory).values())
            for inventory in (_get(projected_private, "inventories", []) or [])
        )
        held_reserve, purchase_need = self._reserves(
            full_selected_route, step, projected_private
        )
        analysis = self._route_analysis(full_selected_route)

        market = _get(observation, "market", {}) or {}
        market_inventory = _positive_map(_get(market, "inventory", {}) or {})
        prices = _positive_map(_get(market, "prices", {}) or {})
        market_params = _get(market, "params", None)
        native = [list(order or []) for order in action_dict.get("market", []) or []]
        native_empty = any(not order for order in native[:max_orders])

        cleaned: list[list[Any]] = []
        kept_input = {item: 0 for item in _INPUTS}
        dead_removed = 0

        for order in native[:10]:
            if not order:
                cleaned.append([])
                continue
            op = str(order[0])
            if op == "SELL" and len(order) >= 2 and str(order[1]) in PRODUCTS:
                continue
            if op == "HIRE":
                if step >= _LAST_STEP - 1 or hour == turns_per_day - 1:
                    dead_removed += 1
                else:
                    cleaned.append(["HIRE"])
                continue
            if op == "BUY_LAND":
                if step >= _PRODUCTION_CUTOFF:
                    dead_removed += 1
                else:
                    cleaned.append(["BUY_LAND"])
                continue
            if len(order) < 3:
                # Keep an intentional invalid order as a real lockstep slot.
                cleaned.append(order)
                continue
            item, requested = str(order[1]), _quantity(order)
            if op in ("BUY_SEED", "BUY_ANIMAL"):
                useful = self._useful_fixed_quantity(
                    op,
                    item,
                    requested,
                    full_selected_route,
                    step,
                    projected_private,
                    analysis,
                )
                if useful > 0:
                    cleaned.append([op, item, useful])
                else:
                    dead_removed += 1
                continue
            if op == "BUY_PRODUCT" and item in _INPUTS:
                useful_total = max(0, purchase_need[item] - shed.get(item, 0))
                useful = min(requested, max(0, useful_total - kept_input[item]))
                if useful > 0 and not terminal:
                    cleaned.append([op, item, useful])
                    kept_input[item] += useful
                else:
                    dead_removed += 1
                continue
            # Unknown native market operations are retained; execute_market is
            # the authority on whether they are valid and affordable.
            cleaned.append(order)

        for item in _INPUTS:
            deficit = max(
                0,
                purchase_need[item] - shed.get(item, 0) - kept_input[item],
            )
            if deficit > 0 and not terminal:
                cleaned.append(["BUY_PRODUCT", item, deficit])
                kept_input[item] += deficit
                self.diagnostics["input_topups"] += deficit

        # A failed earlier purchase is not a reason to miss the next planting or
        # animal pickup. Recompute these obligations from observed stock.
        next_plants = {}
        next_animals = {}
        if step < _LAST_STEP:
            for command in _commands(full_selected_route[step + 1]):
                if len(command) < 2:
                    continue
                op, item = command[:2]
                if op == "PLANT" and item in CROP_INFO:
                    if (step + 1) // 24 + CROP_INFO[item]["first_yield_day"] <= 29:
                        next_plants[item] = next_plants.get(item, 0) + 1
                elif op == "PICKUP" and item in ANIMAL_COST:
                    quantity = _number(command[2], 1) if len(command) >= 3 else 1
                    next_animals[item] = next_animals.get(item, 0) + max(0, quantity)
        for op, needs, stock in (("BUY_SEED", next_plants, projected_private["seeds"]),
                                 ("BUY_ANIMAL", next_animals, shed)):
            for item, wanted in needs.items():
                planned = sum(_quantity(o) for o in cleaned if len(o) >= 3 and o[:2] == [op, item])
                shortage = max(0, wanted - stock.get(item, 0) - planned)
                if shortage:
                    cleaned.append([op, item, shortage])
                    self.diagnostics["input_topups"] += shortage

        rough_cost = self._fixed_cost(cleaned, projected_farm, prices)
        quote_risk = sum(
            _quantity(order) * max(5, prices.get(str(order[1]), 1) // 10)
            for order in cleaned
            if len(order) >= 3 and order[0] == "BUY_PRODUCT"
        )
        needs_cash = rough_cost + quote_risk > float(
            _get(projected_farm, "money", 0.0) or 0.0
        )
        quote_cache: dict[tuple[str, int], int] = {}
        sales: dict[str, int] = {}
        delayed: list[str] = []

        # Every ready product competes for its current marginal price. A delayed
        # sale is reconsidered next turn, not forgotten until a tape SELL.
        for item in PRODUCTS:
            available = max(0, shed.get(item, 0) - held_reserve.get(item, 0))
            if available <= 0:
                continue
            if self._should_delay_sale(
                observation,
                step,
                item,
                available,
                market_inventory.get(item, 10000),
                market_params,
                needs_cash,
                sum(shed.values()) + carried <= shed_capacity - 4,
                quote_cache,
            ):
                delayed.append(item)
                continue
            sales[item] = available


        # Dawn cargo cannot be sold on hour 23.  Sell existing shed stock now so
        # the later deposit has room; buys remain subject to the same exact cap.
        overflow_target = (
            max(0, sum(shed.values()) + carried + sum(kept_input.values()) - shed_capacity)
            if hour == turns_per_day - 1
            else 0
        )
        already_sold = sum(sales.values())
        remaining_overflow = max(0, overflow_target - already_sold)
        if remaining_overflow:
            candidates = sorted(
                PRODUCTS,
                key=lambda item: (
                    item in _INPUTS and purchase_need.get(item, 0) > 0,
                    prices.get(item, 0),
                    item,
                ),
            )
            for item in candidates:
                unsold = max(0, shed.get(item, 0) - sales.get(item, 0))
                quantity = min(remaining_overflow, unsold)
                if quantity:
                    sales[item] = sales.get(item, 0) + quantity
                    remaining_overflow -= quantity
                    self.diagnostics["overflow_sales"] += quantity
                if remaining_overflow <= 0:
                    break

        self.diagnostics["removed_dead_orders"] += dead_removed
        self.diagnostics["delayed_sales"] += len(delayed)

        # Replace route SELL counts with physical post-unit stock.  Put sales at
        # the front of the candidate seed when they are needed to fund purchases;
        # the bounded optimizer still evaluates the other actual slot orders.
        sale_orders = [
            ["SELL", item, quantity]
            for item, quantity in sorted(
                sales.items(), key=lambda pair: (-prices.get(pair[0], 0), pair[0])
            )
            if quantity > 0
        ]
        if terminal:
            orders = sale_orders
        elif needs_cash:
            orders = sale_orders + cleaned
        else:
            orders = cleaned + sale_orders

        # Prefer real intentions over empty slots when the ten-slot cap binds.
        if len(orders) > max_orders:
            nonempty = [order for order in orders if order]
            orders = nonempty[:max_orders]
        effective_reserve = {
            item: min(purchase_need[item], shed.get(item, 0) + kept_input[item])
            for item in _INPUTS
        }
        consider_empty = native_empty or any(
            self._confidence(model) >= 0.08 for model in self._flow.values()
        )
        queue, tracked, objective = self._optimize_queue(
            orders,
            max_orders,
            projected_farm,
            projected_private,
            market_inventory,
            market_params,
            configuration,
            effective_reserve,
            carried,
            shed_capacity,
            hour,
            terminal,
            consider_empty,
        )

        result = dict(action_dict)
        result["market"] = [list(order) for order in queue]
        self._last_step = step
        self._last_inventory = dict(market_inventory)
        self._last_snapshot = {
            "step": step,
            "day": _number(_get(observation, "day", step // turns_per_day)),
            "hour": hour,
            "town": {
                "unlocked_shops": list(
                    _get(_get(observation, "town", {}) or {}, "unlocked_shops", [])
                    or []
                )
            },
        }
        self._last_own_net = {
            item: _number(quantity)
            for item, quantity in dict(tracked.get("net", {}) or {}).items()
        }
        self.diagnostics["last"] = {
            "step": step,
            "cash": float(_get(projected_farm, "money", 0.0) or 0.0),
            "post_unit_shed": dict(shed),
            "carried": carried,
            "reserve": dict(held_reserve),
            "purchase_need": dict(purchase_need),
            "sales": dict(sales),
            "delayed": delayed,
            "dead_orders_removed": dead_removed,
            "queue": [list(order) for order in queue],
            "worst_score": round(objective[0], 2),
            "mean_score": round(objective[1], 2),
            "tracked_net": dict(self._last_own_net),
            "assumptions": {
                "cash": "only simulated sales may fund later slots",
                "inputs": "hold twelve-turn pickups; buy only next-turn deficits",
                "opponent": "weighted observed net flow plus no-op/adverse scenarios",
            },
        }
        return result
