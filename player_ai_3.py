#!/usr/bin/env python3

import requests
import random
import datetime
import time
import copy
import traceback
import lib.board as game_board

# ML option
ML_ENABLE = True
# Run How many times
ROUNDS = 10
# Learning rate
LEARNING_RATE = 0.25
# GOAL
GOAL = 30
# Basic
email = "your@email.here"
session = requests.session()
request_url_base = "http://rota.praetorian.com/rota/service/play.php"

# TODO: stage 1 player turn
def estimax_stage_1(board, score_board):
    max_score = float("-inf")
    max_score_location = 0

    # choose a valid location to place
    els = board.getEmptyLocations()

    for el in els:
        temp = copy.deepcopy(board)
        score = temp.doDryPlace(el, score_board)

        if max_score != max(max_score, score):
            max_score = score
            max_score_location = el

    return max_score_location

# TODO: stage 2 player turn
def estimax_stage_2(board, score_board):
    max_score = float("-inf")
    max_score_src = 0
    max_score_dst = 0

    # choose a piece and a valid location to move
    pls = board.getPlayerLocations()

    for pl in pls:
        enls = board.getEmptyNeighborLocations(pl)
        for enl in enls:
            temp = copy.deepcopy(board)
            score = temp.doDryMove(pl, enl, score_board)

            if max_score != max(max_score, score):
                max_score = score
                max_score_src = pl
                max_score_dst = enl

    return max_score_src, max_score_dst

def rand_stage_1(board):
    # choose a valid location to place
    els = board.getEmptyLocations()

    location = els[random.randint(0, len(els)-1)]

    return location

def rand_stage_2(board):
    # init
    src = 0
    dst = 0
    
    # choose a piece and a valid location to move
    pls = board.getPlayerLocations()

    while True:
        # src location
        src = pls[random.randint(0, len(pls)-1)]
    
        # check our empty neighbors
        enls = board.getEmptyNeighborLocations(src)
    
        # if we get both src and dst
        if src and len(enls):
            dst = enls[random.randint(0, len(enls)-1)]
            break

        #print("Sleep 1 sec.")
        #time.sleep(1)

    return src, dst

def update_score_board(score_board, index, learning_score, updated):
    if index in updated:
        return

    rotate_indexes = list()
    rotate_indexes.append(index)
    rotate_indexes.append("{0}{1}{2}{3}{4}{5}{6}{7}{8}".format(index[1], index[2], index[5], index[0], index[4], index[8], index[3], index[6], index[7]))
    rotate_indexes.append("{0}{1}{2}{3}{4}{5}{6}{7}{8}".format(index[2], index[5], index[8], index[1], index[4], index[7], index[0], index[3], index[6]))
    rotate_indexes.append("{0}{1}{2}{3}{4}{5}{6}{7}{8}".format(index[5], index[8], index[7], index[2], index[4], index[6], index[1], index[0], index[3]))
    rotate_indexes.append("{0}{1}{2}{3}{4}{5}{6}{7}{8}".format(index[8], index[7], index[6], index[5], index[4], index[3], index[2], index[1], index[0]))
    rotate_indexes.append("{0}{1}{2}{3}{4}{5}{6}{7}{8}".format(index[7], index[6], index[3], index[8], index[4], index[0], index[5], index[2], index[1]))
    rotate_indexes.append("{0}{1}{2}{3}{4}{5}{6}{7}{8}".format(index[6], index[3], index[0], index[7], index[4], index[1], index[8], index[5], index[2]))
    rotate_indexes.append("{0}{1}{2}{3}{4}{5}{6}{7}{8}".format(index[3], index[0], index[1], index[6], index[4], index[2], index[7], index[8], index[5]))

    # reverse
    rotate_indexes.append("{0}{1}{2}{3}{4}{5}{6}{7}{8}".format(index[2], index[1], index[0], index[5], index[4], index[3], index[8], index[7], index[6]))
    rotate_indexes.append("{0}{1}{2}{3}{4}{5}{6}{7}{8}".format(index[1], index[0], index[3], index[2], index[4], index[6], index[5], index[8], index[7]))
    rotate_indexes.append("{0}{1}{2}{3}{4}{5}{6}{7}{8}".format(index[0], index[3], index[6], index[1], index[4], index[7], index[2], index[5], index[8]))
    rotate_indexes.append("{0}{1}{2}{3}{4}{5}{6}{7}{8}".format(index[3], index[6], index[7], index[0], index[4], index[8], index[1], index[2], index[5]))
    rotate_indexes.append("{0}{1}{2}{3}{4}{5}{6}{7}{8}".format(index[6], index[7], index[8], index[3], index[4], index[5], index[0], index[1], index[2]))
    rotate_indexes.append("{0}{1}{2}{3}{4}{5}{6}{7}{8}".format(index[7], index[8], index[5], index[6], index[4], index[2], index[3], index[0], index[1]))
    rotate_indexes.append("{0}{1}{2}{3}{4}{5}{6}{7}{8}".format(index[8], index[5], index[2], index[7], index[4], index[1], index[6], index[3], index[0]))
    rotate_indexes.append("{0}{1}{2}{3}{4}{5}{6}{7}{8}".format(index[5], index[2], index[1], index[8], index[4], index[0], index[7], index[6], index[3]))

    updated.extend(rotate_indexes)
    ris = set(rotate_indexes)

    for ri in ris:
        try:
            score_board[ri] += learning_score
        except:
            score_board[ri] = learning_score

