from simulation import Simulation


strategy_dict = {
    'witch': {
        'antidote': {'round': 1, 'target': 'all'},
        'poison': {'round': 2, 'target': 'werewolf'}
    }
}
characters = {
    'Seer': 1,
    'Witch': 1,
    'Hunter': 1,
    'Moron': 1,
    'Werewolf': 4,
    'Villager': 4
}

iter_num = 1000
sim_results = {'werewolf': 0, 'villager': 0}
verbose = False

for _ in range(iter_num):
    simulation = Simulation(characters, strategy_dict)
    winner = simulation.simulate(verbose)
    sim_results[winner] += 1

print(strategy_dict)
print(sim_results)