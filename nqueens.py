from random import choice, randint

class NQueens:

    def __init__(self, size):
        self.size = size
        self.board = [None] * size
        self.conflicts = set()
        self.empty_cols = set([x for x in range(1, size + 1)])
        self.vert = [0] * size
        self.left_diag = [0] * (2 * size - 1)
        self.right_diag = [0] * (2 * size - 1)


    def update_counters(self, row, col, delta):
        self.vert[col - 1] += delta
        self.left_diag[self.size - 2 - row + col] += delta
        self.right_diag[row + col - 1] += delta


    def count_conflicts(self, row, col):
        return self.vert[col - 1] + self.left_diag[self.size - 2 - row + col] + self.right_diag[row + col - 1]


    def print_state(self):
        print('board:', self.board)
        print('conflicts:', self.conflicts)
        print('empty_cols:', self.empty_cols)
        print('vert:', self.vert)
        print('left_diag:', self.left_diag)
        print('right_diag:', self.right_diag)

    def update_conflicts(self, row, to):
        for i in range(to):
            if i == row:
                continue
            conflicting = self.board[i] == self.board[row] or abs(self.board[row] - row) == abs(self.board[i] - i)
            if conflicting:
                self.conflicts.add(i)
            elif i in self.conflicts:
                self.conflicts.remove(i)


    def generate_row(self, row):
        def set_vals(col):
            self.board[row] = col
            self.update_counters(row, col, 1)
            self.empty_cols.remove(col)
            if conflicts != 0:
                self.update_conflicts(row, row)
                self.conflicts.add(row)

        for i in range(50):
            col = choice(tuple(self.empty_cols))
            conflicts = self.count_conflicts(row, col)
            if conflicts == 0:
                set_vals(col)
                return

        col = choice(tuple(self.empty_cols))
        set_vals(col)


    def assign(self, row):
        def remove(row, col):
            self.update_counters(row, col, -1)
            if self.vert[col - 1] == 0:
                self.empty_cols.add(col)

        def add(row, col):
            self.update_counters(row, col, 1)
            self.board[row] = col
            if col in self.empty_cols:
                self.empty_cols.remove(col)

        if len(self.empty_cols) > 0:
            for col in self.empty_cols:
                if self.count_conflicts(row, col) == 0:
                    remove(row, self.board[row])
                    add(row, col)
                    self.update_conflicts(row, self.size)
                    self.conflicts.remove(row)
                    return

        for i in range(10):
            col = randint(1, self.size)
            if self.count_conflicts(row, col) == 1:
                remove(row, self.board[row])
                add(row, col)
                self.update_conflicts(row, self.size)
                return


    def generate_initial(self):
        """ assign queens to spaces on initial board,
        returning board and conflicts for each row
        """
        for row in range(self.size):
            self.generate_row(row)


    def draw_board(self):
        """ generate an nxn representation of the board
        """
        drawn_board = ''

        for placement in self.board:
            for i in range(1, placement):
                drawn_board += 'x '
            drawn_board += 'q '
            for j in range(placement, len(self.board)):
                drawn_board += 'x '
            drawn_board = drawn_board[:-1] + '\n'

        return drawn_board[:-1] + '\n' + str(self.board)


    def min_conflicts(self):
        """ use heuristic repair with the min-conflict heuristic
        to reassign placed queens until either a solution is found
        or the max step limit is reached
        :rtype: List[int] or None
        """
        self.generate_initial()

        for i in range(100):
            if len(self.conflicts) == 0:
                if len(self.board) <= 256:
                    return self.draw_board()
                return str(self.board)

            row = choice(tuple(self.conflicts))
            self.assign(row)

        return None


def main():
    """ execute min_conflicts for each size in input file
    """
    with open('nqueens.txt') as input_file:
        for line in input_file:
            while True:
                n_queens = NQueens(int(line))
                result = n_queens.min_conflicts()
                if result:
                    with open('nqueens_out.txt', 'a') as output_file:
                        output_file.write(result + '\n\n')
                    break


if __name__ == '__main__':
    main()
