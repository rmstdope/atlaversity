import types

from prompt_toolkit import PromptSession
from prompt_toolkit.completion import NestedCompleter
from prompt_toolkit.history import FileHistory
from prompt_toolkit import print_formatted_text as print
from prompt_toolkit import  HTML
from Logging import *

from Mage import *
from SkillLevel import *
from Skill import *
from Turn import *
from OrderEditor import *
import Config
import Game

consts = types.SimpleNamespace()
consts.CMD_LIST_MAGE = 'mage'
consts.CMD_CAN_STUDY ='can_study'
consts.CMD_ORDERS ='order'
consts.CMD_RELOAD = 'reload'
consts.CMD_HOUSING = 'housing'
consts.CMD_EDIT = 'edit'
consts.CMD_QUIT = 'quit'
consts.CMD_EXIT = 'exit'
commands = [consts.CMD_LIST_MAGE, consts.CMD_CAN_STUDY, consts.CMD_ORDERS, consts.CMD_RELOAD, consts.CMD_EDIT, consts.CMD_HOUSING, consts.CMD_QUIT, consts.CMD_EXIT]
editor = None
game = Game.Game()

def reload():
    global editor
    global game
    game = Game.Game()
    try:
        for faction in Config.factions:
            game.read_mages_from_file(faction, Config.start_turn)
        game.read_plan_from_file('mages-plan.csv', Config.start_turn)
    except ValueError as err:
        game = Game.Game()
        Logging.error(err)
    editor = OrderEditor(game)

def get_turn(cmds):
    if len(cmds) > 2:
        try:
            turn_num = int(cmds[2])
        except ValueError: 
            turn_num = -1
    else:
        turn_num = Config.start_turn
    if turn_num < Config.start_turn or turn_num >= len(game.all_turns) + Config.start_turn:
        Logging.error(f'Error: Invalid turn number ({cmds[2]}). Use range {Config.start_turn}-{len(game.all_turns) + Config.start_turn - 1} inclusive.')
        return None
    return game.all_turns[turn_num - Config.start_turn]

def get_mages(cmds):
    if len(cmds) > 1 and cmds[1].lower() != 'all':
        try:
            mage_id = int(cmds[1])
        except ValueError: 
            mage_id = -1
        # TODO Move find_num_by_id to Turn
        mage_num = game.find_num_by_id(mage_id)
        if mage_num == -1:
            Logging.error(f'Error: Mage ID does not exist ({cmds[1]}).')
            return None
        return [(turn.start_mages[mage_num], turn.end_mages[mage_num], turn.study[mage_num])]
    else:
        return zip(turn.start_mages, turn.end_mages, turn.study)

def get_skill(cmds):
    if len(cmds) > 3:
        try:
            return next(x for x in Skill.all_skills if x.name == cmds[3].upper())
        except StopIteration:
            Logging.error(f'Error: Unknown skill ({cmds[3]}).')
            return None            
    return None

def print_can_study(m1, m2):
    print(f'    ', end='')
    for s in Skill.all_skills:
        if m1.can_study(s)[0]:
            print(f'{s.name} ', end='')
        elif m2.can_study(s)[0]:
            Logging.green(f'{s.name} ', end='')
    print()

def housing(mages):
    Logging.green(f'The following mages need housing:')
    num = 0
    for m1,m2,s in mages:
        if s != '' and not s.startswith('TEACH') and m1.get_skill_level(s) >= 2:
            num += 1
            Logging.green(f'{m1.long_name}')
    Logging.green(f'In total, {num} mages need housing.')

def create_nested_completer():
    skill_dict = {}
    for skill in Skill.all_skills:
        skill_dict[skill.name] = None
    turn_dict = {}
    for turn in game.all_turns:
        turn_dict[str(turn.num)] = skill_dict
    mage_dict = {}
    for mage in game.all_mages:
        mage_dict[str(mage.id)] = turn_dict
    mage_dict['all'] = None
    command_dict = {}
    for command in commands:
        command_dict[command] = mage_dict
    nested_completer = NestedCompleter.from_nested_dict(command_dict)
    return nested_completer

Config.read_config('atlaversity.toml')
reload()
session = PromptSession(history=FileHistory('.atlaversity_history.txt'))

data = f''
while len(game.all_turns) > 0:
    data = session.prompt('Command> ', completer=create_nested_completer())
    # data = consts.CMD_EDIT
    cmds = data.split(' ')
    turn = get_turn(cmds)
    mages = get_mages(cmds)
    skill = get_skill(cmds)
    if turn != None and mages != None:
        Logging.blue(f'Turn {turn.num}')
        match cmds[0]:
            case consts.CMD_LIST_MAGE:
                for m1,m2,s in mages:
                    Logging.magenta(f'{m1.long_name} - {m1.comment}')
                    print(m1.get_skill_delta(m2, skill))
            case consts.CMD_CAN_STUDY:
                for m1,m2,s in mages:
                    print(HTML(f'{m1.name} ({m1.id}) can study (before/<ansigreen>after</ansigreen>):'))
                    print_can_study(m1, m2)
            case consts.CMD_ORDERS:
                for mi,(m1,m2,s) in enumerate(mages):
                    if not s.startswith('TEACH'):
                        print(f'{m1.name} ({m1.id}) : ', end='')
                        Logging.green(f'STUDY {s}')
                    else:
                        print(f'{m1.name} ({m1.id}) : ', end='')
                        Logging.green(f'TEACH ', end='')
                        for t in turn.taught[turn.get_teacher_num_by_mage(m1)]:
                            Logging.green(f'{t.id} ', end='')
                        print()
            case consts.CMD_RELOAD:
                reload()
            case consts.CMD_HOUSING:
                housing(mages)
            case consts.CMD_EDIT:
                editor.run()
                editor = OrderEditor(game)
            case consts.CMD_EXIT:
                break
            case consts.CMD_QUIT:
                break
    # break
