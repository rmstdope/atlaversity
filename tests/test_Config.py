import pytest

import src.atlaversity.Config

# @pytest.fixture
# def mages():
#     mages = []
#     for i in range(12):
#         mages.append(Mage(100 + i, f'mage{100 + i}'))
#     return mages

def test_missing_file():
    with pytest.raises(FileNotFoundError):
        src.atlaversity.Config.read_config('invalid')

def test_missing_start_turn():
    filename = 'tests/missing_start_turn.toml'
    with pytest.raises(ValueError) as valerror:
        src.atlaversity.Config.read_config(filename)
    assert str(valerror.value) == f'Error: No or incorrect "start_turn" config specified in {filename}\nError: Use the form "start_turn = <int>"'

def test_incorrect_start_turn():
    filename = 'tests/incorrect_start_turn.toml'
    with pytest.raises(ValueError) as valerror:
        src.atlaversity.Config.read_config(filename)
    assert str(valerror.value) == f'Error: No or incorrect "start_turn" config specified in {filename}\nError: Use the form "start_turn = <int>"'

def test_missing_factions():
    filename = 'tests/missing_factions.toml'
    with pytest.raises(ValueError) as valerror:
        src.atlaversity.Config.read_config(filename)
    assert str(valerror.value) == f'Error: No or incorrect "factions" config specified in {filename}\nError: Use form factions = [<int>;, ...]'

def test_incorrect_factions():
    filename = 'tests/incorrect_factions.toml'
    with pytest.raises(ValueError) as valerror:
        src.atlaversity.Config.read_config(filename)
    assert str(valerror.value) == f'Error: No or incorrect "factions" config specified in {filename}\nError: Use form factions = [<int>;, ...]'

