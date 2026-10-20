"""Climb-safe sparse shop router.

The policy deliberately has only two route-changing observations:

* first unlocked shop is YARN_STORE -> use the validated yarn-first suffix;
* second unlocked shop is YARN_STORE -> use the validated yarn-second suffix.

All route policies are advanced on every turn.  This keeps their bounded weed
repair transactions synchronized before a suffix is selected.  BAKERY does
not select a farm route: it only enables an independent, reserve-safe EGG
market-making expert, and only after the shop is publicly visible.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from v23.planner import PlannerConfig, build_sparse_planner
from v23.state_encoder import get
from v24.market_maker import MarketMakerConfig, MarketMakerExpert


@dataclass(frozen=True)
class SparseShopRouterConfig:
    yarn_first_start: int = 88
    yarn_second_start: int = 153
    bakery_market_maker: bool = False
    egg_batch: int = 10
    egg_cash_reserve: float = 2500.0
    egg_start_step: int = 72
    egg_stop_entry_step: int = 716
    feed_days_reserve: float = 2.0
    investment_horizon: int = 2
    shed_headroom: int = 15
    minimum_expected_profit: float = 1.0


def _shops(obs: Any) -> list[str]:
    town = get(obs, "town", {}) or {}
    return [str(value) for value in (get(town, "unlocked_shops", []) or [])]


def selected_route(obs: Any, config: SparseShopRouterConfig) -> str:
    """Return the route selected from information already visible this turn."""
    step = int(get(obs, "step", 0) or 0)
    shops = _shops(obs)
    if shops and shops[0] == "YARN_STORE" and step >= config.yarn_first_start:
        return "yarn_first"
    if (
        len(shops) >= 2
        and shops[0] != "YARN_STORE"
        and shops[1] == "YARN_STORE"
        and step >= config.yarn_second_start
    ):
        return "yarn_second"
    return "default"


def build_sparse_shop_router(
    routes: dict[str, list[dict]],
    config: SparseShopRouterConfig = SparseShopRouterConfig(),
):
    """Build the three-route policy with an optional BAKERY-only market expert."""
    required = {"default", "yarn_first", "yarn_second"}
    missing = required.difference(routes)
    if missing:
        raise ValueError(f"missing routes: {sorted(missing)}")

    planner_config = PlannerConfig()
    children = {
        name: build_sparse_planner(routes[name], planner_config)
        for name in sorted(required)
    }
    egg_expert = MarketMakerExpert(
        routes["default"],
        MarketMakerConfig(
            enabled=bool(config.bakery_market_maker),
            item="EGG",
            feed_item="WHEAT",
            start_step=int(config.egg_start_step),
            stop_entry_step=int(config.egg_stop_entry_step),
            max_batch=int(config.egg_batch),
            minimum_expected_profit=float(config.minimum_expected_profit),
            mirror_minimum_expected_profit=float(config.minimum_expected_profit),
            minimum_cash_reserve=float(config.egg_cash_reserve),
            feed_days_reserve=float(config.feed_days_reserve),
            investment_horizon=int(config.investment_horizon),
            shed_headroom=int(config.shed_headroom),
        ),
    )
    telemetry = {
        "calls": 0,
        "selected": {name: 0 for name in sorted(required)},
        "bakery_games": 0,
        "bakery_market_turns": 0,
    }
    bakery_seen = {0: False, 1: False}
    last_step = {0: -1, 1: -1}
    states = {0: {}, 1: {}}

    def agent(obs, configuration=None):
        seat = 1 if int(get(obs, "player", 0) or 0) == 1 else 0
        step = int(get(obs, "step", 0) or 0)
        if step == 0 or step < last_step[seat]:
            bakery_seen[seat] = False
        last_step[seat] = step

        shops = _shops(obs)
        if "BAKERY" in shops and not bakery_seen[seat]:
            bakery_seen[seat] = True
            telemetry["bakery_games"] += 1

        # Every stateful child must observe every turn.  Selecting first and
        # calling only that child can leave weed-repair state uninitialized at
        # a late route switch.
        actions = {
            name: policy(obs, configuration)
            for name, policy in children.items()
        }
        route = selected_route(obs, config)
        result = actions[route]

        # Initialize the MM state at game start, but do not let it enter until
        # a BAKERY is actually public.  Shops are monotonic, so once enabled it
        # remains enabled long enough to close every one-turn position.
        if step == 0:
            egg_expert.apply(obs, result, configuration)
        elif config.bakery_market_maker and bakery_seen[seat]:
            before = list(result.get("market", []) or [])
            result = egg_expert.apply(obs, result, configuration)
            telemetry["bakery_market_turns"] += (
                list(result.get("market", []) or []) != before
            )

        telemetry["calls"] += 1
        telemetry["selected"][route] += 1
        states[seat] = {
            "route": route,
            "bakery_seen": bakery_seen[seat],
            "egg_entries": int(egg_expert.telemetry["entries"]),
            "egg_exit_units": int(egg_expert.telemetry["exit_units"]),
        }
        return result

    agent.children = children
    agent.egg_expert = egg_expert
    agent.states = states
    agent.telemetry = telemetry
    agent.router_config = config
    return agent
