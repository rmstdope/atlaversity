from textual.widgets import DataTable
from rich.text import Text

class MageTable(DataTable):
    def __init__(self, editor, turns):
        super().__init__(id='mage_table')
        self.editor = editor
        self.turns = turns

    def on_mount(self):
        self.cursor_type = 'cell'
        self.zebra_stripes = True
        self.fixed_columns = 1
        skill_union = set()
        for m in self.turns[len(self.turns) - 1].end_mages:
            for skill_level in m.skill_levels:
                skill_union.add(skill_level.name)
        self.trained_skills = list(skill_union)
        self.trained_skills.sort()

        self.add_column('Mage', key='Mage')
        for skill in self.trained_skills:
            self.add_column(skill, key=skill)
        for m1 in self.turns[0].start_mages:
            row = []
            row.append(f'{m1.name} ({m1.id})')
            for skill in self.trained_skills:
                row.append('')
            self.add_row(*row, height=1, key=f'{m1.id}')
        self.tooltip = "Select a row to get more details"
        self.update()

    def update(self):
        if hasattr(self, 'trained_skills'):
            widget = self.editor.query_one(f'#study_table')
            turn = widget.cursor_coordinate.column - 1
            for m1,m2 in zip(self.turns[turn].start_mages, self.turns[turn].end_mages):
                for skill in self.trained_skills:
                    d1 = m1.get_skill_level_and_days(skill)
                    d2 = m2.get_skill_level_and_days(skill)
                    if d2 != '0(0)':
                        if d1 == d2:
                            self.update_cell(str(m1.id), skill, f'{d1}', update_width=True)
                        else:
                            self.update_cell(str(m1.id), skill, Text(f'{d1}>{d2}', style='italic #1DAC23'), update_width=True)
                    else:
                        self.update_cell(str(m1.id), skill, f'')

    def on_data_table_column_highlighted(self):
        if self.cursor_coordinate.column == 0:
            self.cursor_coordinate = self.cursor_coordinate.right()

    def on_focus(self):
        self.cursor_type = 'column'
    def on_blur(self):
        self.cursor_type = 'none'
