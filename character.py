import numpy as np
import copy
from .tools import *

class Character:


    def __init__(self, identity, group, camp):
        self.identity = identity
        self.group = group
        self.camp = camp
    
    def __str__(self):
        msg = f"Identity: {self.identity} Group: {self.group}"
        return msg
    
    def night_action(self):
        pass

class Werewolf(Character):


    def __init__(self):
        self.identity = WOLF_TAG
        self.group = WOLF_TAG
        self.camp = BAD_CAMP
    
    def night_action(self, players, p_god):
        is_god = np.random.binomial(1, p_god, 1)
        if is_god:
            return random_select(gods), god_label
        else:
            return random_select(villagers), villager_label


class DummyGod(Character):


    def __init__(self):
        self.identity = GOD_TAG
        self.group = GOD_TAG
        self.camp = GOOD_CAMP


class Villager(Character):


    def __init__(self):
        self.identity = VILLAGER_TAG
        self.group = VILLAGER_TAG
        self.camp = GOOD_CAMP