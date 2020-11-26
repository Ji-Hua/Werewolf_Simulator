import random

from characters import CharacterFactory


class Game:

    def __init__(self, characters):
        self.winner = None
        self.round = 0
        self.shift = 'day'
        self._prepare_characters(characters)
        self._update_scoreboard()
        self._update_suspect_scores()

    def _prepare_characters(self, characters):
        self.characters = {}
        self.original_seats = {}

        factory = CharacterFactory()
        queue = []
        for name, num in characters.items():
            for _ in range(num):
                character = factory.construct(name)
                queue.append(character)
        random.shuffle(queue)

        for i, c in enumerate(queue):
            seat = i + 1
            self.characters[seat] = c
            seats = self.original_seats.get(c.name, [])
            seats.append(seat)
            self.original_seats[c.name] = seats

    def _update_scoreboard(self):
        scoreboard = {'werewolf': 0, 'god': 0, 'villager': 0}
        survivals = {}
        for seat, role in self.characters.items():
            if role.alive:
                scoreboard[role.camp] += 1
                seats = survivals.get(role.name, [])
                seats.append(seat)
                survivals[role.name] = seats
        self.scoreboard = scoreboard
        self.survivals = survivals
    
    def _update_suspect_scores(self):
        suspect_scores = {}
        total_werewolves = len(self.original_seats['werewolf'])
        unknown_werewolves = total_werewolves
        unknown_players = len(self.characters)
        for seat, role in self.characters.items():
            if role.revealed:
                unknown_players -= 1
                if role.name == 'werewolf':
                    unknown_werewolves -= 1
        score = float(unknown_werewolves) / float(unknown_players)
        for seat, role in self.characters.items():
            if role.revealed:
                if role.name == 'werewolf':
                    role.suspect = 1.0
                else:
                    role.suspect = 0.0
            else:
                role.suspect = score
            suspect_scores[seat] = role.suspect
        self.suspect_scores = suspect_scores

    def _check_game_ends(self):
        self._update_scoreboard()
        if self.scoreboard['villager'] == 0 or self.scoreboard['god'] == 0:
            self.winner = 'werewolf'
        elif self.scoreboard['werewolf'] == 0:
            self.winner = 'villager'
    
    def move_to_next_stage(self):
        if self.finished:
            raise Exception('Game is finished')
        
        if self.shift == 'day':
            self.shift = 'night'
            self.round += 1
        else:
            self.shift = 'day'
    
    def find_most_suspectful(self, targets=None, only_unknown=False):
        self._update_suspect_scores()
        if targets:
            if only_unknown:
                unknown = self._find_unknown()
                candidates = [t for t in targets if t in unknown]
            else:
                candidates = targets
        else:
            if only_unknown:
                candidates = self._find_unknown()
            else:
                candidates = []
                for v in self.survivals.values():
                    candidates.extend(v)

        scores = [self.suspect_scores[c] for c in candidates]
        max_score = max(scores)
        return [c for c in candidates if self.suspect_scores[c] == max_score]

    def _find_unknown(self):
        seats = []
        for seat, role in self.characters.items():
            if role.alive:
                if not role.revealed:
                    seats.append(seat)
        return seats

    def get_seats_of(self, targets='all', dead_included=False):
        ''' Targets could be 'all', 'not werwolf', 'werewolf', 'villager'
        'gods', 'not gods', 'not villager', 'seer', 'not seer', 'witch'
        'not witch', 'moron', 'not moron', 'hunter', 'not hunter'
        '''
        self._update_scoreboard()
        inclusives = ['seer', 'witch', 'hunter', 'moron',
         'villager', 'werewolf']
        exclusives = ['not seer', 'not witch', 'not hunter',
         'not moron', 'not villager', 'not werewolf']
        
        if dead_included:
            survivals = self.original_seats # for witch antidote
        else:
            survivals = self.survivals
        if targets in inclusives:
            return survivals[targets]
        elif targets in exclusives:
            name = targets[4:]
            results = []
            for k, v in survivals.items():
                if k != name:
                    results.extend(v)
            return results
        elif targets == 'all':
            results = []
            for _, v in survivals.items():
                results.extend(v)
            return results
        elif targets == 'gods':
            return [
                *survivals['seer'],
                *survivals['moron'],
                *survivals['hunter'],
                *survivals['witch']
            ]
        elif targets == 'not gods':
            return [*survivals['villager'], *survivals['werewolf']]
        else:
            raise ValueError(f'{targets} is invalid')

    @property
    def current_stage(self):
        return f"{self.shift} {self.round}"

    @property
    def finished(self):
        self._check_game_ends()
        return not (self.winner is None)

