from textual.widgets import DataTable

class ValueSelector(DataTable):
    def __init__(self, editor, header, values, callback, context):
        super().__init__()
        self.editor = editor
        self.header = header
        self.values = values
        self.callback = callback
        self.context = context

    def on_mount(self):
        self.cursor_type = 'cell'
        self.zebra_stripes = True
        self.add_column(self.header, key='Mage')
        for s in self.values:
            row = [s]
            self.add_row(*row, height=1)

    def on_data_table_cell_selected(self):
        self.editor.value_selected(self.values[self.cursor_row], self.callback, self.context)

    def on_key(self, event):
        key = event.key.upper()
        if key >= 'A' and key <= 'Z':
            for i,v in enumerate(self.values):
                if len(v) > 0 and v[0].upper() == key:
                    self.move_cursor(row = i)
                    break
        return super()._on_key(event)