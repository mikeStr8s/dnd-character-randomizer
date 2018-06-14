class Character:
    def __init__(self, name):
        self.ability_bonuses = {'str': 0, 'dex': 0, 'con': 0, 'int': 0, 'wis': 0, 'cha': 0}
        self.name = name
        self.racename = ''
        self.subracename = ''
        self.classname = ''
        self.hit_die = ''
        self.skills = []
        self.proficiencies = []
        self.saving_throws = []
        self.speed = 0
        self.size = ''
        self.languages = []
        self.traits = []
        self.equipment = []

    def add_bonus(self, abilities: dict):
        assert isinstance(abilities, dict), 'You must provide a list'
        for x in abilities:
            if x in self.ability_bonuses.keys():
                self.ability_bonuses[x] += abilities[x]
