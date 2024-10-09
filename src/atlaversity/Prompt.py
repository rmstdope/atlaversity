from textual.widgets import Static, Footer, Input
from textual.validation import Validator, ValidationResult
from textual.app import ComposeResult
from textual.suggester import SuggestFromList

skill_names = ['PATT', 'FORC']
class SkillValidator(Validator):
    def validate(self, value:str) -> ValidationResult:
        for skill_name in skill_names:
            if skill_name.lower().startswith(value.lower()):
                return self.success()
        return self.failure()

class PromptInput(Input):
    def on_input_changed(self) -> None:
        # validation_result
        pass
    # self.clear()

class Prompt(Static):
    def compose(self) -> ComposeResult:
        yield PromptInput(placeholder="Type something...", 
                          id=f'prompt',
                          suggester=SuggestFromList(skill_names, case_sensitive=False),
                          validate_on=['changed'],
                          validators=SkillValidator())
        yield Footer()
