from copy import deepcopy

from Logging import *
from Skill import *
from Mage import *

class Turn:
    all_turns = []
    comments = []

    @staticmethod
    def save_to_file(file):
        f = open(file, 'w')
        row = 0
        comment = 0
        for i,m in enumerate(Turn.all_turns[0].start_mages):
            if i > 0:
                f.write(',')
            f.write(str(m.id))
        f.write('\n')
        row += 1
        for i,m in enumerate(Turn.all_turns[0].start_mages):
            if i == 0:
                f.write('#')
            else:
                f.write(',')
            f.write(m.name)
        f.write('\n')
        row += 1
        for i,m in enumerate(Turn.all_turns[0].start_mages):
            if i == 0:
                f.write('#')
            else:
                f.write(',')
            f.write(m.comment)
        f.write('\n')
        row += 1
        for t in Turn.all_turns:
            while len(Turn.comments) > comment and Turn.comments[comment][0] == row:
                f.write(Turn.comments[comment][1])
                f.write('\n')
                comment += 1
                row += 1
            for i,s in enumerate(t.study):
                if i > 0:
                    f.write(',')
                f.write(str(s))
                if t.is_teaching(i):
                    for no in t.get_no_teach(i):
                        f.write(f'-{no}')
            f.write('\n')
            row += 1
        while len(Turn.comments) > comment and Turn.comments[comment][0] == row:
            f.write(Turn.comments[comment][1])
            f.write('\n')
            comment += 1
            row += 1

    @staticmethod
    def read_from_file(file, turn):
        f = open(file, 'r')
        strs = f.read().splitlines()
        if len(strs[0].split(',')) != len(Mage.all_mages):
            raise ValueError('mages in plan file does not match the mage list')
        for i,mage_id in enumerate(strs[0].split(',')):
            if int(mage_id.strip()) != Mage.all_mages[i].id:
                raise ValueError('mages in plan file does not match the mage list')
        for i,comment in enumerate(strs[2][1:].split(',')):
            Mage.all_mages[i].comment = comment
        last_mages = Mage.all_mages
        turn_num = turn
        for i in range(3,len(strs)):
            if strs[i][0] != '#':
                p = Turn(last_mages, strs[i], turn_num)
                Turn.all_turns.append(p)
                last_mages = p.end_mages
                turn_num += 1
            else:
                Turn.comments.append((i, strs[i]))

    def __init__(self, mages, data, num):
        self.study = data.split(',')
        self.start_mages = mages
        self.num = num
        if len(self.study) != len(mages):
            raise ValueError(f'Number of mages is not equal to number of orders in turn {num}')
        self.recalculate()

    def reset(self):
        self.end_mages = [deepcopy(m) for m in self.start_mages]
        if hasattr(self, 'teachers'):
            for i,m in enumerate(self.start_mages):
                for no in self.get_no_teach(i):
                    self.study[i] += f'-{no}'
        self.teachers = []
        self.taught = []
        self.no_teach = []

    def setup_teaching(self):
        for ti, teacher in enumerate(self.teachers):
            for mi, m in enumerate(self.start_mages):
                if m not in self.teachers and teacher.can_teach(m, self.study[mi]) and m.id not in self.no_teach[ti]:
                    self.taught[ti].append(m)
        for m in self.start_mages:
            num = 0
            students = []
            for taught in self.taught:
                if m in taught:
                    num += 1
                    students.append(len(taught))
                else:
                    students.append(-1)
            while num > 1:
                index_max = max(range(len(students)), key=students.__getitem__)
                students[index_max] = -1
                num -= 1
                self.taught[index_max].remove(m)
        for ti, teacher in enumerate(self.teachers):
            if len(self.taught[ti]) > 10:
                Logging.warning(f'Warning: More than ten ({len(self.taught[ti])}) students for {teacher.name} in turn {self.num}.')
        
    def check_study_prerequisites(self):
        for j,m in enumerate(self.start_mages):
            if not self.is_teaching(j):
                (can, reason) = m.can_study(self.study[j])
                if not can:
                    Logging.error(f'Error: {m.name} ({m.id}) cannot study {self.study[j]}: {reason}')

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
            if self.study[j] != 'TEACH' and self.study[j] != '':
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
    
    def get_no_teach(self, index):
        for i,t in enumerate(self.teachers):
            if t == self.start_mages[index]:
                return self.no_teach[i]
        return []

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
        self.run_turn()

