#!/usr/bin/env python3

import requests
import lib.board as board

email = "your@email.here"
session = requests.session()
request_url_base = "http://rota.praetorian.com/rota/service/play.php"

if __name__ == "__main__":
    counter = 0
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

            location = els[0]

            # apply action
            b.placeAt(location)

            # check if game is finished
            if b.isFinished():
                raise Exception("Game set. Winner is {0}.".format(b.getWinner()))

        # move
        while True:
            # init
            src = 0
            dst = 0

            # choose a piece and a valid location to move
            pls = b.getPlayerLocations()

            for pl in pls:
                # src location
                src = pl

                # check our neighbors
                nls = b.getNeighborLocations(pl)
                for nl in nls:
                    if b.checkLocation(nl) == "-":
                        dst = nl
                        break

                    # if we get both src and dst
                    if src and dst:
                        break

            # apply action
            b.moveFromTo(src, dst)

            # check if game is finished
            if b.isFinished():
                raise Exception("Game set. Winner is {0}.".format(b.getWinner()))

    except Exception as e:
        b.printBoard()
        print(e)
