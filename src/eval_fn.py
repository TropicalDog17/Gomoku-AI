import numpy as np
import piece


def evaluation_state(state, current_color):
    return evaluate_color(state, piece.BLACK, current_color) + \
           evaluate_color(state, piece.WHITE, current_color)


def evaluate_color(state, color, current_color):
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

    if consec >= 5:
        if has_empty_space:
            evaluation = 8000
        else:
            evaluation = 10000
    if consec == 4:
        if is_current:
            if block_count == 0:
                evaluation = 10000
            else:
                evaluation = 5000
        else:
            # 4 consecutive stones + user to move -> guarantee win!
            if block_count == 0:
                evaluation = 1500
            else:
                # 4 consecutive stones + 1 block means opponent need to spend a move blocking, so high score
                evaluation = 250

    if consec == 3:
        if block_count == 0:
            if is_current:
                # 3 consecutive stones + 0 block mean current player will win in next 2 moves,
                # But opponents can also win in 2 moves, so not guarantee win
                evaluation = 1000
            else:
                # Opponent needs to block to prevent losing
                evaluation = 200
        else:
            if is_current:
                evaluation = 10
            else:
                evaluation = 2
    if consec == 2:
        if block_count == 0:
            if is_current:
                evaluation = 2
            else:
                evaluation = 2
        else:
            evaluation = 1
    if consec > 5:
        evaluation = WIN_GUARANTEE * 2
    return evaluation

    consec_score = (2, 5, 1000, 10000)
    # 3: 0.05
    block_count_score = (0.5, 0.6, 0.01, 0.25)
    not_current_score = (1, 1, 0.2, 0.15)
    empty_space_score = (1, 1.2, 0.9, 0.4)

    consec_idx = consec - 1
    value = consec_score[consec_idx]
    if block_count == 1:
        value *= block_count_score[consec_idx]
    if not is_current:
        value *= not_current_score[consec_idx]
    if has_empty_space:
        value *= empty_space_score[consec_idx]
    return int(value)
