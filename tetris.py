#!/usr/bin/env python2
import copy
import time
import threading
from random import randrange as rand
from field import Field
from ai import Ai
import pygame, sys

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
            for y in xrange(len(shape)) ]
        for x in xrange(len(shape[0]) - 1, -1, -1) ]

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
    return [[0 for i in xrange(cols)]] + board

def join_matrixes(mat1, mat2, mat2_off):
    off_x, off_y = mat2_off
    for cy, row in enumerate(mat2):
        for cx, val in enumerate(row):
            mat1[cy+off_y-1    ][cx+off_x] += val
    return mat1

def new_board():
    board = [ [ 0 for x in xrange(cols) ]
            for y in xrange(rows) ]
    #board += [[ 1 for x in xrange(cols)]]
    return board

class TetrisApp(object):
    def __init__(self):
        pygame.init()
        pygame.key.set_repeat(250,25)
        self.width = cell_size*(cols+6)
        self.height = cell_size*rows
        self.rlim = cell_size*cols
        self.bground_grid = [[ 8 if x%2==y%2 else 0 for x in xrange(cols)] for y in xrange(rows)]
        self.nbPiece = 0

        self.default_font =  pygame.font.Font(
            pygame.font.get_default_font(), 12)

        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.event.set_blocked(pygame.MOUSEMOTION) # We do not need
                                                     # mouse movement
                                                     # events, so we
                                                     # block them.
        self.next_stone = tetris_shapes[rand(len(tetris_shapes))]
        self.init_game()

    def new_stone(self):
        self.stone = self.next_stone[:]
        self.next_stone = tetris_shapes[rand(len(tetris_shapes))]
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

        pygame.time.set_timer(pygame.USEREVENT+1, 2000)

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

    def add_cl_lines(self, n):
        linescores = [0, 40, 100, 300, 1200]
        self.lines += n
        self.score += linescores[n] * self.level
        if self.lines >= self.level*6:
            self.level += 1
            newdelay = 100-50*(self.level-1)
            newdelay = 100 if newdelay < 100 else newdelay
            pygame.time.set_timer(pygame.USEREVENT+1, 2000)

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
    def quit(self):
        self.center_msg("Exiting...")
        pygame.display.update()
        sys.exit()

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


    def run(self, weights):
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

        self.gameover = False
        self.paused = False

        dont_burn_my_cpu = pygame.time.Clock()
        while 1:
            self.screen.fill((0,0,0))
            if self.gameover:# or self.nbPiece >= maxPiece:
                print(self.lines)
                #self.center_msg("""Game Over!\nYour score: %dPress space to continue""" % self.score)
                return self.score#*1000 + self.nbPiece
            else:
                if self.paused:
                    self.center_msg("Paused")
                else:
                    pygame.draw.line(self.screen,
                        (255,255,255),
                        (self.rlim+1, 0),
                        (self.rlim+1, self.height-1))
                    self.disp_msg("Next:", (
                        self.rlim+cell_size,
                        2))
                    self.disp_msg("Score: %d\n\nLevel: %d\n\nLines: %d" % (self.score, self.level, self.lines),
                        (self.rlim+cell_size, cell_size*5))
                    self.draw_matrix(self.bground_grid, (0,0))
                    self.draw_matrix(self.board, (0,0))
                    self.draw_matrix(self.stone, (self.stone_x, self.stone_y))
                    self.draw_matrix(self.next_stone, (cols+1,2))
            pygame.display.update()

            if not self.computed:
                self.computed = True
                Ai.choose(self.board, self.stone, self.next_stone, self.stone_x, weights, self)
                #thread = threading.Thread(target=Ai.choose, args=(self.board, self.stone, self.next_stone, self.stone_x, weights, self))
                #thread.start()
                #series = Ai.choose(self.board, self.stone, self.next_stone, self.stone_x, weights, self)

            for event in pygame.event.get():
                if event.type == pygame.USEREVENT+1:
                    self.drop(False)
                elif event.type == pygame.QUIT:
                    self.quit()
                elif event.type == pygame.KEYDOWN:
                    for key in key_actions:
                        if event.key == eval("pygame.K_"+key):
                            key_actions[key]()

            dont_burn_my_cpu.tick(maxfps)
            # print(" ")
            # for line in self.board:
            #     print(line)

