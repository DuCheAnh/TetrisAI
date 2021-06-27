#!/usr/bin/env python2
import copy
import time
import threading
import random
from model import Field
from tetris_ai import Ai
import pygame, sys
from gui import Gui

# The configuration
cell_size =    18
cols =        10
rows =        22
maxfps =     30
maxPiece = 500

colors = [
(0,   0,   0  ),
(255, 85,  85),
(100, 200, 115),
(120, 108, 245),
(255, 140, 50 ),
(50,  120, 52 ),
(146, 202, 73 ),
(150, 161, 218 ),
(35,  35,  35) # Helper color for background grid
]

# Define the shapes of the single parts
tetris_shapes = [
    [[1, 1, 1],
     [0, 1, 0]],

    [[0, 2, 2],
     [2, 2, 0]],

    [[3, 3, 0],
     [0, 3, 3]],

    [[4, 0, 0],
     [4, 4, 4]],

    [[0, 0, 5],
     [5, 5, 5]],

    [[6, 6, 6, 6]],

    [[7, 7],
     [7, 7]]
]

def rotate_clockwise(shape):
    return [ [ shape[y][x]
            for y in range(len(shape)) ]
        for x in range(len(shape[0]) - 1, -1, -1) ]

def check_collision(board, shape, offset):
    off_x, off_y = offset
    for cy, row in enumerate(shape):
        for cx, cell in enumerate(row):
            try:
                if cell and board[ cy + off_y ][ cx + off_x ]:
                    return True
            except IndexError:
                return True
    return False

def remove_row(board, row):
    del board[row]
    return [[0 for i in range(cols)]] + board

def join_matrixes(mat1, mat2, mat2_off):
    off_x, off_y = mat2_off
    for cy, row in enumerate(mat2):
        for cx, val in enumerate(row):
            mat1[cy+off_y-1    ][cx+off_x] += val
    return mat1

def new_board():
    board = [ [ 0 for x in range(cols) ]
            for y in range(rows) ]
    #board += [[ 1 for x in xrange(cols)]]
    return board

class TetrisApp(object):
    def __init__(self, playWithUI,seed):
        self.width = cell_size*(cols+6)
        self.height = cell_size*rows
        self.rlim = cell_size*cols
        self.nbPiece = 0
        if seed>=0:
            random.seed(seed)
        self.next_stone = tetris_shapes[random.randint(0, len(tetris_shapes)-1)]
        self.playWithUI = playWithUI
        self.fast_mode = True
        if playWithUI:
            self.gui = Gui()
            self.fast_mode = False
        self.init_game()

    def new_stone(self):
        self.stone = self.next_stone[:]
        self.next_stone = tetris_shapes[random.randint(0, len(tetris_shapes)-1)]
        self.stone_x = int(cols / 2 - len(self.stone[0])/2)
        self.stone_y = 0
        self.nbPiece += 1
        self.computed = False

        if check_collision(self.board,
                           self.stone,
                           (self.stone_x, self.stone_y)):
            self.gameover = True

    def init_game(self):
        self.board = new_board()
        self.new_stone()
        self.level = 1
        self.score = 0
        self.lines = 0

    def add_cl_lines(self, n):
        linescores = [0, 40, 100, 300, 1200]
        self.lines += n
        self.score += linescores[n] * self.level
        if self.lines >= self.level*6:
            self.level += 1

    def move(self, delta_x):
        if not self.gameover and not self.paused:
            new_x = self.stone_x + delta_x
            if new_x < 0:
                new_x = 0
            if new_x > cols - len(self.stone[0]):
                new_x = cols - len(self.stone[0])
            if not check_collision(self.board,
                                   self.stone,
                                   (new_x, self.stone_y)):
                self.stone_x = new_x

    def drop(self, manual):
        if not self.gameover and not self.paused:
            self.score += 1 if manual else 0
            self.stone_y += 1
            if check_collision(self.board,
                               self.stone,
                               (self.stone_x, self.stone_y)):
                self.board = join_matrixes(
                  self.board,
                  self.stone,
                  (self.stone_x, self.stone_y))
                self.new_stone()
                cleared_rows = 0

                for i, row in enumerate(self.board):
                    if 0 not in row:
                        self.board = remove_row(
                          self.board, i)
                        cleared_rows += 1
                self.add_cl_lines(cleared_rows)
                return True
        return False

    def insta_drop(self):
        if not self.gameover and not self.paused:
            while(not self.drop(True)):
                pass

    def rotate_stone(self):
        if not self.gameover and not self.paused:
            new_stone = rotate_clockwise(self.stone)
            if not check_collision(self.board,
                                   new_stone,
                                   (self.stone_x, self.stone_y)):
                self.stone = new_stone

    def toggle_pause(self):
        self.paused = not self.paused

    def start_game(self):
        if self.gameover:
            self.init_game()
            self.gameover = False

    def quit(self):
        if self.playWithUI:
            self.gui.center_msg("Exiting...")
            pygame.display.update()
        sys.exit()

    def speed_up(self):
        self.fast_mode = not self.fast_mode
        if self.fast_mode:
            pygame.time.set_timer(pygame.USEREVENT+1, 2000)
            self.insta_drop()
        else:
            pygame.time.set_timer(pygame.USEREVENT+1, 25)

    def executes_moves(self, moves):
        key_actions = {
            'ESCAPE':    self.quit,
            'LEFT':        lambda:self.move(-1),
            'RIGHT':    lambda:self.move(+1),
            'DOWN':        lambda:self.drop(True),
            'UP':        self.rotate_stone,
            'p':        self.toggle_pause,
            'SPACE':    self.start_game,
            'RETURN':    self.insta_drop
        }
        for action in moves:
            key_actions[action]()

        if self.fast_mode:
            self.insta_drop()


    def run(self, weights, limitPiece):
        self.gameover = False
        self.paused = False

        #dont_burn_my_cpu = pygame.time.Clock()
        while 1:

            if self.nbPiece >= limitPiece and limitPiece > 0:
                self.gameover = True

            if self.playWithUI:
                self.gui.update(self)

            if self.gameover:
                return self.lines*1000 + self.nbPiece

            if not self.computed:
                self.computed = True
                Ai.choose(self.board, self.stone, self.next_stone, self.stone_x, weights, self, True)

            if self.playWithUI:
                for event in pygame.event.get():
                    if event.type == pygame.USEREVENT+1:
                        self.drop(False)
                    elif event.type == pygame.QUIT:
                            self.quit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == eval("pygame.K_s"):
                            self.speed_up()
                        elif event.key == eval("pygame.K_p"):
                            self.toggle_pause()

            #dont_burn_my_cpu.tick(maxfps)


if __name__ == '__main__':
    weights=[-0.510066,0.76606,-0.35663,-0.184483]
    seed=1
    piece_limit=200
    # weights=[-0.73796594,  1.71730086, -2.15707346, -0.89728016]
    result = TetrisApp(True,seed).run(weights, piece_limit)
    print(result)
