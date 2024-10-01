from SkillLevel import SkillLevel

class Mage:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.skill_levels = []

    def __str__(self):
        s = f'{self.name} ({self.id})\n'
        s += '    '
        for i, skill in enumerate(self.skill_levels):
            if i % 8 == 0 and i != 0:
                s += '\n    '
            elif i != 0:
                s += ', '
            s += f'{skill}'
        return s
    
    def add_skill(self, s):
        self.skill_levels.append(s)

    def has_skill_level(self, name, level):
        for s in self.skill_levels:
            if s.name == name and s.level >= level:
                return True
        return False

    def get_skill_level(self, name):
        for s in self.skill_levels:
            if s.name == name:
                return s.level
        return 0
    
    def get_skill_days(self, name):
        for s in self.skill_levels:
            if s.name == name:
                return s.days
        return 0
    
    def has_skill(self, name):
        for s in self.skill_levels:
            if s.name == name:
                return True
        return False

    def can_study(self, skill):
        can = True
        if self.has_skill(skill.name) and self.get_skill_level(skill.name) == 5:
            return False
        for d in skill.dependencies:
            m = False
            need_level = d['level']
            if self.has_skill(skill.name):
                need_level = max(need_level, self.get_skill_level(skill.name) + 1)	
            if not self.has_skill_level(d['skill'].name, need_level):
                can = False
        return can

    def train(self, skill, days):
        trained = False
        for s in self.skill_levels:
            if s.name == skill.name:
                s.train(days)
        if not trained:
            self.skill_levels.append(SkillLevel(skill.name, 60))