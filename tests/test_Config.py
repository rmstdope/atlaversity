import pytest
import unittest.mock as mock

import src.atlaversity.Config

def test_missing_file():
    with pytest.raises(FileNotFoundError):
        src.atlaversity.Config.read_config('invalid')

def test_missing_start_turn():
    with mock.patch('builtins.open', mock.mock_open(read_data=b'factions = [20, 34, 39, 47, 62, 64, 80]')):
        with pytest.raises(ValueError) as valerror:
            src.atlaversity.Config.read_config('filename')
        assert str(valerror.value) == f'Error: No or incorrect "start_turn" config specified in filename\nError: Use the form "start_turn = <int>"'

def test_incorrect_start_turn():
    with mock.patch('builtins.open', mock.mock_open(read_data=b'start_turn=\'1\'\nfactions = [20, 34, 39, 47, 62, 64, 80]')):
        with pytest.raises(ValueError) as valerror:
            src.atlaversity.Config.read_config('filename')
        assert str(valerror.value) == f'Error: No or incorrect "start_turn" config specified in filename\nError: Use the form "start_turn = <int>"'

def test_missing_factions():
    with mock.patch('builtins.open', mock.mock_open(read_data=b'start_turn=1')):
        with pytest.raises(ValueError) as valerror:
            src.atlaversity.Config.read_config('filename')
        assert str(valerror.value) == f'Error: No or incorrect "factions" config specified in filename\nError: Use form factions = [<int>;, ...]'

def test_incorrect_factions():
    with mock.patch('builtins.open', mock.mock_open(read_data=b'start_turn=1\nfactions = 62')):
        with pytest.raises(ValueError) as valerror:
            src.atlaversity.Config.read_config('filename')
        assert str(valerror.value) == f'Error: No or incorrect "factions" config specified in filename\nError: Use form factions = [<int>;, ...]'

