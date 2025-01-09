import os
from textual.app import App, ComposeResult
from textual.widgets import Header
from textual.widgets import Footer
import shutil

from atlaversity.game.Game import Game
from atlaversity.editor.Prompt import Prompt
from atlaversity.editor.StudyTable import StudyTable
from atlaversity.editor.MageTable import MageTable
from atlaversity.editor.ValueSelector import ValueSelector
from atlaversity.editor.ValueInput import ValueInput

class OrderEditor(App):
    BINDINGS = [
        ("ctrl+d", "toggle_dark", "Toggle dark mode"),
        ("ctrl+s", "save", "Save study list"),
        ("ctrl+a", "new_turn", "Add new turn"),
    ]
    CSS_PATH = 'OrderEditor.css'

    def __init__(self, game, config):
        super().__init__()
        self.game = game
        self.config = config
        self.selector = None

    def compose(self) -> ComposeResult:
        self.study_table = StudyTable(self, self.game.all_turns)
        yield Header()
        yield self.study_table
        yield MageTable(self, self.game.all_turns)
        yield Footer()

    def action_toggle_dark(self) -> None:
        self.dark = not self.dark

#TODO: Need to use the config path
    def action_save(self) -> None:
        if os.path.exists(self.config.data_dir + 'mages-plan.csv'):
            shutil.copyfile(self.config.data_dir + 'mages-plan.csv', self.config.data_dir + 'mages-plan.backup')
        self.game.save_to_file('mages-plan.csv')
        self.select_value('File saved', ['OK'])

    def action_new_turn(self) -> None:
        self.game.add_new_turn()
        self.study_table.add_empty_turn(self.game.all_turns[len(self.game.all_turns) - 1].num)

    def select_value(self, header, skills, callback = None, context = None):
        if self.selector is None:
            self.selector = ValueSelector(self, header, skills, callback, context)
            self.mount(self.selector)
            self.selector.focus()

    def value_selected(self, value, callback, context):
        self.selector.remove()
        if callback is not None:
            callback(value, context)
        self.selector = None

    def enter_value(self, header, callback, context = None):
        self.selector = ValueInput(self, header, callback, context)
        self.mount(self.selector)
        self.selector.focus()

    def value_entered(self, value, callback, context):
        self.selector.remove()
        if callback is not None:
            callback(value, context)
