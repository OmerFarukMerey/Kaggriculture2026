"""Build v50's original market policy with our proven v46 farming guide.

    py -3.12 tools/build_v50.py --extract
    py -3.12 tools/build_v50.py --bundle

The default bundle retains v46's reactive farming and working-stock intent,
not its executable trade queue. --profiles, --augment, and --plans reproduce
the rejected recorded-plan experiments; they are not deployment defaults.
"""
import argparse
import ast
import base64
from concurrent.futures import ProcessPoolExecutor
import hashlib
from importlib.metadata import distribution
import json
from pathlib import Path
import sys
import zlib

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'agents'))
DEST = ROOT / 'agents' / 'v50'
SOURCE = ROOT / 'submissions' / 'v48-2965-mirrorgate' / 'main.py'


def route_data():
    source = SOURCE.read_text(encoding='utf-8')
    tree = ast.parse(source)
    node = next(n for n in tree.body if isinstance(n, ast.Assign)
                and any(isinstance(t, ast.Name) and t.id == '_R108_DATA' for t in n.targets))
    encoded = max((n.value for n in ast.walk(node.value)
                   if isinstance(n, ast.Constant) and isinstance(n.value, str)), key=len)
    return json.loads(zlib.decompress(base64.b85decode(encoded)))


def extract():
    DEST.mkdir(parents=True, exist_ok=True)
    path = distribution('kaggle-environments').locate_file(
        'kaggle_environments/envs/kaggriculture/kaggriculture.py')
    source = path.read_text(encoding='utf-8')
    tree = ast.parse(source)
    nodes = {}
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
            nodes[node.name] = node
        elif isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    nodes[target.id] = node
    wanted = {'_apply_unit_action', '_parse_order', '_commit_unit', '_do_hire',
              '_do_buy_land', 'market_price', 'MARKET_PARAMS', 'SHOPS', 'get',
              '_new_farm', '_new_private', '_new_market', '_daily_refresh_plants',
              '_daily_refresh_animals', '_decay_plants', '_drop_inventories_to_shed'}
    pending = list(wanted)
    while pending:
        node = nodes[pending.pop()]
        for child in ast.walk(node):
            if isinstance(child, ast.Name) and isinstance(child.ctx, ast.Load):
                if child.id in nodes and child.id not in wanted:
                    wanted.add(child.id)
                    pending.append(child.id)
    selected = {id(nodes[name]) for name in wanted}
    pieces = [ast.get_source_segment(source, node) for node in tree.body if id(node) in selected]
    header = ('# Deterministic physics from Kaggle kaggle-environments 1.32.7.\n'
              '# Apache-2.0; mechanically extracted by tools/build_v50.py.\n'
              '# No environment RNG, filesystem, networking, or opponent-private access.\n'
              'import math\n\n')
    (DEST / '_engine.py').write_text(header + '\n\n'.join(pieces) + '\n', encoding='utf-8')
    print(json.dumps({'engine_sha256': hashlib.sha256(source.encode()).hexdigest(),
                      'source_sha256': hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
                      'rules': str(DEST / '_engine.py'), 'symbols': len(wanted)}), flush=True)


def profile_route(route_id):
    # A real engine rollout is used to measure physical yield, not copied SELL orders.
    from kaggle_environments import make
    from v50.mechanics import project_units, execute_market
    data = route_data()
    route = [data['actions'][i] for i in data['routes'][str(route_id)]]
    profile = {'yield': [{} for _ in range(30)], 'inputs': [{} for _ in range(30)],
               'fixed': [0.0] * 30}
    env = make('kaggriculture', configuration={'episodeSteps': 720, 'seed': 632149,
                                              'weedSpawnChance': 0.0}, debug=False)
    failures = []

    def actor(obs, configuration):
        step = int(obs['step'])
        action = route[step]
        flows = {'yield': {}, 'inputs': {}}
        farm, private = project_units(obs, action, configuration, flows=flows)
        day = step // 24
        for category in ('yield', 'inputs'):
            for item, quantity in flows[category].items():
                out = profile[category][day]
                out[item] = out.get(item, 0) + quantity
        result = execute_market(action.get('market', []), [], farm, private,
                                obs['market']['inventory'], obs['market'].get('params'),
                                configuration)
        profile['fixed'][day] += result['fixed_spend']
        return action

    env.run([actor, 'pass'])
    for logs in env.logs:
        for entry in logs:
            if 'Traceback (most recent call last)' in entry.get('stderr', ''):
                failures.append(entry['stderr'])
    if len(env.steps) != 720 or failures or any(s.status != 'DONE' for s in env.steps[-1]):
        raise RuntimeError(f'Route profile {route_id} failed: {failures}')
    profile['reference_reward'] = env.steps[-1][0].reward
    return route_id, profile


