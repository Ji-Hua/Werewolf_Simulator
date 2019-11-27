import numpy as np
import copy

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
        return 0, random_select(first_group)
    else:
        return 1, random_select(second_group)