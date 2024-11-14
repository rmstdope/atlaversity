from enum import StrEnum

from prompt_toolkit import PromptSession
from prompt_toolkit.history import FileHistory
from prompt_toolkit.completion import NestedCompleter

from Game import *
from OrderEditor import *
import Config

class CommandLine(PromptSession):

    class Commands(StrEnum):
        CMD_LIST_MAGE = 'mage'
        CMD_CAN_STUDY ='can_study'
        CMD_ORDERS ='order'
        CMD_RELOAD = 'reload'
        CMD_HOUSING = 'housing'
        CMD_EDIT = 'edit'
        CMD_QUIT = 'quit'
        CMD_EXIT = 'exit'    

    def __init__(self):
        super().__init__(self, history=FileHistory('.atlaversity_history.txt'))
        self.editor = None
        self.game = Game()

    def run(self):
        self.reload()
        data = f''
        while len(self.game.all_turns) > 0:
            data = self.prompt('Command> ', completer=self.create_nested_completer())
            # data = self.Commands.CMD_EDIT
            cmds = data.split(' ')
            turn = self.get_turn(cmds)
            mages = self.get_mages(cmds, turn)
            skill = self.get_skill(cmds)
            if turn != None and mages != None:
                Logging.blue(f'Turn {turn.num}')
                match cmds[0]:
                    case self.Commands.CMD_LIST_MAGE:
                        for m1,m2,s in mages:
                            Logging.magenta(f'{m1.long_name} - {m1.comment}')
                            print(m1.get_skill_delta(m2, skill))
                    case self.Commands.CMD_CAN_STUDY:
                        for m1,m2,s in mages:
                            print(HTML(f'{m1.name} ({m1.id}) can study (before/<ansigreen>after</ansigreen>):'))
                            self.print_can_study(m1, m2)
                    case self.Commands.CMD_ORDERS:
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
                    case self.Commands.CMD_RELOAD:
                        self.reload()
                    case self.Commands.CMD_HOUSING:
                        self.housing(mages)
                    case self.Commands.CMD_EDIT:
                        self.editor.run()
                        self.editor = OrderEditor(self.game)
                    case self.Commands.CMD_EXIT:
                        break
                    case self.Commands.CMD_QUIT:
                        break
            # break

    def reload(self):
        self.game = Game()
        try:
            for faction in Config.factions:
                self.game.read_mages_from_file(faction, Config.start_turn)
            self.game.read_plan_from_file('mages-plan.csv', Config.start_turn)
        except ValueError as err:
            self.game = Game()
            Logging.error(err)
        self.editor = OrderEditor(self.game)

    def create_nested_completer(self):
        skill_dict = {}
        for skill in Skill.all_skills:
            skill_dict[skill.name] = None
        turn_dict = {}
        for turn in self.game.all_turns:
            turn_dict[str(turn.num)] = skill_dict
        mage_dict = {}
        for mage in self.game.all_mages:
            mage_dict[str(mage.id)] = turn_dict
        mage_dict['all'] = None
        command_dict = {}
        for command in self.Commands:
            command_dict[command.value] = mage_dict
        nested_completer = NestedCompleter.from_nested_dict(command_dict)
        return nested_completer

    def get_turn(self, cmds):
        if len(cmds) > 2:
            try:
                turn_num = int(cmds[2])
            except ValueError: 
                turn_num = -1
        else:
            turn_num = Config.start_turn
        if turn_num < Config.start_turn or turn_num >= len(self.game.all_turns) + Config.start_turn:
            Logging.error(f'Error: Invalid turn number ({cmds[2]}). Use range {Config.start_turn}-{len(self.game.all_turns) + Config.start_turn - 1} inclusive.')
            return None
        return self.game.all_turns[turn_num - Config.start_turn]

    def get_mages(self, cmds, turn):
        if len(cmds) > 1 and cmds[1].lower() != 'all':
            try:
                mage_id = int(cmds[1])
            except ValueError: 
                mage_id = -1
            # TODO Move find_num_by_id to Turn
            mage_num = self.game.find_num_by_id(mage_id)
            if mage_num == -1:
                Logging.error(f'Error: Mage ID does not exist ({cmds[1]}).')
                return None
            return [(turn.start_mages[mage_num], turn.end_mages[mage_num], turn.study[mage_num])]
        else:
            return zip(turn.start_mages, turn.end_mages, turn.study)

    def get_skill(self, cmds):
        if len(cmds) > 3:
            try:
                return next(x for x in Skill.all_skills if x.name == cmds[3].upper())
            except StopIteration:
                Logging.error(f'Error: Unknown skill ({cmds[3]}).')
                return None            
        return None

    def print_can_study(self, m1, m2):
        print(f'    ', end='')
        for s in Skill.all_skills:
            if m1.can_study(s)[0]:
                print(f'{s.name} ', end='')
            elif m2.can_study(s)[0]:
                Logging.green(f'{s.name} ', end='')
        print()

    def housing(self, mages):
        Logging.green(f'The following mages need housing:')
        num = 0
        for m1,m2,s in mages:
            if s != '' and not s.startswith('TEACH') and m1.get_skill_level(s) >= 2:
                num += 1
                Logging.green(f'{m1.long_name}')
        Logging.green(f'In total, {num} mages need housing.')
