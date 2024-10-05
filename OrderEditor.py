from textual.app import App, ComposeResult
from textual.widgets import Header
#, Footer

from Prompt import Prompt
from StudyTable import StudyTable
from MageTable import MageTable

class OrderEditor(App):
    BINDINGS = [("d", "toggle_dark", "Toggle dark mode")]
    DEFAULT_CSS = """
    Input {
        border: none;
        height: 1;
    }
    Input:focus {
        border: none;
        height: 1;
    }
    Prompt {
        dock: bottom;
    }
    """

    def __init__(self, turns):
        super().__init__()
        self.turns = turns

    def compose(self) -> ComposeResult:
        yield Header()
        yield StudyTable(self, self.turns)
        yield MageTable(self, self.turns)
        yield Prompt(id='prompt')
        #yield Footer()

    def action_toggle_dark(self) -> None:
        self.dark = not self.dark
