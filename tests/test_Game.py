import pytest
import unittest.mock as mock

from src.atlaversity.Game import Game

def test_read_mages():
    game = Game()
    data ='''Skill,1 One,2 Two,3 Three
    FORC,30,0,0
    PATT,0,60,0
    SPIR,0,0,90'''
    with mock.patch('builtins.open', mock.mock_open(read_data=data)):
        game.read_mages_from_file(62, 10)
    assert len(game.all_mages) == 3
    assert game.all_mages[0].id == 1
    assert game.all_mages[0].name == 'One'
    assert game.all_mages[1].id == 2
    assert game.all_mages[1].name == 'Two'
    assert game.all_mages[2].id == 3
    assert game.all_mages[2].name == 'Three'
    assert game.all_mages[0].get_skill_level_and_days('FORC') == '1(30)'
    assert game.all_mages[1].get_skill_level_and_days('PATT') == '1(60)'
    assert game.all_mages[2].get_skill_level_and_days('SPIR') == '2(90)'
    assert game.all_mages[0].get_skill_level_and_days('PATT') == '0(0)'

def test_read_mages_multiple():
    game = Game()
    data1 ='''Skill,1 One,2 Two
'''
    data2 ='''Skill,3 Three,4 Four
'''
    with mock.patch('builtins.open', mock.mock_open(read_data=data1)):
        game.read_mages_from_file(62, 10)
    with mock.patch('builtins.open', mock.mock_open(read_data=data2)):
        game.read_mages_from_file(64, 10)
    assert len(game.all_mages) == 4
    assert game.all_mages[0].id == 1
    assert game.all_mages[1].id == 2
    assert game.all_mages[2].id == 3
    assert game.all_mages[3].id == 4
