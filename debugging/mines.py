#!/usr/bin/python3
import random
import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

class Minesweeper:
    def __init__(self, width=1, height=2, mines=1):
        self.width = width
        self.height = height
        self.mines = set(random.sample(range(width * height), mines))
        self.field = [[' ' for _ in range(width)] for _ in range(height)]
        self.revealed = [[False for _ in range(width)] for _ in range(height)]
        self.flagged = [[False for _ in range(width)] for _ in range(height)]
        self.remaining_mines = mines

    def print_board(self, reveal=False):
        clear_screen()
        print(f"Remaining mines: {self.remaining_mines}")
        print('  ' + ' '.join(str(i) for i in range(self.width)))
        for y in range(self.height):
            print(y, end=' ')
            for x in range(self.width):
                if reveal and (y * self.width + x) in self.mines:
                    print('*', end=' ')
                elif self.flagged[y][x]:
                    print('F', end=' ')
                elif self.revealed[y][x]:
                    count = self.count_mines_nearby(x, y)
                    print(count if count > 0 else ' ', end=' ')
                else:
                    print('.', end=' ')
            print()

    def count_mines_nearby(self, x, y):
        count = 0
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    if (ny * self.width + nx) in self.mines:
                        count += 1
        return count

    def reveal(self, x, y):
        if not (0 <= x < self.width and 0 <= y < self.height):
            return True
        if self.revealed[y][x] or self.flagged[y][x]:
            return True
        if (y * self.width + x) in self.mines:
            return False
        self.revealed[y][x] = True
        if self.count_mines_nearby(x, y) == 0:
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    self.reveal(x + dx, y + dy)
        return True

    def toggle_flag(self, x, y):
        if not self.revealed[y][x]:
            self.flagged[y][x] = not self.flagged[y][x]
            self.remaining_mines += 1 if not self.flagged[y][x] else -1

    def check_win(self):
        return all(self.revealed[y][x] or (y * self.width + x) in self.mines
                   for y in range(self.height) for x in range(self.width))

    def play(self):
        while True:
            self.print_board()
            try:
                action = input("Enter action (r for reveal, f for flag) and coordinates (e.g., r 3 4): ").split()
                if len(action) != 3:
                    raise ValueError
                act, x, y = action[0].lower(), int(action[1]), int(action[2])
                if act == 'r':
                    if not self.reveal(x, y):
                        self.print_board(reveal=True)
                        print("Game Over! You hit a mine.")
                        break
                    if self.check_win():
                        self.print_board(reveal=True)
                        print("Congratulations! You won!")
                        break
                elif act == 'f':
                    self.toggle_flag(x, y)
                else:
                    raise ValueError
            except ValueError:
                print("Invalid input. Please enter 'r' or 'f' followed by two numbers.")

if __name__ == "__main__":
    game = Minesweeper()
    game.play()
