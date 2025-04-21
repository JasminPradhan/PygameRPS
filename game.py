class Game:
    def __init__(self, id):
        self.p1Move = False
        self.p2Move = False
        self.ready = False
        self.id = id
        self.moves = [None, None]
        self.wins = [0, 0]
        self.ties = 0
        self.leaderboard = []  # List of top players

        self.names = ["Player 1", "Player 2"]

    def set_player_name(self, p, name):
        self.names[p] = name

    def get_opponent_name(self, p):
        return self.names[1 - p]  # Return the other player's name


    def get_player_move(self, p):
        """
        :param p: [0,1]
        :return:Move
        """
        return self.moves[p]


    def play(self, player, move):
        self.moves[player] = move

        if player == 0:
            self.p1Move = True
        else:
            self.p2Move = True


    def connected(self):
        return self.ready


    def bothMoved(self):
        return self.p1Move and self.p2Move


    def win(self):
        p1 = self.moves[0].upper()[0]
        p2 = self.moves[1].upper()[0]

        print(p1, p2)
        winner = -1  # for tie

        if p1 == 'R' and p2 == 'P':
            winner = 1
        elif p1 == 'R' and p2 == 'S':
            winner = 0
        elif p1 == 'S' and p2 == 'R':
            winner = 1
        elif p1 == 'S' and p2 == 'P':
            winner = 0
        elif p1 == 'P' and p2 == 'S':
            winner = 1
        elif p1 == 'P' and p2 == 'R':
            winner = 0

        return winner

    def resetMove(self):
        self.p1Move = False
        self.p2Move = False


