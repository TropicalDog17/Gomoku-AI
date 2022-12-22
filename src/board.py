import numpy as np
import piece
import string


class BoardState:
    def __init__(self, size=19, values=None, evals=None, color=piece.BLACK):
        if np.all(values != None):
            self.values = np.copy(values)
        else:
            self.values = np.full((size, size), piece.EMPTY)

        self.size = size
        self.color = color
        self.last_move = None
        self.winner = 0

    def value(self, position):
        return self.values[position]

    def is_valid_position(self, position):
        return (is_inside_board(self.size, position)
                and self.values[position] == piece.EMPTY)

    def possible_moves(self):

        """
        The AI is restricted to play only at cells that are adjacent to occupied cells
        :return: a
        """
        prev_move_idxs = self.values != piece.EMPTY
        area_idxs = expand_area(self.size, prev_move_idxs)
        return np.column_stack(np.where(area_idxs == True))

    def next(self, position):
        next_state = BoardState(size=self.size,
                                values=self.values,
                                color=-self.color)
        next_state[position] = next_state.color
        next_state.last_move = tuple(position)
        return next_state

    def is_terminal(self):
        is_win, color = self.check_five_in_a_row()
        is_full = self.is_full()
        if is_full:
            return True
        return is_win

    def check_five_in_a_row(self):
        pattern = np.full((5,), 1)
        five_black_in_a_row = np.full((5,), 1) * piece.BLACK
        five_white_in_a_row = np.full((5,), 1) * piece.WHITE

        black_win = self.check_pattern(pattern * piece.BLACK)
        white_win = self.check_pattern(pattern * piece.WHITE)

        if black_win:
            self.winner = piece.BLACK
            return True, piece.BLACK
        if white_win:
            self.winner = piece.WHITE
            return True, piece.WHITE
        return False, piece.EMPTY

    def is_full(self):
        return not np.any(self.values == piece.EMPTY)

    def check_pattern(self, pattern):
        count = 0
        for line in self.get_all_lines():
            if issub(line, pattern):
                count += 1
        return count

    def get_all_lines(self):
        """
        Get all possible lines in the board for evaluation purpose
        :return: a list of all valid rows, columns and diagonal(length >= 5)
        """
        l = []

        # rows and cols
        for i in range(self.size):
            l.append(self.values[i, :])
            l.append(self.values[:, i])

        # 2 diags
        for i in range(-self.size + 5, self.size - 4):
            l.append(np.diag(self.values, k=i))
            l.append(np.diag(np.fliplr(self.values), k=i))

        for line in l:
            yield line

    def __getitem__(self, position):
        i, j = position
        return self.values[i, j]

    def __setitem__(self, position, value):
        i, j = position
        self.values[i, j] = value

    def __str__(self):
        alphabet = list(string.ascii_uppercase)
        out = ' ' * 2

        # row
        for i in range(self.size):
            out += f'{alphabet[i]} '
        # out += '{}\n'.format(''.join(
        #     '{}{}'.format((i + 1) % 10, i < 10 and ' ' or "'")
        #     for i in range(self.size)
        # ))
        out += '\n'
        for i in range(self.size):
            out += f'{alphabet[i]} '
            # out += '{}{} '.format(i + 1 < 10 and ' ' or '', i + 1)
            for j in range(self.size):
                out += piece.symbols[self[i, j]]
                if self.last_move and (i, j) == tuple(self.last_move):
                    out += '*'
                else:
                    out += ' '
            if i == self.size - 1:
                out += ''
            else:
                out += '\n'
        return out

    def __repr__(self):
        return self.__str__()


def issub(l, subl):
    l_size = len(l)
    subl_size = len(subl)
    for i in range(l_size - subl_size):
        curr = l[i:min(i + subl_size, l_size - 1)]
        if (curr == subl).all():
            return True
    return False


def expand_area(size, occupied_idxs):
    """
    :param: size: size of the board
    :param: occupied_idxs: a 2D board of boolean value indicating occupied cells in the board
    :return: a 2D board of boolean value indicating cells that are adjacent to each occupied cell.
    """
    area_idxs = np.copy(occupied_idxs)
    for i in range(size):
        for j in range(size):
            if not occupied_idxs[i, j]:
                continue
            for direction in ((1, 0), (0, 1), (1, 1), (1, -1)):
                di, dj = direction
                for side in (1, -1):
                    ni = i + di * side
                    nj = j + dj * side
                    if not is_inside_board(size, (ni, nj)):
                        continue
                    area_idxs[ni, nj] = True
    return np.bitwise_xor(area_idxs, occupied_idxs)


def is_inside_board(board_size, position):
    i, j = position
    return 0 <= i < board_size and 0 <= j < board_size
