from textual.widgets import DataTable
from rich.text import Text

from Prompt import Prompt

from Turn import *

class StudyTable(DataTable):
    
    def __init__(self, editor, turns):
        super().__init__(id='study_table')
        self.turns = turns
        self.editor = editor
    
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
            for mi,m in enumerate(t.start_mages):
                skill = t.study[mi]
                if t.is_taught(m):
                    skill = Text(f'{skill} (T{t.get_taught_by_num(m)})', style="italic #03AC13")
                elif skill == 'TEACH':
                    skill = Text(f'{skill} ({t.find_teacher_num_by_mage(m)})', style="italic #1323AC")
                rows[mi].append(skill)
        self.add_rows(rows)
        self.tooltip = "Select a row to get more details"
        
    def on_data_table_cell_highlighted(self):
        if self.cursor_coordinate.column == 0:
            self.cursor_coordinate = self.cursor_coordinate.right()
        else:
            mage_table = self.editor.query_one(f'#mage_table')
            study = self.turns[self.cursor_column - 1].study[self.cursor_row]
            if study == 'TEACH':
                mage_table.cursor_type = 'none'
            else:
                mage_table.cursor_type = 'cell'
                col = self.trained_skills.index(study) + 1
                mage_table.move_cursor(row = self.cursor_coordinate.row, column = col, animate = True)
            if self.old_column != self.cursor_coordinate.column:
                mage_table.update()
                self.old_column = self.cursor_coordinate.column

    def on_data_table_cell_selected(self):
        widget = self.editor.query_one(f'#prompt', expect_type=Prompt)
        widget.focus()
