from textual.widgets import DataTable

class ValueSelector(DataTable):
    def __init__(self, editor, name, header, values):
        super().__init__(id = name)
        self.editor = editor
        self.header = header
        self.values = values

    def on_mount(self):
        self.cursor_type = 'cell'
        self.zebra_stripes = True
        self.add_column(self.header, key='Mage')
        for s in self.values:
            row = [s]
            self.add_row(*row, height=1)

    def on_data_table_cell_selected(self):
        self.editor.value_selected(self.values[self.cursor_row])
