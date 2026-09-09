import random
import os
from players.MancalaAI import MancalaAI
def load_player_files():
    ignore_files = [
        "__pycache__",
        "__init__.py",
        "dirty_slate.py",
        "random_idiot.py",
        "MancalaAI.py",
        "seq_dummy.py",
        "easy_peasy.py"
    ]
    players_list = os.listdir('//Users/jason/dev/devpipeline/curriculum/mancala/players')
    for i in ignore_files:
        if i in players_list:
            index_boom = players_list.index(i)
            players_list.pop(index_boom)
    return players_list
players = load_player_files()
pascal_list = []
with open('_slate.py','w') as hacker_file:
    
    for i in players:
        pascal = str(i)
        pascal = pascal.replace('_',' ').title().replace(' ','').split('.')
        pascal = pascal[0]
        i = i.split('.')
        i = i[0]
        hacker_file.write(f'from players.{i} import {pascal}\n')
        pascal_list.append(pascal)
from _slate import *

class DirtySlate(MancalaAI):
    def get_move(self, board_obj):
            random_opponent = random.choice(pascal_list)
            return eval(random_opponent).get_move(self, board_obj)