def profiles(workers):
    data = route_data()
    ids = [int(k) for k in data['routes']]
    measured = {}
    with ProcessPoolExecutor(max_workers=workers, max_tasks_per_child=1) as pool:
        for route_id, profile in pool.map(profile_route, ids):
            measured[route_id] = profile
            print(f'Profile {len(measured)}/{len(ids)} route={route_id} '
                  f'reference_reward={profile["reference_reward"]}', flush=True)
    payload = {'actions': data['actions'], 'routes': data['routes'], 'profiles': measured}
    encoded = base64.b85encode(zlib.compress(json.dumps(payload, separators=(',', ':')).encode(), 9)).decode()
    code = ('# Physical plans from the user\'s v48; upstream Apache-2.0 notices in bundled main.py.\n'
            '# Profiles: real 1.32.7 engine, no weeds, seed632149, passive opponent.\n'
            '# These are production forecasts, not evidence of competitive strength.\n'
            'import base64\nimport json\nimport zlib\n\n'
            f'_DATA = json.loads(zlib.decompress(base64.b85decode({encoded!r})))\n'
            'ROUTES = {int(k): [_DATA["actions"][i] for i in ids] for k, ids in _DATA["routes"].items()}\n'
            'PROFILES = {int(k): v for k, v in _DATA["profiles"].items()}\n'
            'del _DATA\n')
    (DEST / 'data.py').write_text(code, encoding='utf-8')
    (ROOT / 'analysis' / 'v50_route_profiles.json').write_text(json.dumps(measured, indent=2), encoding='utf-8')
    print('PROFILE DATA COMPLETE', flush=True)


