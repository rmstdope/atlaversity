from copy import deepcopy
from messages import ok, warning, error
from Skill import Skill

class Turn:
    def __init__(self, mages, data, num):
        self.study = data.split(',')
        self.start_mages = mages
        self.num = num
        self.end_mages = [deepcopy(m) for m in self.start_mages]
        self.teacher = -1
        self.taught = []
        self.not_taught = []
        self.find_teacher()
        self.check_study_prerequisites()
        self.check_teaching()
        self.run_turn()

    def check_teaching(self):
        if self.teacher >= 0:
            for j, m in enumerate(self.start_mages):
                if j != self.teacher and m.get_skill_level(self.study[j]) < self.start_mages[self.teacher].get_skill_level(self.study[j]):
                    self.taught.append(m)
                elif j != self.teacher:
                    #warning(f'{m.id} - {self.start_mages[self.teacher].id} / {m.get_skill_level(self.study[j])} - {self.start_mages[self.teacher].get_skill_level(self.study[j])}')
                    self.not_taught.append(j)
            if len(self.taught) < len(self.start_mages) - 1:
                warning(f'Warning: Only {len(self.taught)} out of {len(self.start_mages) - 1} can be taught in turn {self.num}.')
                for n in self.not_taught:
                    warning(f' ->{self.start_mages[n].name} ({self.start_mages[n].id}) cannot be taught {self.study[n]}')
            if len(self.taught) > 10:
                warning(f'Warning: More than ten students for {self.start_mages[self.teacher].name} in turn {self.num}.')
        
    def check_study_prerequisites(self):
        for j,m in enumerate(self.start_mages):
            if self.study[j] != 'TEACH':
                if not m.can_study(Skill.string_to_skill(self.study[j])):
                    error(f'Error: {m.name} ({m.id}) cannot study {self.study[j]}')
                    raise ValueError(f'Error: {m.name} ({m.id}) cannot study {self.study[j]}')

    def find_teacher(self):
        for j,m in enumerate(self.start_mages):
            if self.study[j] == 'TEACH':
                self.teacher = j

    def run_turn(self):
        pass
        for j,m in enumerate(self.start_mages):
            if self.study[j] != 'TEACH':
                self.end_mages[j].train(Skill.string_to_skill(self.study[j]), 60 if m in self.taught else 30)