import pygame as pg
from validator import Validator
from alias import PlayerColor
from alias import GameDirection


class GUI:

    def __init__(self, WIDTH, HEIGHT, DIMENSION, SQ_SIZE, images, FPS, WHITE, BLACK, RED, SWIDTH, board):
        self._WIDTH = WIDTH
        self._HEIGHT = HEIGHT
        self._DIMENSION = DIMENSION  # dimensions of a checkers board are 8x8
        self._SQ_SIZE = SQ_SIZE  # size of one square in the board
        self._images = images
        self._FPS = FPS
        self._WHITE = WHITE
        self._BLACK = BLACK
        self._RED = RED
        self._SWIDTH = SWIDTH  # width of the score board window
        pg.display.set_caption("CHECKERS by team PINK")  # title of the game
        self._board = board
        self._clock = pg.time.Clock()
        pg.init()
        self._screen = pg.display.set_mode((self._WIDTH + self._SWIDTH, self._HEIGHT))
        self.load_images()
        self.menu_init(self._screen)

    def load_images(self):
        self._images["b"] = pg.image.load("data/b.png")  # loads image from the file
        self._images["b_transformed"] = pg.transform.scale(self._images["b"], (
            self._SQ_SIZE, self._SQ_SIZE))  # scales the image to the size of one square
        self._images["bb"] = pg.image.load("data/bb.png")
        self._images["bb_transformed"] = pg.transform.scale(self._images["bb"], (self._SQ_SIZE, self._SQ_SIZE))
        self._images["w"] = pg.image.load("data/w.png")
        self._images["w_transformed"] = pg.transform.scale(self._images["w"], (self._SQ_SIZE, self._SQ_SIZE))
        self._images["ww"] = pg.image.load("data/ww.png")
        self._images["ww_transformed"] = pg.transform.scale(self._images["ww"], (self._SQ_SIZE, self._SQ_SIZE))
        self._images["wood"] = pg.image.load("data/wood.png")
        self._images["home_screen"] = pg.image.load("data/home_screen.png")

    def draw_game_state(self, screen, validator, selectedSQ, board, valid_moves, players):
        self.draw_board(screen)  # draw squares on the board
        self.highlight_SQ(screen, validator, selectedSQ, board, valid_moves)  # highlights selected square
        self.draw_pieces(screen, self._board)  # draw pieces on the top of the squares
        self.draw_score(screen, players[0].get_score(), players[1].get_score())  # draw players score on the right window

    def draw_board(self, screen):
        screen.fill(self._BLACK)
        for row in range(self._DIMENSION):
            for col in range(row % 2, self._DIMENSION, 2):
                pg.draw.rect(screen, self._WHITE,
                             (col * self._SQ_SIZE, row * self._SQ_SIZE, self._SQ_SIZE, self._SQ_SIZE))

    def draw_pieces(self, screen, board):
        for row in range(self._DIMENSION):
            for col in range(self._DIMENSION):
                piece = board[row][col]
                if piece != "-":
                    screen.blit(self._images[piece+"_transformed"],
                                (col * self._SQ_SIZE, row * self._SQ_SIZE, self._SQ_SIZE, self._SQ_SIZE))

    def draw_score(self, screen, white_score, black_score):
        screen.blit(self._images["wood"], (self._WIDTH, 0, self._SWIDTH, self._HEIGHT))
        screen.blit(self._images["ww_transformed"], (self._WIDTH + 10, 0))
        screen.blit(self._images["bb_transformed"], (self._WIDTH + 140, 0))
        player_font = pg.font.Font("data/FROSTBITE.ttf", 30)
        quit_game = player_font.render("QUIT GAME", True, self._RED)
        screen.blit(quit_game, (self._WIDTH + 40, 750))

        score_font = pg.font.Font("data/FROSTBITE.ttf", 70)
        w_score = score_font.render("{%d}" % int(white_score), True, self._WHITE)
        b_score = score_font.render("{%d}" % int(black_score), True, self._WHITE)
        screen.blit(w_score, (self._WIDTH + 40, 120)) if white_score < 10 else screen.blit(w_score,
                                                                                           (self._WIDTH + 25, 120))
        screen.blit(b_score, (self._WIDTH + 165, 120)) if black_score < 10 else screen.blit(b_score,
                                                                                            (self._WIDTH + 150, 120))

    def menu_init(self, screen):
        path_to_font = "data/FROSTBITE.ttf"

        screen.blit(self._images["home_screen"], (0, 0, self._WIDTH, self._HEIGHT))
        screen.blit(self._images["wood"], (self._WIDTH, 0, self._SWIDTH, self._HEIGHT))
        screen.blit(self._images["ww"], (200, 265))
        screen.blit(self._images["bb"], (330, 300))

        head_line_font = pg.font.Font(path_to_font, 125)
        head_line = head_line_font.render("CHECKERS", True, self._RED)
        screen.blit(head_line, (15, 170))

        credit_font = pg.font.Font(path_to_font, 50)
        credit = credit_font.render("Created by team PINK", True, self._RED)
        screen.blit(credit, (100, 490))

        player_font = pg.font.Font(path_to_font, 23)
        one_player = player_font.render("Player vs PC", True, self._RED)
        screen.blit(one_player, (self._WIDTH + 33, 50))
        screen.blit(self._images["bb_transformed"], (self._WIDTH + 42, 90))
        screen.blit(self._images["ww_transformed"], (self._WIDTH + 100, 120))

        two_players = player_font.render("Player vs Player", True, self._RED)
        screen.blit(two_players, (self._WIDTH + 8, 230))
        screen.blit(self._images["bb_transformed"], (self._WIDTH + 42, 270))
        screen.blit(self._images["ww_transformed"], (self._WIDTH + 100, 300))

        load_game = player_font.render("LOAD GAME", True, self._RED)
        screen.blit(load_game, (self._WIDTH + 50, 700))

        quit_game = player_font.render("QUIT GAME", True, self._RED)
        screen.blit(quit_game, (self._WIDTH + 50, 750))

    def highlight_SQ(self, screen, validator, selectedSQ, board, valid_moves):
        if selectedSQ != () and selectedSQ[1] < 8:
            r = selectedSQ[0]
            c = selectedSQ[1]
            if board[r][c] != "-":
                s = pg.Surface((self._SQ_SIZE, self._SQ_SIZE))
                s.set_alpha(100)
                s.fill(pg.Color("blue"))
                screen.blit(s, (self._SQ_SIZE * c, self._SQ_SIZE * r))

                s.fill(pg.Color("yellow"))
                for move in valid_moves:
                    if selectedSQ == validator.get_rowcol_from_sq_string(move[0]):
                        screen.blit(s, (self._SQ_SIZE * validator.get_rowcol_from_sq_string(move[1])[1],
                                        self._SQ_SIZE * validator.get_rowcol_from_sq_string(move[1])[0]))

    def menu_run(self, status):
        while status:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    status = False

                elif event.type == pg.MOUSEBUTTONDOWN:
                    location = pg.mouse.get_pos()  # (x, y) position of mouse clicked

                    # Check if user click on the button for player vs PC
                    if self._WIDTH + 30 <= location[0] <= self._WIDTH + 215 and 45 <= location[1] <= 65:
                        # menu = False
                        return 0

                    # Check if user click on the button for player vs player
                    elif self._WIDTH + 7 <= location[0] <= self._WIDTH + 230 and 225 <= location[1] <= 235:
                        # menu = False
                        return 1

                    # Check if user click on the button for load game (not ready)
                    elif self._WIDTH + 48 <= location[0] <= self._WIDTH + 195 and 699 <= location[1] <= 709:
                        pass

                    # Check if user click on the button for quit game
                    elif self._WIDTH + 48 <= location[0] <= self._WIDTH + 195 and 749 <= location[1] <= 759:
                        status = False

            self._clock.tick(self._FPS)
            pg.display.flip()

    def run_game(self, validator, game, status, players):
        selectedSQ = ()  # last clicked square (row, col)
        finalSQ = ()
        valid_moves = []
        player_clicks = []  # most recent 2 clicks of the player

        while status:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    status = False

                elif event.type == pg.MOUSEBUTTONDOWN:
                    location = pg.mouse.get_pos()  # (x, y) position of mouse clicked
                    col = int(location[0] // self._SQ_SIZE)
                    row = int(location[1] // self._SQ_SIZE)
                    valid_moves = validator.find_all_valid_moves(
                        validator.translate_GUI_board_to_Validator_board(self._board), players[0].get_color())

                    # Check if user click on the button for quit game
                    if self._WIDTH + 39 <= location[0] <= self._WIDTH + 208 and 749 <= location[1] <= 770:
                        status = False

                    # for move in valid_moves:
                    #     if move[0] == Validator.get_sq_string_from_2D_board(row, col):
                    #         finalSQ[0] = Validator.get_rowcol_from_sq_string(move[-1])[0]
                    #         finalSQ[1] = Validator.get_rowcol_from_sq_string(move[-1])[1]

                    if selectedSQ == (row, col):  # selected square is the same as previous one
                        selectedSQ = ()  # deselect
                        player_clicks = []
                    else:
                        selectedSQ = (row, col)
                        player_clicks.append(selectedSQ)
                    if len(player_clicks) == 2:  # check if it was 2nd click
                        pass

            self.draw_game_state(self._screen, validator, selectedSQ, self._board, valid_moves, players)
            self._clock.tick(self._FPS)
            pg.display.flip()

        pg.quit()
