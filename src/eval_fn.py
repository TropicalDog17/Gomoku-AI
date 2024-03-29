import numpy as np
from src import piece


def get_eval_state(state, current_color):
    return get_color_evaluation(state, piece.BLACK, current_color) + \
           get_color_evaluation(state, piece.WHITE, current_color)


def get_color_evaluation(state, color, current_color):
    values = state.values
    size = state.size
    current = color == current_color
    evaluation = 0

    # evaluate rows and cols
    for i in range(size):
        evaluation += evaluate_line(values[i, :], color, current)
        evaluation += evaluate_line(values[:, i], color, current)

    # evaluate diags
    for i in range(-size + 5, size - 4):
        evaluation += evaluate_line(np.diag(values, k=i),
                                    color,
                                    current)
        evaluation += evaluate_line(np.diag(np.fliplr(values), k=i),
                                    color,
                                    current)

    return evaluation * color


def evaluate_line(line, color, current):
    evaluation = 0
    size = len(line)
    # consecutive
    consec = 0
    block_count = 2
    empty = False

    for i in range(len(line)):
        value = line[i]
        if value == color:
            consec += 1
        elif value == piece.EMPTY and consec > 0:
            if not empty and i < size - 1 and line[i + 1] == color:
                empty = True
            else:
                evaluation += calc(consec, block_count - 1, current, empty)
                consec = 0
                block_count = 1
                empty = False
        elif value == piece.EMPTY:
            block_count = 1
        elif consec > 0:
            evaluation += calc(consec, block_count, current)
            consec = 0
            block_count = 2
        else:
            block_count = 2

    if consec > 0:
        evaluation += calc(consec, block_count, current)

    return evaluation


def calc(consec, block_count, is_current, has_empty_space=False):
    WIN_GUARANTEE = 10000
    evaluation = 0
    if block_count == 2 and consec < 5:
        return 0
    if consec == 5:
        return WIN_GUARANTEE
    if consec == 4:
        # 4 consecutive stones + player to move -> guarantee win!
        if is_current:
            evaluation = WIN_GUARANTEE
        else:
            # 4 consecutive stones + no_block -> guarantee win in the next move
            # But opponents can also win in the next move, so not 100% guarantee win!
            if block_count == 0:
                evaluation = 1500
            else:
                # 4 consecutive stones + 1 block means opponent need to spend a move blocking
                # So high evaluation score
                evaluation = 300

    if consec == 3:
        if block_count == 0:
            if is_current:
                # 3 consecutive stones + 0 block mean current player will win in next 2 moves,
                # But opponents can also win in 2 moves, so not guarantee win
                return 1000
            else:
                # Opponent needs to block to prevent losing -> fairly high score
                return 200
        else:
            if is_current:
                evaluation = 10
            else:
                evaluation = 2
    if consec == 2:
        if block_count == 0:
            evaluation = 5
        else:
            evaluation = 3
    if consec == 1:
        evaluation = 1

    # Overline -> Surely win
    if consec > 5:
        return WIN_GUARANTEE * 2
    return evaluation