def capture_incumbent(job):
    """Measure complete physical schedules, including the incumbents' unit repairs."""
    import importlib
    from copy import deepcopy
    from kaggle_environments import make
    from v50.mechanics import project_units
    route_id, source_ref, seed, forced_route = job
    source = ROOT / source_ref
    namespace = {}
    exec(compile(source.read_text(encoding='utf-8'), str(source), 'exec'), namespace)
    actor = [value for value in namespace.values() if callable(value)][-1]
    if forced_route is not None:
        chassis = namespace['_IMPL'].chassis
        if forced_route not in chassis.routes:
            raise ValueError(f'Unknown physical route {forced_route}')
        chassis.router = lambda observation, step, state: forced_route
    route = []
    profile = {'yield': [{} for _ in range(30)], 'inputs': [{} for _ in range(30)],
               'fixed': [0.0] * 30, 'source': source_ref, 'training_seed': seed,
               'forced_route': forced_route,
               'source_sha256': hashlib.sha256(source.read_bytes()).hexdigest()}
    engine = importlib.import_module('kaggle_environments.envs.kaggriculture.kaggriculture')
    saved = (engine._process_market, engine._commit_unit, engine._do_hire, engine._do_buy_land)
    market_context = {}

    def process_market(state, env):
        market_context['farm'] = state[0].observation.farms[0]
        market_context['day'] = int(state[0].observation.step) // 24
        return saved[0](state, env)

    def commit(op, item, quote, farm, private, market, shed_capacity=100):
        ok = saved[1](op, item, quote, farm, private, market, shed_capacity)
        if ok and farm is market_context['farm'] and op in ('BUY_SEED', 'BUY_ANIMAL'):
            profile['fixed'][market_context['day']] += quote
        return ok

    def hire(farm, private, board, mult=1):
        before = farm['money']
        result = saved[2](farm, private, board, mult)
        if farm is market_context['farm']:
            profile['fixed'][market_context['day']] += before - farm['money']
        return result

    def land(farm, board):
        before = farm['money']
        result = saved[3](farm, board)
        if farm is market_context['farm']:
            profile['fixed'][market_context['day']] += before - farm['money']
        return result

    def measured_actor(obs, configuration):
        action = actor(obs, configuration)
        if not isinstance(action, dict):
            raise TypeError('Incumbent returned a non-action')
        route.append(deepcopy(action))
        flows = {'yield': {}, 'inputs': {}}
        project_units(obs, action, configuration, flows=flows)
        for category in ('yield', 'inputs'):
            bucket = profile[category][int(obs.step) // 24]
            for item, quantity in flows[category].items():
                bucket[item] = bucket.get(item, 0) + quantity
        return action

    env = make('kaggriculture', configuration={'episodeSteps': 720, 'seed': seed,
                                              'weedSpawnChance': 0.0}, debug=False)
    engine._process_market, engine._commit_unit, engine._do_hire, engine._do_buy_land = (
        process_market, commit, hire, land)
    try:
        env.run([measured_actor, str(source)])
    finally:
        engine._process_market, engine._commit_unit, engine._do_hire, engine._do_buy_land = saved
    errors = [entry['stderr'] for logs in env.logs for entry in logs
              if 'Traceback (most recent call last)' in entry.get('stderr', '')]
    if len(route) != 719 or len(env.steps) != 720 or errors:
        raise RuntimeError(f'Incumbent schedule {route_id} failed: {errors}')
    profile['reference_reward'] = env.steps[-1][0].reward
    return route_id, route, profile


def augment(workers):
    # These seeds are training environments, never runtime routing keys.
    seeds = (1381090153, 85879428, 830977, 5000, 632149, 7013)
    sources = ('submissions/v48-2965-mirrorgate/main.py', 'submissions/v46-platform/main.py')
    jobs = [(200 + i * len(seeds) + j, source, seed, None)
            for i, source in enumerate(sources) for j, seed in enumerate(seeds)]
    route_ids = sorted(int(rid) for rid in route_data()['routes'])
    jobs.extend((1000 + i * len(route_ids) + j, sources[0], seed, rid)
                for i, seed in enumerate(seeds) for j, rid in enumerate(route_ids))
    routes, measured = {}, {}
    with ProcessPoolExecutor(max_workers=workers, max_tasks_per_child=1) as pool:
        for route_id, route, profile in pool.map(capture_incumbent, jobs):
            routes[route_id], measured[route_id] = route, profile
            print(f'Captured route={route_id} source={profile["source"]} '
                  f'reference_reward={profile["reference_reward"]}', flush=True)
    actions, indexed, keys = [], {}, {}
    for route_id, route in sorted(routes.items()):
        ids = []
        for action in route:
            key = json.dumps(action, sort_keys=True, separators=(',', ':'))
            if key not in keys:
                keys[key] = len(actions)
                actions.append(action)
            ids.append(keys[key])
        indexed[route_id] = ids
    payload = {'actions': actions, 'routes': indexed, 'profiles': measured}
    encoded = base64.b85encode(zlib.compress(json.dumps(payload, separators=(',', ':')).encode(), 9)).decode()
    code = ("# Route data and measured physical schedules from the user's v48/v46.\n"
            '# No controller code or runtime seed lookup is included.\n'
            '# Measurements are forecasts, not competitive validation.\n'
            'import base64\nimport json\nimport zlib\n\n'
            f'_DATA = json.loads(zlib.decompress(base64.b85decode({encoded!r})))\n'
            'ROUTES = {int(k): [_DATA["actions"][i] for i in ids] for k, ids in _DATA["routes"].items()}\n'
            'PROFILES = {int(k): v for k, v in _DATA["profiles"].items()}\n'
            'del _DATA\n')
    (DEST / 'data.py').write_text(code, encoding='utf-8')
    (ROOT / 'analysis' / 'v50_route_profiles.json').write_text(json.dumps(measured, indent=2), encoding='utf-8')
    print(f'AUGMENTED DATA COMPLETE: {len(routes)} physical plans', flush=True)


def market_core(source):
    """Exclude the rejected route-planning policy from the guided deployment."""
    tree = ast.parse(source)
    controller = next(node for node in tree.body
                      if isinstance(node, ast.ClassDef) and node.name == 'MarketController')
    removed = {'_route_analysis', '_future_pickups', '_reserves', '_useful_fixed_quantity', 'act'}
    assert removed <= {node.name for node in controller.body if isinstance(node, ast.FunctionDef)}
    controller.body = [node for node in controller.body
                       if not (isinstance(node, ast.FunctionDef) and node.name in removed)]
    initializer = next(node for node in controller.body
                       if isinstance(node, ast.FunctionDef) and node.name == '__init__')
    initializer.body = [node for node in initializer.body
                        if not (isinstance(node, ast.AnnAssign)
                                and isinstance(node.target, ast.Attribute)
                                and node.target.attr == '_route_cache')]
    tree.body = [node for node in tree.body
                 if not (isinstance(node, ast.FunctionDef) and node.name in {'_step', '_commands'})
                 and not (isinstance(node, ast.Assign) and any(
                     isinstance(target, ast.Name) and target.id in {'_ANIMALS', '_PRODUCTION_CUTOFF'}
                     for target in node.targets))]
    needed = {node.id for node in ast.walk(tree) if isinstance(node, ast.Name)}
    for node in tree.body:
        if isinstance(node, ast.ImportFrom) and node.module != '__future__':
            node.names = [alias for alias in node.names if (alias.asname or alias.name) in needed]
    tree.body = [node for node in tree.body if not isinstance(node, ast.ImportFrom) or node.names]
    return ast.unparse(tree) + '\n'


def bundle(output, guide='submissions/v46-platform/main.py'):
    names = ('_engine', 'mechanics', 'market', 'guided') if guide else (
        '_engine', 'mechanics', 'data', 'production', 'market')
    modules = {name: (DEST / f'{name}.py').read_text(encoding='utf-8') for name in names}
    if guide:
        modules['market'] = market_core(modules['market'])
        modules['native'] = (ROOT / guide).read_text(encoding='utf-8')
    source = SOURCE.read_text(encoding='utf-8')
    first = ast.parse(source).body[0].lineno
    upstream = '\n'.join(source.splitlines()[:first - 1])
    payload = base64.b85encode(zlib.compress(json.dumps(modules).encode(), 9)).decode()
    code = '''# v50: original inventory/cash market control with reused farming expertise.
# Copyright 2026 Omer Faruk Merey. Apache-2.0.
# Reused components and exact module fingerprints are recorded in build.json.
# Rules adapted from Kaggle kaggle-environments 1.32.7 (Apache-2.0).
# Source modules: agents/v50/. Reproducible builder: tools/build_v50.py.
'''
    code += '# Historical upstream notices below describe their source, not this controller.\n'
    code += upstream + '\n\nimport base64 as _base64\nimport json as _json\nimport zlib as _zlib\n'
    code += 'import sys as _sys\nimport types as _types\n\n'
    code += f'_sources = _json.loads(_zlib.decompress(_base64.b85decode({payload!r})))\n'
    code += '''_package_name = "_v50_" + str(id(globals()))
_package = _types.ModuleType(_package_name)
_package.__path__ = []
_sys.modules[_package_name] = _package
for _name, _source in _sources.items():
    _module = _types.ModuleType(_package_name + "." + _name)
    _module.__package__ = _package_name
    _module.__file__ = "<v50/" + _name + ".py>"
    _sys.modules[_module.__name__] = _module
    setattr(_package, _name, _module)
    exec(compile(_source, _module.__file__, "exec"), _module.__dict__)
del _sources, _source
_controllers = {}
'''
    if guide:
        code += '''_guide = [value for value in _package.native.__dict__.values() if callable(value)][-1]


def v50_agent(observation, configuration=None):
    seat, step = int(observation["player"]), int(observation["step"])
    state = _controllers.get(seat)
    if state is None or step <= state[0]:
        state = [-1, _package.guided.GuidedMarketController()]
        _controllers[seat] = state
    action = _guide(observation, configuration)
    action = state[1].act(observation, configuration, action)
    state[0] = step
    return action
'''
    else:
        code += '''

def v50_agent(observation, configuration=None):
    seat, step = int(observation["player"]), int(observation["step"])
    state = _controllers.get(seat)
    if state is None or step <= state[0]:
        state = [-1, _package.production.ProductionController(_package.data.ROUTES, _package.data.PROFILES),
                 _package.market.MarketController()]
        _controllers[seat] = state
    action, future = state[1].act(observation, configuration)
    action = state[2].act(observation, configuration, action, future)
    state[0] = step
    return action
'''
    target = ROOT / output
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(code, encoding='utf-8')
    metadata = {'source': str(target.relative_to(ROOT)),
                'sha256': hashlib.sha256(target.read_bytes()).hexdigest(),
                'module_sha256': {name: hashlib.sha256(text.encode()).hexdigest() for name, text in modules.items()},
                'guide': guide,
                'reused': [guide or 'v48/v46 measured physical schedules',
                           'kaggle-environments 1.32.7 deterministic rules']}
    target.with_name('build.json').write_text(json.dumps(metadata, indent=2), encoding='utf-8')
    print(json.dumps(metadata, indent=2), flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--extract', action='store_true')
    parser.add_argument('--profiles', action='store_true')
    parser.add_argument('--augment', action='store_true')
    parser.add_argument('--bundle', action='store_true')
    parser.add_argument('--guide', default='submissions/v46-platform/main.py',
                        help='Reactive farming and stock-intent source')
    parser.add_argument('--plans', action='store_true', help='Build the rejected recorded-plan experiment')
    parser.add_argument('--workers', type=int, default=8)
    parser.add_argument('--output', default='submissions/v50-adaptive-economy/main.py')
    args = parser.parse_args()
    if args.extract:
        extract()
    if args.profiles:
        profiles(args.workers)
    if args.augment:
        augment(args.workers)
    if args.bundle:
        bundle(args.output, None if args.plans else args.guide)
    if not (args.extract or args.profiles or args.augment or args.bundle):
        parser.error('choose --extract, --profiles, --augment, or --bundle')


if __name__ == '__main__':
    main()
