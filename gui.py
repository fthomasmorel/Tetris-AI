#!/usr/bin/env python2
import copy
import time
from random import randrange as rand
from field import Field
from ai import Ai
import pygame, sys

# The configuration
cell_size =    18
cols =        10
rows =        22
maxfps =     30
time =     2000
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

class Gui(object):
    def __init__(self):
        pygame.init()
        pygame.key.set_repeat(250,25)
        self.width = cell_size*(cols+6)
        self.height = cell_size*rows
        self.rlim = cell_size*cols
        self.bground_grid = [[ 8 if x%2==y%2 else 0 for x in xrange(cols)] for y in xrange(rows)]

        self.default_font =  pygame.font.Font(
            pygame.font.get_default_font(), 12)

        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.event.set_blocked(pygame.MOUSEMOTION)
        pygame.time.set_timer(pygame.USEREVENT+1, time)

    def disp_msg(self, msg, topleft):
        x,y = topleft
        for line in msg.splitlines():
            self.screen.blit(
                self.default_font.render(
                    line,
                    False,
                    (255,255,255),
                    (0,0,0)),
                (x,y))
            y+=14

    def center_msg(self, msg):
        for i, line in enumerate(msg.splitlines()):
            msg_image =  self.default_font.render(line, False,
                (255,255,255), (0,0,0))

            msgim_center_x, msgim_center_y = msg_image.get_size()
            msgim_center_x //= 2
            msgim_center_y //= 2

            self.screen.blit(msg_image, (
              self.width // 2-msgim_center_x,
              self.height // 2-msgim_center_y+i*22))

    def draw_matrix(self, matrix, offset):
        off_x, off_y  = offset
        for y, row in enumerate(matrix):
            for x, val in enumerate(row):
                if val:
                    pygame.draw.rect(self.screen,colors[val],
                        pygame.Rect(
                            (off_x+x) *
                              cell_size,
                            (off_y+y) *
                              cell_size,
                            cell_size,
                            cell_size),0)

    def update(self, tetris):
        self.screen.fill((0,0,0))
        if tetris.gameover:# or self.nbPiece >= maxPiece:
            self.center_msg("""Game Over!\nYour score: %dPress space to continue""" % tetris.score)
        else:
            if tetris.paused:
                self.center_msg("Paused")
            else:
                pygame.draw.line(self.screen,
                    (255,255,255),
                    (self.rlim+1, 0),
                    (self.rlim+1, self.height-1))
                self.disp_msg("Next:", (
                    self.rlim+cell_size,
                    2))
                self.disp_msg("Score: %d\n\nLevel: %d\n\nLines: %d" % (tetris.score, tetris.level, tetris.lines),
                    (self.rlim+cell_size, cell_size*5))
                self.draw_matrix(self.bground_grid, (0,0))
                self.draw_matrix(tetris.board, (0,0))
                self.draw_matrix(tetris.stone, (tetris.stone_x, tetris.stone_y))
                self.draw_matrix(tetris.next_stone, (cols+1,2))
        pygame.display.update()
