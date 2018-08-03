#!/usr/bin/env python3

import json

class ML():
    def __init__(self):
        self.score_board = dict()
        self.board_action_history = list()

    def save_to_json(self):
        try:
            print("save to json")
            json.dump(self.score_board, open("/tmp/ML.json", "w"))
        except Exception as e:
            print("Can not write to file. Reason: {0}".format(e))

    def read_from_json(self):
        try:
            print("read from json")
            self.score_board = json.load(open("/tmp/ML.json", "r"))
        except Exception as e:
            print("Can not read from file. Reason: {0}".format(e))
            self.score_board = dict()            
