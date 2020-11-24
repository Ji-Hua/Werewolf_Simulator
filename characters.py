from abc import ABC
import traceback


class Character(ABC):
    
    def __init__(self):
        self.death = False
        self.revealed = False
        self.suspect = 0.0
    
    def die(self, method=None):
        self.death = True
    
    def revive(self):
        self.death = False
    
    def death_action(self):
        pass
    
    @property
    def alive(self):
        return not self.death
    
    def __repr__(self):
        return self.name


class CharacterTypes:
    class Seer(Character):
        
        def __init__(self):
            super().__init__()
            self.name = 'seer'
            self.camp = 'god'

    class Witch(Character):
        
        def __init__(self):
            super().__init__()
            self.name = 'witch'
            self.camp = 'god'
            self.poison = True
            self.antidote = True
        
        def use_antidote(self):
            self.antidote = False
        
        def use_poison(self):
            self.poison = False

    class Moron(Character):

        def __init__(self):
            super().__init__()
            self.name = 'moron'
            self.camp = 'god'
            self.revealed = False
        
        def die(self, method):
            if method == 'banished':
                self.revealed = True
            self.death = True
        
    class Hunter(Character):

        def __init__(self):
            super().__init__()
            self.name = 'hunter'
            self.camp = 'god'
            self.shotgun = True

        def die(self, method):
            if method == 'poisoned':
                self.shotgun = False
            else:
                self.revealed = True
            self.death = True

    class Villager(Character):
        def __init__(self):
            super().__init__()
            self.name = 'villager'
            self.camp = 'villager'

    class Werewolf(Character):
        def __init__(self):
            super().__init__()
            self.name = 'werewolf'
            self.camp = 'werewolf'


class CharacterFactory:

    def construct(self, builder_name):
        setattr(self, builder_name, CharacterTypes())
        try:
            target_class = getattr(CharacterTypes, builder_name)
            instance = target_class()
            return instance
        except AttributeError:
            print("Builder {} not defined.".format(builder_name))
            traceback.print_stack()
