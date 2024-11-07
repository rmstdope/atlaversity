import tomllib
from Logging import *

def read_config(filename):
    global start_turn, factions
    with open(filename, "rb") as configfile:
        data = tomllib.load(configfile)
    if not 'start_turn' in data or not isinstance(data['start_turn'], int):
        raise ValueError(f'Error: No or incorrect "start_turn" config specified in {filename}\nError: Use the form "start_turn = <int>"')
    if not 'factions' in data or not isinstance(data['factions'], list):
        raise ValueError(f'Error: No or incorrect "factions" config specified in {filename}\nError: Use form factions = [<int>;, ...]')
    start_turn = data['start_turn']
    factions = data['factions']
