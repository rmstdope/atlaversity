import types

from prompt_toolkit import PromptSession
from prompt_toolkit import prompt
from prompt_toolkit.completion import NestedCompleter
from prompt_toolkit.history import FileHistory
from prompt_toolkit import print_formatted_text as print
from prompt_toolkit import  HTML
from messages import *

from Mage import Mage
from SkillLevel import SkillLevel
from Skill import Skill
from Turn import Turn

consts = types.SimpleNamespace()
consts.CMD_LIST_MAGE = 'mage'
consts.CMD_CAN_STUDY ='can_study'
consts.CMD_ORDERS ='order'
consts.CMD_QUIT = 'quit'
commands = [consts.CMD_LIST_MAGE, consts.CMD_CAN_STUDY, consts.CMD_ORDERS, consts.CMD_QUIT]

all_mages = []
def read_mages_from_file(faction, turn):
    file = 'mages' + str(faction).zfill(2) + str(turn).zfill(2) + '.csv'
    f = open(file, 'r')
    strs = f.read().splitlines()
    for i, mage in enumerate(strs[0].split(',')[1:]):
        d = mage.split(' ', 1)
        m = Mage(int(d[0]), d[1])
        for skill in strs[1:]:
            d = skill.split(',')
            if int(d[i + 1]) > 0:
                s = SkillLevel(d[0], int(d[i + 1]))
                m.add_skill(s)
        all_mages.append(m)

turns = []
def read_plan_from_file(file, turn):
    f = open(file, 'r')
    strs = f.read().splitlines()
    if len(strs[0].split(',')) != len(all_mages):
        raise ValueError('mages in plan file does not match the mage list')
    for i,mage_id in enumerate(strs[0].split(',')):
        if int(mage_id.strip()) != all_mages[i].id:
            raise ValueError('mages in plan file does not match the mage list')
    for i,comment in enumerate(strs[1].split(',')):
        all_mages[i].comment = comment
    last_mages = all_mages
    for i in range(2,len(strs)):
        if strs[i][0] != '#':
            p = Turn(last_mages, strs[i], turn + i - 2)
            turns.append(p)
            last_mages = p.end_mages


def find_mage_by_id(mage_id) -> Mage:
    for m in all_mages:
        if m.id == int(mage_id):
            return m
    return None

def find_mage_num_by_id(mage_id) -> int:
    for i,m in enumerate(all_mages):
        if m.id == int(mage_id):
            return i
    return -1

start_turn = 9
read_mages_from_file(20, start_turn)
read_mages_from_file(34, start_turn)
read_mages_from_file(47, start_turn)
read_mages_from_file(62, start_turn)

read_plan_from_file('mages-plan.csv', start_turn)

data = consts.CMD_CAN_STUDY
session = PromptSession(history=FileHistory('.atlaversity_history.txt'))

def get_turn(cmds):
    if len(cmds) > 2:
        try:
            turn_num = int(cmds[2])
        except ValueError: 
            turn_num = -1
    else:
        turn_num = start_turn
    if turn_num < start_turn or turn_num >= len(turns) + start_turn:
        error(f'Error: Invalid turn number ({cmds[2]}). Use range {start_turn}-{len(turns) + start_turn - 1} inclusive.')
        return None
    return turns[turn_num - start_turn]

def get_mages(cmds):
    if len(cmds) > 1 and cmds[1].lower() != 'all':
        try:
            mage_id = int(cmds[1])
        except ValueError: 
            mage_id = -1
        mage_num = find_mage_num_by_id(mage_id)
        if mage_num == -1:
            error(f'Error: Mage ID does not exist ({cmds[1]}).')
            return None
        return [(turn.start_mages[mage_num], turn.end_mages[mage_num], turn.study[mage_num])]
    else:
        return zip(turn.start_mages, turn.end_mages, turn.study)

def get_skill(cmds):
    if len(cmds) > 3:
        try:
            return next(x for x in Skill.all_skills if x.name == cmds[3])
        except StopIteration:
            error(f'Error: Unknown skill ({cmds[3]}).')
            return None            
    return None

def print_can_study(m1, m2):
    print(f'    ', end='')
    for s in Skill.all_skills:
        if m1.can_study(s):
            print(f'{s.name} ', end='')
        elif m2.can_study(s):
            green(f'{s.name} ', end='')
    print()

def create_nested_completer():
    skill_dict = {}
    for skill in Skill.all_skills:
        skill_dict[skill.name] = None
    turn_dict = {}
    for turn in turns:
        turn_dict[str(turn.num)] = skill_dict
    mage_dict = {}
    for mage in all_mages:
        mage_dict[str(mage.id)] = turn_dict
    mage_dict['all'] = None
    command_dict = {}
    for command in commands:
        command_dict[command] = mage_dict
    nested_completer = NestedCompleter.from_nested_dict(command_dict)
    return nested_completer

while data != consts.CMD_QUIT:
    data = session.prompt('Command> ', completer=create_nested_completer())
    cmds = data.split(' ')
    turn = get_turn(cmds)
    mages = get_mages(cmds)
    skill = get_skill(cmds)
    if turn != None and mages != None:
        blue(f'Turn {turn.num}')
        match cmds[0]:
            case consts.CMD_LIST_MAGE:
                for m1,m2,s in mages:
                    magenta(f'{m1.long_name} - {m1.comment}')
                    print(m1.get_skill_delta(m2, skill))
            case consts.CMD_CAN_STUDY:
                for m1,m2,s in mages:
                    print(HTML(f'{m1.name} ({m1.id}) can study (before/<ansigreen>after</ansigreen>):'))
                    print_can_study(m1, m2)
            case consts.CMD_ORDERS:
                for m1,m2,s in mages:
                    if s != 'TEACH':
                        print(f'{m1.name} ({m1.id}) : ', end='')
                        green(f'STUDY {s}')
                    else:
                        print(f'{m1.name} ({m1.id}) : ', end='')
                        green(f'TEACH ', end='')
                        for t in turn.taught:
                            green(f'{t.id} ', end='')
                        print()
    
    # data = consts.CMD_QUIT
