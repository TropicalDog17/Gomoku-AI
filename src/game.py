from src import piece
import numpy as np
from src.board import BoardState
from src.ai import get_best_move


class GameRunner:
    def __init__(self, depth, color=piece.BLACK, size=19, ):
        self.size = size
        self.depth = depth
        self.finished = False
        self.restart(color=color)

    def restart(self, color, player_index=-1):
        self.is_max_state = True if player_index == -1 else False
        self.state = BoardState(self.size, color=color)
        self.ai_color = -player_index

    def play(self, i, j):
        position = (i, j)
        if self.state.color != self.ai_color:
            return False
        if not self.state.is_valid_position(position):
            return False
        self.state = self.state.next(position)
        self.finished = self.state.is_terminal()
        return True

    def aiplay(self):
        # import time
        # t = time.time()
        if self.state.color == self.ai_color:
            return False, (0, 0)
        move, value = get_best_move(self.state, self.depth, self.is_max_state)
        self.state = self.state.next(move)
        self.finished = self.state.is_terminal()
        # print(time.time() - t)
        return True, move

