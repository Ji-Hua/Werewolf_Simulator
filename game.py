from .tools import *

WOLF_TAG = 'wolf'
VILLAGER_TAG = 'villager'
GOD_TAG = 'god'

BAD_CAMP = 'bad'
GOOD_CAMP = 'good'

def random_select(iterable):
    return np.random.choice(list(iterable))

def sample_from_two_groups(p_first, first_group, second_group):
    is_first = np.random.binomial(1, p_first, 1)
    if is_first:
        return random_select(first_group)
    else:
        return random_select(second_group)

class Game:
    
    
    def __init__(self, players, badge=False):
        if len(players) != 12:
            raise Exception('Wrong player number')
        self.players = players
        self.badge = badge
        self.sheriff = None
        self.wolves = set()
        self.gods = set()
        self.villagers = set()
        for i, p in players.items():
            if p.identity == WOLF_TAG:
                self.wolves.add(i)
            elif p.identity == GOD_TAG:
                self.gods.add(i)
            elif p.identity == VILLAGER_TAG:
                self.villagers.add(i)
            else:
                raise Exception(f'Invalid identity: {p.identity}')
        self.good_camp = self.gods.union(self.villagers)
        self.history = []
        self.round = 1
        self.night = True
        self.in_game = False
        self.winner = None

       
    def _check_game_end(self):
        if len(self.gods) == 0:
            self.winner = WOLF_TAG
        elif len(self.villagers) == 0:
            self.winner = WOLF_TAG
        elif len(self.wolves) == 0:
            self.winner = VILLAGER_TAG
        else:
            self.winner = None
        self.in_game = False
    
    def _switch_day_night(self):
        # toggle night/day
        self.night = not self.night
    
    def pass_badge(self):
        # p_good = self.players[self.sheriff].skill_level
        p_good = 1  # assume badge is always passed to a good guy
        return sample_from_two_groups(p_good, self.good_camp, self.wolves)

    def death_check(self, player_id):
        # TODO: add hunter / moron later
        # now check sheriff
        if player_id == self.sheriff:
            self.sheriff = self.pass_badge()
    
    def _get_wolf_prob_recoginze_god(self):
        p_god = 0.5
        # Assume that during the night communication
        # the best player will help the others find god
        # so the probability of finding a god should be
        # as high as the best player's skill level
        for i in self.wolves:
            if self.players[i].skill_level > p_god:
                p_god = self.players[i].skill_level
        return p_god
    
    def hunt(self):
        p_god = self._get_wolf_prob_recoginze_god()
        target = sample_from_two_groups(p_god, self.gods, self.villagers)
        return target
    
    def sheriff_elect(self, only_good=True):
        # TODO: add sheriff candidates
        if only_good:
            all_candidates = self.good_camp
        else:
            all_candidates = self.good_camp.union(self.wolves)
        return random_select(all_candidates)
    
    def sheriff_banish_vote(self):
        p_good = self.players[self.sheriff].skill_level
        target = sample_from_two_groups(p_good, self.good_camp, self.wolves)
        self.ballots[target] += 1.5  # badge advantage
        return target
    
    def good_vote(self, player_id, sheriff_vote_target=None):
        player = self.players[player_id]
        p_detect = player.skill_level
        other = sample_from_two_groups(p_detect, self.wolves, (self.good_camp - player_id))
        if sheriff_vote_target:
            # if the player is selected to be banished by sheriff, then reject to follow
            if sheriff_vote_target == player_id:
                vote = other
            else:
                p_follow = player.follow()
                vote = sample_from_two_groups(p_follow, [sheriff_vote_target], [other])
        else:
            vote = other
        self.ballots[vote] += 1
    
    def wolf_vote(self, player_id, sheriff_vote_target=None):
        # A wolf vote follows the following logic:
        # 1. sheriff is wolf, vote with him
        # 2.1 sheriff is a villager, target is wolf, follow sheriff with
        # a low possibility
        # 2.2 sheriff is villager, target is a good guy, follow sheriff with a
        # high possibility
        # 2.3 (special) if wolf camp has an arrangement the night before, follow it

        player = self.players[player_id]
        if self.sheriff in self.wolves:
            # ignore logic 1 for now
            pass
        else:
            # should have chance to vote his teammates?
            other = random_select(self.good_camp)
            if sheriff_vote_target in self.wolves:
                p_follow = 1 - player.skill_level
                vote = sample_from_two_groups(p_follow, [sheriff_vote_target], [other])
            else:
                p_follow = player.follow()
                vote = sample_from_two_groups(p_follow, [sheriff_vote_target], [other])
            self.ballots[vote] += 1

    
    def banish_vote(self):
        # TODO: make this simulate reality better
        self.ballots = {i: 0 for i, p in self.players if not p.death}
        sheriff_vote_target = self.sheriff_banish_vote()
        for i, p in self.players:
            if i in self.good_camp:
                self.good_vote(i, sheriff_vote_target)
            else:
                self.wolf_vote(i, sheriff_vote_target)
        # count result
        maxium_vote = max(self.ballots.values())
        result = random_select([k for k, v in self.ballots.items() if v == maxium_vote])
        return result

    
    def night_action(self):
        # TODO: add god skill later to extend
        night_death = []
        hunt_victim = self.hunt()
        night_death.append(hunt_victim)
        self._update_death(night_death)
    
    def day_action(self):
        if self.badge and (not self.sheriff):
            self.sheriff_elect()
        self.banished = self.banish_vote()
        

    
    def _update_death(self, victims):
        for v in victims:
            self.death_check(v)
            if v in self.wolves:
                self.wolves.discard(v)
            elif v in self.villagers:
                self.villagers.discard(v)
                self.good_camp.discard(v)
            else:
                self.gods.discard(v)
                self.good_camp.discard(v)
            self.players[v].death = True


    def start(self):
        self.in_game = True
        while self.in_game:
            pass
    