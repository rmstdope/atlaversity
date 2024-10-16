from copy import deepcopy

from messages import ok, warning, error
from Skill import *
from Mage import *

class Turn:
    all_turns = []

    @staticmethod
    def read_from_file(file, turn):
        f = open(file, 'r')
        strs = f.read().splitlines()
        if len(strs[0].split(',')) != len(Mage.all_mages):
            raise ValueError('mages in plan file does not match the mage list')
        for i,mage_id in enumerate(strs[0].split(',')):
            if int(mage_id.strip()) != Mage.all_mages[i].id:
                raise ValueError('mages in plan file does not match the mage list')
        for i,comment in enumerate(strs[1].split(',')):
            Mage.all_mages[i].comment = comment
        last_mages = Mage.all_mages
        turn_num = turn
        for i in range(2,len(strs)):
            if strs[i][0] != '#':
                p = Turn(last_mages, strs[i], turn_num)
                Turn.all_turns.append(p)
                last_mages = p.end_mages
                turn_num += 1

    def __init__(self, mages, data, num):
        self.study = data.split(',')
        self.start_mages = mages
        self.num = num
        if len(self.study) != len(mages):
            raise ValueError(f'Number of mages is not equal to number of orders in turn {num}')
        self.recalculate()
        self.run_turn()

    def reset(self):
        self.end_mages = [deepcopy(m) for m in self.start_mages]
        self.teachers = []
        self.taught = []
        self.no_teach = []

    def setup_teaching(self):
        for ti, teacher in enumerate(self.teachers):
            for mi, m in enumerate(self.start_mages):
                if m not in self.teachers and teacher.can_teach(m, self.study[mi]) and m.id not in self.no_teach[ti]:
                    self.taught[ti].append(m)
        # For now, assume at most two teachers
        for m in self.start_mages:
            if len(self.taught) > 1 and m in self.taught[0] and m in self.taught[1]:
                if len(self.taught[0]) > len(self.taught[1]):
                    self.taught[0].remove(m)
                else:
                    self.taught[1].remove(m)
        for ti, teacher in enumerate(self.teachers):
            if len(self.taught[ti]) > 10:
                warning(f'Warning: More than ten ({len(self.taught[ti])}) students for {teacher.name} in turn {self.num}.')
        
    def check_study_prerequisites(self):
        for j,m in enumerate(self.start_mages):
            if not self.is_teaching(j):
                (can, reason) = m.can_study(self.study[j])
                if not can:
                    error(f'Error: {m.name} ({m.id}) cannot study {self.study[j]}: {reason}')

    def setup_teachers(self):
        for j,m in enumerate(self.start_mages):
            if self.study[j].startswith('TEACH'):
                self.teachers.append(m)
                self.taught.append([])
                self.no_teach.append([])
                no_teach = self.study[j].split('-')
                self.study[j] = 'TEACH'
                for t in no_teach[1:]:
                    self.no_teach[len(self.no_teach) - 1].append(int(t))

    def run_turn(self):
        for j,m in enumerate(self.start_mages):
            if self.study[j] != 'TEACH':
                self.end_mages[j].train(Skill.string_to_skill(self.study[j]), 60 if self.is_taught(self.start_mages[j]) else 30)

    def is_teaching(self, index):
        return self.study[index] == 'TEACH'
        
    def get_taught_by_num(self, mage):
        for ti,students in enumerate(self.taught):
            for student in students:
                if student == mage:
                    return ti
        return -1

    def is_taught(self, mage):
        return self.get_taught_by_num(mage) >= 0

    def get_teacher_num_by_mage(self, mage) -> int:
        for i,teacher in enumerate(self.teachers):
            if teacher == mage:
                return i
        return -1

    def can_update(self, mage_num, study):
        ok = True
        old_study = self.study[mage_num]
        self.study[mage_num] = study
        try: self.recalculate()
        except ValueError: ok = False
        self.study[mage_num] = old_study
        self.recalculate()
        return ok        

    def update(self, mage_num, study):
        self.study[mage_num] = study
        self.recalculate()
        
    def recalculate(self):
        self.reset()
        self.setup_teachers()
        self.setup_teaching()
        self.check_study_prerequisites()

