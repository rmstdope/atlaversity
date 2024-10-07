from prompt_toolkit import  HTML

from SkillLevel import *
from Skill import *

class Mage:
    all_mages = []

    @staticmethod
    def find_by_id(mage_id):
        for m in Mage.all_mages:
            if m.id == int(mage_id):
                return m
        return None
    
    @staticmethod
    def find_num_by_id(mage_id) -> int:
        for i,m in enumerate(Mage.all_mages):
            if m.id == int(mage_id):
                return i
        return -1

    @staticmethod
    def read_from_file(faction, turn):
        file = 'mages' + str(faction).zfill(2) + str(turn).zfill(2) + '.csv'
        f = open(file, 'r')
        strs = f.read().splitlines()
        for i, mage in enumerate(strs[0].split(',')[1:]):
            d = mage.split(' ', 1)
            m = Mage(int(d[0]), d[1])
            for skill in strs[1:]:
                d = skill.split(',')
                if int(d[i + 1]) > 0 and d[0] != 'COMB' and d[0] != 'OBSE':
                    s = SkillLevel(d[0], int(d[i + 1]))
                    m.add_skill(s)
            Mage.all_mages.append(m)

    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.skill_levels = []
        self.long_name = f'{name} ({self.id})'
        self.comment = ''

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

    def get_skill_list(self):
        s = '    '
        for i, skill in enumerate(self.skill_levels):
            if i % 8 == 0 and i != 0:
                s += '\n    '
            elif i != 0:
                s += ', '
            s += f'{skill}'
        return s
            
    def get_skill_delta(self, m2, skill2):
        s = '    '
        all_skills = list(set(x.name for x in self.skill_levels) | set(x.name for x in m2.skill_levels))
        all_skills.sort()
        for i, skill in enumerate(all_skills):
            if skill2 == None:
                if i % 8 == 0 and i != 0:
                    s += '\n    '
                elif i != 0:
                    s += ', '
            if skill2 == None or skill2.name == skill:
                s += f'{skill} {self.get_skill_level_and_days(skill)}'
                if self.get_skill_days(skill) != m2.get_skill_days(skill):
                    s += f'<ansigreen>->{m2.get_skill_level_and_days(skill)}</ansigreen>'
        return HTML(s)
            
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
    
    def get_skill_level_and_days(self, name):
        for s in self.skill_levels:
            if s.name == name:
                return str(s.level) + '(' + str(s.days) + ')'
        return '0(0)'
    
    def has_skill(self, name):
        for s in self.skill_levels:
            if s.name == name:
                return True
        return False

    def can_study(self, skill):
        if isinstance(skill, str):
            skill = Skill.string_to_skill(skill)
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
            self.skill_levels.append(SkillLevel(skill.name, days))
            
    def can_teach(self, student, skill):
        return self.get_skill_level(skill) > student.get_skill_level(skill)