if __name__ == '__main__':
    #weights = [1.9843171562430688, -3.1638758897496073, -2.7194142782664126, -3.0205617435714953, -0.06426633888614375, -0.19418460826802197, -2.9317670226921186, -5.739889690415672, 0.5965420392539678, 4.6930416502908034, -14.32678214571752, 10.411945507867074, -7.877896947646873, -22.306553682279766, -11.469566973122774, -2.654205113501031, -4.3192240963506086, -3.7489706294820797] #15658 lignes #1h
    #weights = [1.3448679137809203, -1.7480884590386485, -1.1908598926963248, -3.8690712858704637, -0.9408694086802846, -1.4234929700958472, -2.86346255688619, -3.8310120698527776, 0.8866909521249849, 5.372087947093633, -14.511195282556155, 6.900681043271475, -7.515477057301684, -21.065545748457037, -10.295009323508955, -2.559387336241411, -2.3673939737607284, -2.324706781161897]
    #weights = [-0.1548175086588222, -2.9381109764551376, -3.847493329020864, -0.7742432704418234, -4.402100959435273, -3.253421200722233, -4.207450411038958, -2.8762130084453954, -7.00348096894661, 2.9439669498872014, -21.467210864748694, -3.8711025276246644, -2.2504104081197385, -4.102063738379772, -0.7693041487234451, -5.630869324348871, -4.589809221543835, -6.872027720243644, 0.40478995674799056, -5.471599470575599, 1.8117768841911979, -3.3821091256324918, -4.465338298999946, -7.412932103744623, -2.1763647806260416, -6.062923271090441, -2.994847720957777, -2.654005757780462, -4.246432891377617, -5.57578507286433, 11.295230103694601, -2.413335297197231, -7.8271099220105125, 4.045849115776209] #19709 lignes
    #weights = [0.2977064921051234, -3.0059523318579124, -3.4672303365124733, -2.156125483489782, -6.752952117444787, 0.5289009458161702, -6.0903111107166845, -3.1012719801035553, -9.329380814619915, 2.5717195590709365, -21.352160995916222, -5.064092719415802, 0.07118535209028343, -2.0606879835962455, 0.19449485660703125, -8.035926155271493, -7.731597009289003, -3.34867057477323, 2.873551464954007, -16.507622339334606, -2.3513881677091844, -0.17170468935040661, -3.22658891363458, -7.6149738540685625, -2.959813784728351, -4.865498444303364, -4.67279674095317, -2.3584149646652186, -3.0841140015948447, -3.693579159565839, 17.253838886071968, -3.526777754600351, -6.747937005387159, 9.067206938471001] #2534 lignes
    weights = [0.39357083734159515, -1.8961941343266449, -5.107694873375318, -3.6314963941589093, -2.9262681134021786, -2.146136640641482, -7.204192964669836, -3.476853402227247, -6.813002842291903, 4.152001386170861, -21.131715861293525, -10.181622180279133, -5.351108175564556, -2.6888972099986956, -2.684925769670947, -4.504495386829769, -7.4527302422826, -6.3489634714511505, -4.701455626343827, -10.502314845278828, 0.6969259450910086, -4.483319180395864, -2.471375907554622, -6.245643268054767, -1.899364785170105, -5.3416512085013395, -4.072687054171711, -5.936652569831475, -2.3140398163110643, -4.842883337741306, 17.677262456993276, -4.42668539845469, -6.8954976464473585, 4.481308299774875] #21755 lignes
    result = TetrisApp().run(weights)
    print(result)
