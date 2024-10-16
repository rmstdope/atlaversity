from textual.app import App, ComposeResult
from textual.widgets import Header
import shutil

from Prompt import Prompt
from StudyTable import StudyTable
from MageTable import MageTable
from ValueSelector import ValueSelector

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
        yield Prompt('prompt', self)

    def action_toggle_dark(self) -> None:
        self.dark = not self.dark

    def action_save(self) -> None:
        shutil.copyfile('mages-plan.csv', 'mages-plan.backup')

    def select_value(self, name, header, skills):
        self.selector = ValueSelector(self, name, header, skills)
        self.mount(self.selector)
        self.selector.focus()

    def value_selected(self, value):
        self.selector.remove()
        self.study_table.update(value)  
