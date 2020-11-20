##!/usr/bin/env python3

import math

import pygame

from primitives import GameObject, Pose
import constants as c
from player import Player

class HighScoreColumn(GameObject):
    def __init__(self, game, parent, get_data, align=c.LEFT, width=100, small_font=False):
        super().__init__(game)
        self.align = align
        self.width = width
        self.small_font = small_font

        # get_data takes in a player and returns data for the column as string
        self.get_data = get_data
        # self.surface = self.get_column_surface()

class HighScoreRow(GameObject):
    def __init__(self, game, player, columns = None, row_number=0):
        super().__init__(game)
        self.player = player
        self.columns = columns if columns is not None else []
        self.row_number = row_number
        self.wiggle_radius = 3
        self.wiggle_offset = -self.row_number * 0.6
        self.wiggle_frequency = 0.7
        self.debug_lines = False
        self.age = 0
        self.tile = self.get_tile()
        self.tile_shadow.fill(c.BLACK)
        self.tile_shadow.set_alpha(80)

    def height(self):
        return self.tile.get_height()

    def tile_color(self):
        if self.row_number%2:
            return c.SCORE_ODD_COLOR
        else:
            return c.SCORE_EVEN_COLOR

    def get_piece(self, player, column):
        line_text = column.get_data(player)
        color = c.BLACK
        if line_text and line_text[0] == "@":
            line_text = line_text[1:]
            color = player.color
        font = self.game.scoreboard_font
        if column.small_font:
            font = self.game.small_scoreboard_font
        text = font.render(line_text, 1, color)
        text_white = font.render(line_text, 1, c.WHITE)
        surf = pygame.Surface((column.width, c.SCORE_ROW_HEIGHT - c.SCORE_TILE_PADDING*2))
        surf.fill(self.tile_color())
        surf.set_colorkey(self.tile_color())
        if column.align is c.LEFT or text.get_width() > surf.get_width() - c.SCORE_ROW_PADDING*2:
            x = c.SCORE_ROW_PADDING
        elif column.align is c.RIGHT:
            x = surf.get_width() - text.get_width() - c.SCORE_ROW_PADDING
        else:
            x = surf.get_width()//2 - text.get_width()//2
        if player.name is c.EMPTY:
            text.set_alpha(128)
            text_white.set_alpha(0)
        else:
            text.set_alpha(128)
        white_offset = 1
        offsets = c.TEXT_BLIT_OFFSETS if player.name is not c.EMPTY else [c.CENTER]
        for offset in offsets:
            surf.blit(text, (x + offset[0], surf.get_height()//2 - text.get_height()//2 + offset[1]))
        surf.blit(text_white, (x, surf.get_height()//2 - text.get_height()//2 - white_offset))
        if player.name is c.EMPTY:
            black = pygame.Surface((surf.get_width(), surf.get_height()))
            black.set_alpha(75)
            surf.blit(black, (0, 0))
        if self.debug_lines:
            pygame.draw.rect(surf, c.RED, (0, 0, surf.get_width(), surf.get_height()), width=1)
        return surf

    def get_row_surface(self, player):
        pieces = [self.get_piece(player, column) for column in self.columns]
        width = sum([piece.get_width() for piece in pieces])
        surf = pygame.Surface((width, c.SCORE_ROW_HEIGHT - 2*c.SCORE_TILE_PADDING))
        surf.fill(self.tile_color())
        x = 0
        for piece in pieces:
            surf.blit(piece, (x, 0))
            x += piece.get_width()
        self.tile_shadow = surf.copy()
        return surf

    def get_tile(self):
        return(self.surf_to_tile(self.get_row_surface(self.player)))

    def surf_to_tile(self, surface):
        tile = pygame.Surface((surface.get_width() + c.SCORE_TILE_PADDING * 2, c.SCORE_ROW_HEIGHT))
        tile.fill((50, 80, 110))
        tile.set_colorkey((50, 80, 110))
        pygame.draw.rect(tile,
                        c.GRAY,
                        (c.SCORE_TILE_PADDING,
                        c.SCORE_TILE_PADDING,
                        tile.get_width() - c.SCORE_TILE_PADDING * 2,
                        tile.get_height() - c.SCORE_TILE_PADDING * 2))
        x = tile.get_width()//2 - surface.get_width()//2
        y = tile.get_height()//2 - surface.get_height()//2
        tile.blit(surface, (x, y))
        return tile

    def update(self, dt, events):
        self.age += dt

    def draw(self, surface, offset=(0, 0)):
        wx = math.sin(math.pi * 2 * self.wiggle_frequency * self.age + self.wiggle_offset) * self.wiggle_radius
        wy = -math.cos(math.pi * 2 * self.wiggle_frequency * self.age + self.wiggle_offset) * self.wiggle_radius
        x = offset[0] - self.tile.get_width()//2 + wx
        y = offset[1] - self.tile.get_height()//2 + wy
        if not self.player.name is c.EMPTY:
            surface.blit(self.tile_shadow, (x+9, y+11))
        surface.blit(self.tile, (x, y))

class HighScoreTable(GameObject):
    def __init__(self, game):
        super().__init__(game)
        self.pose = Pose((c.WINDOW_WIDTH//2, c.WINDOW_HEIGHT//2), 0)
        hours_to_display = 480
        snapshot_dict = self.game.scoreboard.get_total_by_player(hours_to_display)
        self.rows = 10
        self.last_snapshot = self.game.last_snapshot
        self.snapshot = self.dict_to_sorted_list(snapshot_dict)
        self.game.last_snapshot = self.snapshot
        self.player_names = [item[0] for item in self.snapshot[:self.rows]]
        self.player_names += [c.EMPTY for i in range(self.rows - len(self.player_names))]
        self.add_missing_players()
        self.columns = []
        self.placing_calls = 0
        self.assemble_table()
        players = [self.game.players[name] for name in self.player_names]
        self.rows = [HighScoreRow(self.game, player, columns=self.columns, row_number=i) for i, player in enumerate(players)]

    def add_missing_players(self):
        if c.EMPTY not in self.game.players:
            self.game.players[c.EMPTY] = Player(self.game, c.EMPTY, c.MEDIUM_DARK_GRAY)
        for player_name in self.player_names:
            if player_name not in self.game.players:
                self.game.players[player_name] = Player(self.game, player_name)

    def placing(self, player):
        return self.player_names.index(player.name) + 1

    def render_placing(self, player):
        self.placing_calls += 1
        return f"#{self.placing_calls}"

    def player_to_score(self, player):
        if player.name == c.EMPTY:
            return 0
        placing = self.placing(player)
        return self.snapshot[placing - 1][1].score

    def rank_change(self, player):
        if player.name == c.EMPTY:
            return 0
        if self.last_snapshot is None:
            return 0
        else:
            last_players = [item[0] for item in self.last_snapshot]
            cur_players = [item[0] for item in self.snapshot]
            cur_index = cur_players.index(player.name)
            if not player.name in last_players:
                return len(cur_players) - cur_index
            last_index = last_players.index(player.name)
            return cur_index - last_index

    def score_increase(self, player):
        if player.name == c.EMPTY:
            return ""
        if self.last_snapshot is None:
            return "-"
        else:
            last_players = [item[0] for item in self.last_snapshot]
            cur_players = [item[0] for item in self.snapshot]
            cur_index = cur_players.index(player.name)
            if not player.name in last_players:
                increase = self.snapshot[cur_index][1].score
            else:
                last_index = last_players.index(player.name)
                increase = self.snapshot[cur_index][1].score - self.last_snapshot[last_index][1].score
            increase = int(increase)
            plus = "+" if increase >= 0 else ""
            return f"{plus}{increase}"

    def assemble_table(self):
        self.columns = [
            HighScoreColumn(self.game, self, lambda x: f"{self.render_placing(x)}", align=c.CENTER, width=50),
            HighScoreColumn(self.game, self, lambda x: f"{x.name}", align=c.CENTER, width=400),
            HighScoreColumn(self.game, self, lambda x: f"{self.score_increase(x)}", align=c.CENTER, width=70, small_font=True),
            HighScoreColumn(self.game, self, lambda x: f"{int(self.player_to_score(x))}", align=c.RIGHT, width=120)
        ]

    @staticmethod
    def dict_to_sorted_list(d):
        l = [(key, d[key]) for key in d]
        l.sort(reverse=True, key=lambda x: x[1].score)
        return l

    def update(self, dt, events):
        for row in self.rows:
            row.update(dt, events)

    def draw(self, surface, offset=(0, 0)):
        height = c.SCORE_ROW_HEIGHT * len(self.rows) + 2 * c.SCORE_TABLE_PADDING
        width = self.rows[0].tile.get_width() + 2 * c.SCORE_TABLE_PADDING
        x = offset[0] + self.pose.x
        y = offset[1] + self.pose.y - (c.SCORE_ROW_HEIGHT * len(self.rows))//2 + c.SCORE_ROW_HEIGHT//2
        pygame.draw.rect(surface, c.SCORE_TABLE_COLOR, (x - width//2, y - c.SCORE_TABLE_PADDING - c.SCORE_ROW_HEIGHT//2, width, height))
        for row in self.rows:
            row.draw(surface, (x, y))
            y += row.height()