if __name__ == "__main__":
    b = game_board.GAME_BOARD(email, session, request_url_base)

    # TODO: Learning
    score_board = b.ML_tool.score_board
    history = b.ML_tool.board_action_history

    counter = 0

    # How many ROUNDS will we play?
    for R in range(0, ROUNDS, 1):
        if R != 0:
            if counter > GOAL:
                b.startNextRound()
            else:
                b.startNewGame()

            counter = 0
            current_time = datetime.datetime.now()
            random.seed(current_time)
            history.clear()

        try:
            # place
            for turn in range(1, 4, 1):
                # show current board
                b.printBoard()
    
                # TODO: Learning. Choose the MinMax of next board
                esti_max_location = estimax_stage_1(copy.deepcopy(b), score_board)
    
                # TODO: simple random choose
                rand_location = rand_stage_1(copy.deepcopy(b))
    
                # apply action
                if ML_ENABLE:
                    # TODO: Learning record to history
                    action = b.placeAt(esti_max_location)
                    b.ML_tool.board_action_history.append((copy.deepcopy(b.board), action))
                else:
                    b.placeAt(rand_location)
    
                # check if game is finished
                if b.isFinished():
                    raise Exception("Game set. Winner is {0}. Score is {1}. Return moves is {2}.".format(b.getWinner(), counter, b.moves))
    
            # move
            while True:
                # show current board
                b.printBoard()
    
                # TODO: Learning. Choose the MinMax of next board
                esti_max_location = estimax_stage_2(copy.deepcopy(b), score_board)
    
                # TODO: simple random choose
                rand_location = rand_stage_2(copy.deepcopy(b))
    
                # apply action
                counter += 1
                if ML_ENABLE:
                    action = b.moveFromTo(esti_max_location[0], esti_max_location[1])
                    b.ML_tool.board_action_history.append((copy.deepcopy(b.board), action))
                else:
                    b.moveFromTo(rand_location[0], rand_location[1])
    
                # check if game is finished
                if b.isFinished() or counter > GOAL:
                    raise Exception("Game set. Winner is {0}. Score is {1}. Return moves is {2}.".format(b.getWinner(), counter, b.moves))
    
        except Exception as e:
            b.printBoard()
            print(e)
    
        if counter > GOAL:
            # pass ML if game is not end at U_Win
            continue

        # TODO: Learning
        if ML_ENABLE:
            length = len(history)
            updated = list()
            final_score = counter
            learning_score = final_score

            # update the last one to -1
            update_score_board(score_board, b.board, -1, updated)

            if history[-1][0] in score_board:
                difference = -1 - score_board[history[-1][0]]
            else:
                difference = -1

            learning_score = difference * LEARNING_RATE
            update_score_board(score_board, history[-1][0], learning_score, updated)
            for i in range(length-2, 0, -1):
                if history[i][0] in score_board:
                    difference = score_board[history[i+1][0]] - score_board[history[i][0]]
                else:
                    difference = score_board[history[i+1][0]]

                learning_score = difference * LEARNING_RATE
                update_score_board(score_board, history[i][0], learning_score, updated)

#        print(score_board)

    # Close the board
    b.close()
