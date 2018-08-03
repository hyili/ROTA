#!/usr/bin/env python3

class ACTION():
    def __init__(self):
        pass

    def run(self, game_board):
        pass


class NEW(ACTION):
    def __init__(self, email):
        super().__init__()
        self.email = email

    def run(self, game_board):
        request = "{0}?request=new&email={1}".format(game_board.request_url_base, self.email)
        result = game_board.session.get(request)

        return result

class PLACE(ACTION):
    def __init__(self, location):
        super().__init__()
        self.location = location

    def run(self, game_board):
        request = "{0}?request=place&location={1}".format(game_board.request_url_base, self.location)
        result = game_board.session.get(request)

        return result

class MOVE(ACTION):
    def __init__(self, src, dst):
        super().__init__()
        self.src = src
        self.dst = dst

    def run(self, game_board):
        request = "{0}?request=move&from={1}&to={2}".format(game_board.request_url_base, self.src, self.dst)
        result = game_board.session.get(request)

        return result

class STATUS(ACTION):
    def __init__(self):
        super().__init__()

    def run(self, game_board):
        request = "{0}?request=status".format(game_board.request_url_base)
        result = game_board.session.get(request)

        return result

class NEXT(ACTION):
    def __init__(self):
        super().__init__()

    def run(self, game_board):
        request = "{0}?request=next".format(game_board.request_url_base)
        result = game_board.session.get(request)

        return result

