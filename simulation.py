import random

from game import Game

class Simulation:

    def __init__(self, characters, strategy):
        self.game = Game(characters)
        self.strategy = strategy
        self.history = []
    

    @property
    def game_stage(self):
        return self.game.current_stage
    
  
    def simulate(self, verbose=False):
        self.history.append(self.game.characters)
        while not self.game.finished:
            self.game.move_to_next_stage()
            if self.game.shift == 'night':
                self._simulate_night_actions()
                self.game._update_scoreboard()
            else:
                self._simulate_day_actions()
                self.game._update_scoreboard()
        
        self.history.append(f'{self.game.winner} wins!')
        if verbose:
            for message in self.history:
                print(message)
        return self.game.winner


    def _pick_target(self, select='all', unrevealed=False):
        return random.choice(self.game.get_seats_of(select))


    def _werewolf_night_action(self):
        config = self.strategy.get('werewolf')
        if config is None:
            target = self._pick_target('not werewolf')
        else:
            select = config.get(
                self.game_stage, 'not werewolf')
            target = self._pick_target(select)
        
        role = self.game.characters[target]
        role.die(method='hunted')
        message = f"{self.game_stage}: Werewolves hunted #{target} {role}"
        self.history.append(message)
        return target

    
    def _witch_night_action(self, hunt_target):
        witch_seat = self.game.get_seats_of('witch', True)[0]
        witch = self.game.characters[witch_seat]

        config = self.strategy.get('witch')
        if config is None:
            pass
        else:
            used_antidote = False # antidote and poison cannot be used together
            if witch.alive:
                if witch.antidote:
                    antidote_config = config.get('antidote')
                    if antidote_config and antidote_config['round'] <= self.game.round:
                        candidates = antidote_config['target']
                        if hunt_target in self.game.get_seats_of(candidates, True):
                            hunted_role = self.game.characters[hunt_target]
                            hunted_role.revive()
                            witch.use_antidote()
                            used_antidote = True

                            message = f"{self.game_stage}: Witch saved #{hunt_target} {hunted_role}"
                            self.history.append(message)

            if (witch.alive or (hunt_target == witch_seat)) and (not used_antidote):
                if witch.poison:
                    poison_config = config.get('poison')
                    if poison_config and poison_config['round'] <= self.game.round:
                        candidates = poison_config.get('target', 'non witch')
                        target = self._pick_target(candidates)
                        poisoned_role = self.game.characters[target]
                        poisoned_role.die('poisoned')
                        witch.use_poison()

                        message = f"{self.game_stage}: Witch poisoned #{target} {poisoned_role}"
                        self.history.append(message)

    def _seer_night_action(self):
        config = self.strategy.get('witch')
        if config is None:
            pass
        else:
            pass
    
    def _simulate_night_actions(self):
        hunt_target = self._werewolf_night_action()
        self.game._update_scoreboard()
        self._witch_night_action(hunt_target)
        self.game._update_scoreboard()
        self._seer_night_action()
    
    def _simulate_day_actions(self):
        config = self.strategy.get('villagers')
        if config is None:
            target = self._pick_target('all')
        else:
            select = config.get(
                self.game_stage, 'all')
            target = self._pick_target(select)

        role = self.game.characters[target]
        role.die(method='banished')
        message = f"{self.game_stage}: Villagers banished #{target} {role}"
        self.history.append(message)
        return target
