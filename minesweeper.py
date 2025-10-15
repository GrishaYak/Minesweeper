from math import sqrt
from random import randint, random
import os
from sys import stdout


def clear():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')


class Field:
    def __init__(self, rows=-1, cols=-1, cnt_of_mines=-1):
        if rows == cols == cnt_of_mines == -1:
            return
        self.rows = rows
        self.cols = cols
        self.cnt_of_mines = cnt_of_mines
        self.closed = self.rows * self.cols
        self.field = [[cells['closed']] * cols] * rows
        self.mines = [[0] * cols] * rows

    def place_mines(self, mines):
        ci = self.rows // 2
        cj = self.cols // 2
        to_place = mines
        max_dist_sq = ci * ci + cj * cj
        while to_place:
            i = randint(0, self.rows - 1)
            j = randint(0, self.cols - 1)
            dist_sq = (i - ci) ** 2 + (j - cj) ** 2
            prob = sqrt(dist_sq / max_dist_sq)
            if random() < prob:
                to_place -= 1
                mines[i][j] = 1

    def get_neighbours(self, i, j, func=None):
        if func is None:
            func = lambda i, j: self.mines[i][j]

        def get(i, j):
            try:
                return func(i, j)
            except IndexError:
                return -1

        neis = [get(i - 1, j), get(i - 1, j - 1), get(i - 1, j + 1), get(i, j - 1), get(i, j + 1), get(i + 1, j - 1),
                get(i + 1, j), get(i + 1, j + 1)]
        res = [el for el in neis if el != -1]
        return res

    def open(self, i, j, open_empty=True):
        """Returns either -2, which means that player has lost, -1, which means that the cell is already opened, 0
         if there is a flag there, 1 if it was opened successfully, and 2 if the player has won."""
        if self.field[i][j] not in [cells['closed']]:
            return 0 if self.field[i][j] == cells['flag'] else -1
        if self.mines[i][j] == 1:
            self.field[i][j] = cells['mine']
            return -2

        self.closed -= 1

        mines_nearby = sum(self.get_neighbours(i, j))
        if mines_nearby > 0:
            self.field[i][j] = str(mines_nearby)
        if mines_nearby == 0:
            self.field[i][j] = cells['empty']
            if open_empty:
                self.open_empty(i, j)

        if self.closed == self.cnt_of_mines:
            return 2
        return 1

    def open_empty(self, i, j):
        to_check = [neighbour_coords(i, j, o) for o in range(8)]
        checked = set()
        while to_check:
            x, y = to_check.pop()
            if (x, y) in checked:
                continue
            checked.add((x, y))
            try:
                self.mines[x][y]
            except IndexError:
                continue
            mines_nearby = sum(self.get_neighbours(i, j))
            self.open(x, y, open_empty=False)
            if mines_nearby == 0:
                to_check += [neighbour_coords(i, j, o) for o in range(8)]

    def set_flag(self, i, j):
        if self.field[i][j] == cells['flag']:
            self.field[i][j] = cells['closed']
            return 1
        if self.field[i][j] == cells['closed']:
            self.field[i][j] = cells['flag']
            return 1
        return -1

    def __str__(self):

        res = '\n  ' + ''.join(map(lambda x: ' ' * (3 - len(str(x))) + str(x), range(1, self.cols + 1))) + '\n'
        for i in range(self.rows):
            row = ' ' * (2 - len(str(i + 1))) + str(i + 1) + ' '
            for j in range(self.cols):
                row += f"[{self.field[i][j]}]"
            res += row + '\n'
        return res

    def handle_next_move(self):
        i, j, a = self.ask_the_move()
        if a == 1:
            return self.open(i, j)
        self.set_flag(i, j)
        return 1

    def ask_the_move(self, show_tips=True):
        """Returns what to do in format "x, y, action", where action is either 1 (open) or 0 (set flag)."""
        if show_tips:
            print("Write your next move in format (x, y, action)")
            print('If you want to open the cell, you may not write any action.')
            print('If you want to set flag, than write "f" or "flag"')
            print(f'1 <= x <= {self.cols}, 1 <= y <= {self.rows}')
        line = input("Your next move: ")
        args = line.split()
        if len(args) not in (2, 3):
            return self.ask_the_move()
        try:
            j, i = map(lambda x: int(x) - 1, args)
        except TypeError:
            return self.ask_the_move()
        if not (0 <= i < self.rows) or not (0 <= j < self.cols):
            return self.ask_the_move()

        if len(args) == 2:
            return i, j, 1
        action = args[2]
        if action in 'f flag'.split():
            return i, j, 0
        if action in 'o open'.split():
            return i, j, 1
        return self.handle_next_move()


def neighbour_coords(x, y, order):
    get_n = [lambda i, j: (i - 1, j), lambda i, j: (i - 1, j - 1), lambda i, j: (i - 1, j + 1),
             lambda i, j: (i, j - 1), lambda i, j: (i, j + 1), lambda i, j: (i + 1, j - 1),
             lambda i, j: (i + 1, j), lambda i, j: (i + 1, j + 1)]
    return get_n[order](x, y)


def start(show_tips=True):
    a = 9
    b = 9
    try:
        if show_tips:
            print("If you want 9x9, then just press enter.")
        line = input('Enter the field size: ')
        if line:
            a, b = map(int, line.split())
    except TypeError:
        start()
    except ValueError:
        start()
    if not (5 < a < 100) or not (5 < b < 100):
        print("Number(s) are out of bounds!")
        start()
    field_params = get_field_params(a, b)
    main_game_cycle(Field(*field_params))


def main_game_cycle(ground: Field):
    code = 1
    while abs(code) != 2:
        out = ''
        if code == -1:
            out += "This cell is already open.\n"
        elif code == 0:
            out += "You can't open the cell with the flag.\n"
        out += str(ground)
        stdout.write(out)
        code = ground.handle_next_move()
    final(code)


def final(code):
    if code == 2:
        win()
    elif code == -2:
        defeat()
    retry = input("Do you want to retry? (print \"y\" if yes)\n")
    if retry == 'y':
        clear()
        start()
    exit()


def win():
    print("You've won!")


def defeat():
    print("You've lost. What a pity.")


def get_field_params(rows, cols):
    diff = ask_difficulty()
    fields = rows * cols
    mines = fields * (1 + diff) // 10
    return rows, cols, mines


def ask_difficulty():
    print("What level of difficulty do you want? (enter num between 1 and 3)")
    level = input()
    if level == 'easy':
        level = 1
    elif level == 'medium':
        level = 2
    elif level == 'hard':
        level = 3
    else:
        try:
            level = int(level)
            if not (0 < level < 4):
                print('Level is out of bounds!')
                ask_difficulty()
        except TypeError:
            print('Wrong Format!')
            ask_difficulty()

    return level


if __name__ == '__main__':
    cells = {'empty': ' ', 'mine': 'o', 'flag': 'P', 'closed': '.'}
    start()
