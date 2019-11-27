class player:

    def __init__(self, skill_level):
        if 0 <= skill_level <= 10:
            self.skill_level = skill_level
        else:
            raise ValueError('Invalid skill level')
        self.character = None
    
    # def __str__(self):
    #     if self.death：
    #         state = 'dead'
    #     else:
    #         state = 'alive'
    #     msg = f'Player {name} {state}\n' 
    #     msg += f'Speech {self.speech} Detect {self.detect} Logic {logic}'
    #     if self.character:
    #         msg += f'Identity: {self.character.Identity}'
    #     return msg

    def get_character(self, character):
        self.character = character

    def game_start(self, players):
        if not self.character:
            raise AttributeError('No character assigned')
        self.death = False
        self.reference_table = 

    
    @property
    def camp(self):
        if self.character:
            return self.character.camp
    
    @property
    def identity(self):
        if self.character:
            return self.character.identity
    
    @property
    def follow(self):
        # use fixed number now
        p_follow = 0.95
        return p_follow