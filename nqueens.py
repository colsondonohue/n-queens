from random import choice, randint

def assign(board, row, conflicts):
    """ assign queen to column in row such that conflicts are minimized
    :rtype: Tuple(int, Set[int])
    """

    min_conflicts = float('inf') # current lowest number of conflicts
    min_columns = [] # the current columns with the minimum number of conflicts
    column_conflicts = [] # the corresponding sets of conflicts for each column

    for i in range(1, len(board) + 1):
        current_conflicts = 0
        temp_conflicts = set()

        for j, current in enumerate(board):
            if j == row:
                continue
            # check vertical
            if current == i:
                current_conflicts += 1
                temp_conflicts.add(j)
                # print('vertical conflict: column', i, ' in row', row, ' with column', current, ' in row', j)
            # check left diagonal
            if i - (row - j) == current:
                current_conflicts += 1
                temp_conflicts.add(j)
                # print('left diagonal conflict: column', i, ' in row', row, ' with column', current, ' in row', j)
            # check right diagonal
            if i + (row - j) == current:
                current_conflicts += 1
                temp_conflicts.add(j)
                # print('right diagonal conflict: column', i, ' in row', row, ' with column', current, ' in row', j)

        if current_conflicts == min_conflicts:
            min_columns.append(i)
            column_conflicts.append(temp_conflicts)
        if current_conflicts < min_conflicts:
            min_conflicts = current_conflicts
            min_columns = [i]
            column_conflicts = [temp_conflicts]


    if min_conflicts > 0:
        conflicts.add(row)
    if min_conflicts == 0 and row in conflicts:
        conflicts.remove(row)

    tiebreak = randint(0, len(min_columns) - 1)

    return min_columns[tiebreak], conflicts.union(column_conflicts[tiebreak])


def generate_initial(size):
    """ assign queens to spaces on initial board,
    returning board and conflicts for each row
    :type size: int
    :rtype: Tuple(List[int], Set[int])
    """
    board = [None] * size
    conflicts = set()

    for row in range(size):
        column, conflicts = assign(board, row, conflicts)
        board[row] = column

    return board, conflicts


def draw_board(board):
    """ generate an nxn representation of the board
    :type board: List[int]
    """
    drawn_board = ''

    for placement in board:
        for i in range(1, placement):
            drawn_board += 'x '
        drawn_board += 'q '
        for j in range(placement, len(board)):
            drawn_board += 'x '
        drawn_board = drawn_board[:-1] + '\n'

    return drawn_board[:-1]


def min_conflicts(size):
    """ use heuristic repair with the min-conflict heuristic
    to reassign placed queens until either a solution is found
    or the max step limit is reached
    :type size: int
    :rtype: List[int] or None
    """
    board, conflicts = generate_initial(size)

    for i in range(100):
        print(i)
        if len(conflicts) == 0:
            if len(board) <= 256:
                return draw_board(board) + '\n' + str(board)
            return str(board)

        row = choice(tuple(conflicts))
        board[row], conflicts = assign(board, row, conflicts)

    return None


def main():
    """ execute min_conflicts for each size in input file
    """
    with open('nqueens.txt') as input_file:
        for line in input_file:
            while True:
                result = min_conflicts(int(line))
                if result:
                    with open('nqueens_out.txt', 'a') as output_file:
                        output_file.write(result + '\n\n')
                    break

if __name__ == '__main__':
    main()
