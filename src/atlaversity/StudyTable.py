from textual.widgets import DataTable
from rich.text import Text

from Prompt import *
from Turn import *
from Logging import *

class StudyTable(DataTable):
    
    def __init__(self, editor, turns):
        super().__init__(id='study_table')
        self.turns = turns
        self.editor = editor
    
    def get_column_data(self, turn, cells):
        for mage_num,mage in enumerate(turn.start_mages):
            skill = turn.study[mage_num]
            if turn.is_taught(mage):
                skill = Text(f'{skill} (T{turn.get_taught_by_num(mage)})', style="italic #03AC13")
            elif skill == 'TEACH':
                skill = Text(f'{skill} ({turn.get_teacher_num_by_mage(mage)})', style="italic #1323AC")
            elif skill == '':
                skill = Text(f'<No study>', style="italic #03AC13")
            cells.append(skill)

    def on_mount(self):
        self.cursor_type = 'cell'
        self.zebra_stripes = True
        skill_union = set()
        for m in self.turns[len(self.turns) - 1].end_mages:
            for skill_level in m.skill_levels:
                skill_union.add(skill_level.name)
        self.trained_skills = list(skill_union)
        self.trained_skills.sort()
        self.old_column = self.cursor_coordinate.column
        columns = ['Mage']
        for t in self.turns:
            columns.append(str(t.num))
        self.add_columns(*columns)
        rows = []
        for m in self.turns[0].start_mages:
            rows.append([f'{m.name} ({m.id}) - {m.comment}'])
        for t in self.turns:
            cells = []
            self.get_column_data(t, cells)
            for i,c in enumerate(cells):
                rows[i].append(c)
        self.add_rows(rows)
        self.tooltip = "Select a row to get more details"
        
    def on_data_table_cell_highlighted(self):
        if self.cursor_coordinate.column == 0:
            self.cursor_coordinate = self.cursor_coordinate.right()
        else:
            mage_table = self.editor.query_one(f'#mage_table')
            study = self.turns[self.cursor_column - 1].study[self.cursor_row]
            mage_table.update_highlight(self.cursor_row)
            if study == 'TEACH' or study == '':
                mage_table.cursor_type = 'none'
            else:
                mage_table.cursor_type = 'cell'
                col = self.trained_skills.index(study) + 1
                mage_table.move_cursor(row = self.cursor_coordinate.row, column = col, animate = True)
            if self.old_column != self.cursor_coordinate.column:
                mage_table.update()
                self.old_column = self.cursor_coordinate.column

    def on_data_table_cell_selected(self):
        mage = self.turns[self.cursor_column - 1].start_mages[self.cursor_row]
        skills = mage.get_can_study_list()
        skills.append('TEACH')
        self.editor.select_value('Select Skill', skills, self.update)

    def can_update(self, value : str) -> bool:
        return self.turns[self.cursor_column - 1].can_update(self.cursor_row, value)

    def update(self, value : str, context):
        if context is not None and context[:5] == 'TEACH':
            if value != '':
                self.editor.enter_value('Exclude mage (Type ID or press Enter for none)', self.update, context + f'-{value}')
                return
            else:
                value = context
        if value == 'TEACH':
            self.editor.enter_value('Exclude mage (Type ID or press Enter for none)', self.update, 'TEACH')
        else:            
            turn = self.turns[self.cursor_column - 1]
            Logging.clear_message_list()
            turn.update(self.cursor_row, value)
            self.focus()
            cells = []
            self.get_column_data(turn, cells)
            for i,cell in enumerate(cells):
                r,c = self.coordinate_to_cell_key((i, self.cursor_column))
                self.update_cell(r, c, cell)
            if len(Logging.get_message_list()) > 0:
                s = ''
                for m in Logging.get_message_list():
                    s = s + m + '\n'
                self.editor.select_value(s, ['OK'], None)

