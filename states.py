import models


class GameState(object):
    def __init__(self, game):
        self.game = game

    def is_in_game(self):
        raise NotImplemented()

    def end_turn_allowed(self):
        if not self.is_in_game():
            return False
        raise NotImplemented()


class GameStatePreGame(GameState):
    def is_in_game(self):
        return False


class GameStateInGame(GameState):
    def is_in_game(self):
        return True

    def end_turn_allowed(self):
        return False


class GameStateTurnStart(GameStateInGame):
    def end_turn_allowed(self):
        return False


class GameStateRolled(GameStateInGame):
    def end_turn_allowed(self):
        return True


class GameStatePostGame(GameState):
    def is_in_game(self):
        return False


##
# Abstract state class to inherit concrete states from
#
class BoardState(object):
    def __init__(self, board):
        self.board = board

    def hex_change_allowed(self):
        return self.hex_number_change_allowed() and self.hex_type_change_allowed()

    def cycle_hex_type(self, tile_id):
        if self.hex_type_change_allowed():
            tile = self.board.tiles[tile_id - 1]
            next_idx = (list(models.Terrain).index(tile.terrain) + 1) % len(models.Terrain)
            next_terrain = list(models.Terrain)[next_idx]
            tile.terrain = next_terrain

    def cycle_hex_number(self, tile_id):
        if self.hex_number_change_allowed():
            tile = self.board.tiles[tile_id - 1]
            next_idx = (list(models.HexNumber).index(tile.number) + 1) % len(models.HexNumber)
            next_hex_number = list(models.HexNumber)[next_idx]
            tile.number = next_hex_number

    ##
    # Begin methods to implement in concrete states
    #
    def hex_number_change_allowed(self):
        raise NotImplemented()

    def hex_type_change_allowed(self):
        raise NotImplemented()


class BoardStateModifiable(BoardState):
    def hex_number_change_allowed(self):
        return True

    def hex_type_change_allowed(self):
        return True


class BoardStateLocked(BoardState):
    def hex_number_change_allowed(self):
        return False

    def hex_type_change_allowed(self):
        return False
