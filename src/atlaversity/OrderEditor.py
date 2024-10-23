from textual.app import App, ComposeResult
from textual.widgets import Header
import shutil

from Turn import Turn
from Prompt import Prompt
from StudyTable import StudyTable
from MageTable import MageTable
from ValueSelector import ValueSelector
from ValueInput import ValueInput

class OrderEditor(App):
    BINDINGS = [
        ("d", "toggle_dark", "Toggle dark mode"),
        ("s", "save", "Save study list"),
    ]
    CSS_PATH = 'OrderEditor.css'

    def __init__(self, turns):
        super().__init__()
        self.turns = turns

    def compose(self) -> ComposeResult:
        self.study_table = StudyTable(self, self.turns)
        yield Header()
        yield self.study_table
        yield MageTable(self, self.turns)

    def action_toggle_dark(self) -> None:
        self.dark = not self.dark

    def action_save(self) -> None:
        shutil.copyfile('mages-plan.csv', 'mages-plan.backup')
        Turn.save_to_file('mages-plan-new.csv')
        self.select_value('File saved', ['OK'])

    def select_value(self, header, skills, callback = None, context = None):
        self.selector = ValueSelector(self, header, skills, callback, context)
        self.mount(self.selector)
        self.selector.focus()

    def value_selected(self, value, callback, context):
        self.selector.remove()
        if callback is not None:
            callback(value, context)

    def enter_value(self, header, callback, context = None):
        self.selector = ValueInput(self, header, callback, context)
        self.mount(self.selector)
        self.selector.focus()

    def value_entered(self, value, callback, context):
        self.selector.remove()
        if callback is not None:
            callback(value, context)

