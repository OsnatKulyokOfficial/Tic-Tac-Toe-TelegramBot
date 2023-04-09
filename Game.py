class Game:
    WIN_LANES = [
        [0, 1, 2],
        [3, 4, 5],
        [6, 7, 8],
        [0, 3, 6],
        [1, 4, 7],
        [2, 5, 8],
        [0, 4, 8],
        [2, 4, 6]
    ]

    def __init__(self) -> None:
        self.board = ['' for i in range(9)]
        self.weights = [0 for i in range(9)]
        self.is_game_on = True

    def turn(self, index):
        if not self.is_game_on:
            return
        if self.board[index]:
            return 'Not empty'
        self.board[index] = 'X'
        # checks if there is any lane where all boxes hold X, you can't win but for the sport we will check anyway
        if any([all([self.board[g] == 'X' for g in i]) for i in Game.WIN_LANES]):
            self.is_game_on = False
            return 'X wins'
        if not all(self.board):
            return self.o_play()
        return 'Tie'

    def o_play(self):
        if not self.board[4]:
            self.board[4] = 'O'
            return 4
        if ''.join(self.board) == 'XOX' and (''.join(self.board[2:7:4]) == 'XX' or ''.join(self.board[::8]) == 'XX'):
            self.board[3] = 'O'
            return 3
        self.weights = [-10 ** 3 if i else 0 for i in self.board]
        self.balance()
        max_weight = max(self.weights)
        max_index = self.weights.index(max_weight)
        self.board[max_index] = 'O'
        if max_weight >= 100:
            self.is_game_on = False
            return f'O wins by playing {max_index}'
        return max_index
        # return f'O wins by playing {max_index}' if max_weight >= 100 else max_index

    def balance(self):
        for lane in Game.WIN_LANES:
            lane_marks = [self.board[i] for i in lane]
            xs = lane_marks.count('X')
            os = lane_marks.count('O')
            for i in lane:
                self.weights[i] += 10 ** (xs - 1)
                if os == 2:
                    self.weights[i] += 10 ** 2
