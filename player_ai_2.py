#!/usr/bin/env python3

import requests
import random
import datetime
import time
import lib.board as board

email = "your@email.here"
session = requests.session()
request_url_base = "http://rota.praetorian.com/rota/service/play.php"

if __name__ == "__main__":
    counter = 0
    current_time = datetime.datetime.now()
    random.seed(current_time)
    b = board.GAME_BOARD(email, session, request_url_base)

    try:
        # place
        for turn in range(1, 4, 1):
            # show current board
            b.printBoard()

            # init
            location = 0

            # choose a valid location to place
            els = b.getEmptyLocations()

            location = els[random.randint(0, len(els)-1)]

            # apply action
            b.placeAt(location)

            # check if game is finished
            if b.isFinished():
                raise Exception("Game set. Winner is {0}.".format(b.getWinner()))

        # move
        while True:
            # show current board
            b.printBoard()

            # init
            src = 0
            dst = 0

            # choose a piece and a valid location to move
            pls = b.getPlayerLocations()

            while True:
                # src location
                src = pls[random.randint(0, len(pls)-1)]

                # check our neighbors
                nls = b.getNeighborLocations(src)

                valid_dst = list()
                for nl in nls:
                    if b.checkLocation(nl) == "-":
                        valid_dst.append(nl)

                # if we get both src and dst
                if src and len(valid_dst):
                    dst = valid_dst[random.randint(0, len(valid_dst)-1)]
                    break

                print("Sleep 1 sec.")
                print(valid_dst)
                time.sleep(1)

            # apply action
            b.moveFromTo(src, dst)

            # check if game is finished
            if b.isFinished():
                raise Exception("Game set. Winner is {0}.".format(b.getWinner()))

    except Exception as e:
        b.printBoard()
        print(e)
