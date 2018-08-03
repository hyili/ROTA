#!/usr/bin/env python3

import json
import copy
import lib.action as a
import lib.ml as ml

VALID_LINK = {
    1: [2, 4, 5],
    2: [1, 3, 5],
    3: [2, 5, 6],
    4: [1, 5, 7],
    5: [1, 2, 3, 4, 6, 7, 8, 9],
    6: [3, 5, 9],
    7: [4, 5, 8],
    8: [5, 7, 9],
    9: [5, 6, 8]
}


class GAME_BOARD():
    def __init__(self, email, session, request_url_base):
        # Init
        print("Initialinze Game_Board object.")

        self.ML_tool = ml.ML()

        self.email = email
        self.session = session
        self.request_url_base = request_url_base

        self.init()

        self.startNewGame()
        print("Ready.")

    # Board method
    def init(self):
        self.ML_tool.read_from_json()
        self.board = "---------"
        self.I_win = 0
        self.U_win = 0
        self.moves = 0
        self.won = 0

    def reset(self):
        self.r_board = self.board
        self.r_I_win = self.I_win
        self.r_U_win = self.U_win
        self.r_moves = self.moves
        self.r_won = self.won

        self.board = "---------"
        self.I_win = 0
        self.U_win = 0
        self.moves = 0
        self.won = 0

    def close(self):
        self.ML_tool.save_to_json()
        self.session.close()

    def getBoard(self):
        return self.board

    def printBoard(self, board=None):
        if board == None:
            board = self.board

        for i in range(0, 3, 1):
            print("{0} {1} {2}".format(board[3*i+0], board[3*i+1], board[3*i+2]))

    def printHistory(self):
        for history in self.ML_tool.board_action_history:
            self.printBoard(history[0])
            print(type(history[1]).__name__)

    def checkLocation(self, location):
        if location > 0 and location < 10:
            return self.board[location-1]
        else:
            return None

    def getNeighborLocations(self, location):
        return VALID_LINK[location]

    def isFinished(self):
        result = True if self.I_win != self.r_I_win or self.U_win != self.r_U_win else False

        return result

    def isReachGoal(self):
        result =  True if self.moves > 30 else False

        return result

    def getComputerLocations(self):
        result = list()
        for location in range(0, 9, 1):
            if self.board[location] == "c":
                result.append(location+1)

        return result

    def getPlayerLocations(self):
        result = list()
        for location in range(0, 9, 1):
            if self.board[location] == "p":
                result.append(location+1)

        return result

    def getEmptyLocations(self):
        result = list()
        for location in range(0, 9, 1):
            if self.board[location] == "-":
                result.append(location+1)

        return result

    def getEmptyNeighborLocations(self, location):
        result = list()
        nls = self.getNeighborLocations(location)
    
        for nl in nls:
            if self.checkLocation(nl) == "-":
                result.append(nl)

        return result

    def getWinner(self):
        if self.isFinished():
            return "Player" if self.I_win else "Computer"

    # Do actions
    def updateGameBoard(self, data):
        self.board = data["board"]
        self.I_win = data["player_wins"]
        self.U_win = data["computer_wins"]
        self.moves = data["moves"]
        self.won = data["games_won"]

    def doAction(self, action):
        result = action.run(self)

        try:
            if result.status_code != 200:
                raise Exception("status_code: {0}".format(str(result.status_code)))

            data = json.loads(result.text)

            if "status" in data:
                if data["status"] == "success":
                    self.updateGameBoard(data["data"])
                    return 0
                else:
                    print("Apply action {0} failed.".format(type(action).__name__))
                    raise Exception("{0}".format(data["data"]))
            else:
                raise Exception("Invalid operation: {0}".format(data["data"]))
        except Exception as e:
            traceback.print_exc()
            print("Error occurred. Reason: {0}".format(e))

        return 1

    def startNewGame(self, dry=False):
        print("Preparing to start new game...")
        self.reset()
        action = a.NEW(self.email)
        if not dry:
            self.doAction(action)

        return action

    def placeAt(self, location, dry=False):
        print("Preparing to place at {0}.".format(location))
        action = a.PLACE(location)
        if not dry:
            self.doAction(action)

        return action

    def moveFromTo(self, src, dst, dry=False):
        print("Preparing to move from {0} to {1}.".format(src, dst))
        action = a.MOVE(src, dst)
        if not dry:
            self.doAction(action)

        return action

    def getCurrentStatus(self, dry=False):
        print("Preparing to show status.")
        action = a.STATUS()
        if not dry:
            self.doAction(action)

        return action

    def startNextRound(self, dry=False):
        print("Preparing to start next round.")
        self.reset()
        action = a.NEXT()
        if not dry:
            self.doAction(action)

        return action


    # TODO: Player method

    # TODO: estimax Learning Player method
    def doDryPlace(self, location, score_board):
        # player turn
        self.board = "{0}p{1}".format(self.board[0:location-1], self.board[location:])

        # computer turn
        # still stage 1
        total_score = 0
        total_moves = 0
        els = self.getEmptyLocations()
        if len(els) > 3:
            for el in els:
                total_moves += 1
                self.board = "{0}c{1}".format(self.board[0:el-1], self.board[el:])
                try:
                    total_score += score_board[self.board]
                except:
                    # self.board not yet in score_board
                    pass
                self.board = "{0}-{1}".format(self.board[0:el-1], self.board[el:])

        # stage 2
        else:
            cls = self.getComputerLocations()
            for cl in cls:
                enls = self.getEmptyNeighborLocations(cl)
                for enl in enls:
                    total_moves += 1
                    self.board = "{0}-{1}".format(self.board[0:cl-1], self.board[cl:])
                    self.board = "{0}c{1}".format(self.board[0:enl-1], self.board[enl:])
                    try:
                        total_score += score_board[self.board]
                    except:
                        # self.board not yet in score_board
                        pass
                    self.board = "{0}c{1}".format(self.board[0:cl-1], self.board[cl:])
                    self.board = "{0}-{1}".format(self.board[0:enl-1], self.board[enl:])

        total_score /= total_moves
        return total_score

    # TODO: estimax Learning Player method
    def doDryMove(self, src, dst, score_board):
        # player turn
        self.board = "{0}-{1}".format(self.board[0:src-1], self.board[src:])
        self.board = "{0}p{1}".format(self.board[0:dst-1], self.board[dst:])

        # computer turn
        # stage 2
        total_score = 0
        total_moves = 0

        cls = self.getComputerLocations()
        for cl in cls:
            enls = self.getEmptyNeighborLocations(cl)
            for enl in enls:
                total_moves += 1
                self.board = "{0}-{1}".format(self.board[0:cl-1], self.board[cl:])
                self.board = "{0}c{1}".format(self.board[0:enl-1], self.board[enl:])
                try:
                    total_score += score_board[self.board]
                except:
                    # self.board not yet in score_board
                    pass
                self.board = "{0}c{1}".format(self.board[0:cl-1], self.board[cl:])
                self.board = "{0}-{1}".format(self.board[0:enl-1], self.board[enl:])

        total_score /= total_moves
        return total_score
