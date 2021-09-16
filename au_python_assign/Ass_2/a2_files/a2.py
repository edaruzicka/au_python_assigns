EMPTY_TILE = "tile"
START_PIPE = "start"
END_PIPE = "end"
LOCKED_TILE = "locked"

SPECIAL_TILES = {
    "S": START_PIPE,
    "E": END_PIPE,
    "L": LOCKED_TILE
}

PIPES = {
    "ST": "straight",
    "CO": "corner",
    "CR": "cross",
    "JT": "junction-t",
    "DI": "diagonals",
    "OU": "over-under"
}

### add code here ###

SIDES = {
    0: "N",
    1: "E",
    2: "S",
    3: "W",
    }

class Tile:
    """
    Representation of a tile.
    """
    def __init__(self, name, selectable = True):
        """
        Construct a tile with an assigned name and set if the tile should be selectable.

        Parameters:
            name (str): The name of the tile.
            selectable(bool): If true, the pipe can be selected and manipulated with.
        """
        self._name = name
        self._selectable = selectable
        self._id = "tile"
    
    def get_name(self):
        """
        (str): The name of the tile.
        """
        return self._name

    def get_id(self):
        """
        (str): The id of the tile.
        """
        return self._id
    
    def set_select(self, selectable):
        """
        Set, if a tile should be selectable; if it should be manipulated with.

        Parameters:
            selectable(bool): If true, the pipe can be selected and manipulated with.
        """
        self._selectable = selectable

    def can_select(self):
        """
        (bool): True if the tile is selectable.
        """
        if self._selectable == True:
            return True
        else:
            return False
    
    def __str__(self):
        str_repre = "Tile('" + self.get_name() + "', " + str(self.can_select()) + ")"
        return str_repre
    
    def __repr__(self):
        return str(self)


class Pipe(Tile):
    """
    Representation of a pipe.
    """
    def __init__(self, name, orientation = 0, selectable = True):
        """
        Construct a pipe with an assigned name, orientation
        and set if the tile should be selectable.

        Parameters:
            name (str): The name of the tile.
            orientation (int): Orientation of a tile. Must be in range [0, 3].
            selectable(bool): If true, the pipe can be selected and manipulated with.
        """
        super().__init__(name, selectable)

        if orientation not in range(0, 4):
            raise ValueError("Orientation must be in range [0, 3]")
        self._orientation = orientation
        self._id = "pipe"
        
    def get_connected(self, side):
        """
        Returns a list of all sides that are connected to the given side.
        Different calculation (range()) depending on the type of a pipe.

        Parameters:
            side(str): Given side. ‘N’, ‘S’, ‘E’ or ‘W’.
        
        Returns:
            (list<str>): List of all sides that are connected to the given side.
        """
        connected_sides = []
        connected_sides_2 = [] # second list needed for diagonals and over-under pipes
        name = self.get_name()
        ori = self.get_orientation()

        # get all connected sides
        if name == "straight":
            for x in range(ori, ori+4, 2):
                connected_sides.append(SIDES[x%4])
        elif name == "corner":
            for x in range(ori, ori+2, 1):
                connected_sides.append(SIDES[x%4])
        elif name == "cross":
            for x in range(ori, ori+4, 1):
                connected_sides.append(SIDES[x%4])
        elif name == "junction-t":
            for x in range(ori+1, ori+4, 1):
                connected_sides.append(SIDES[x%4])
        elif name == "diagonals":
            for x in range(ori, ori+2, 1):
                connected_sides.append(SIDES[x%4])
            for x in range(ori+2, ori+4, 1):
                connected_sides_2.append(SIDES[x%4])
        elif name == "over-under":
            for x in range(ori, ori+4, 2):
                connected_sides.append(SIDES[x%4])
            for x in range(ori+1, ori+5, 2):
                connected_sides_2.append(SIDES[x%4])
                
        # if desired side is in connected sides, remove side from the list to be printed, else there are no connected sides
        if side in connected_sides:
            connected_sides.remove(side)
            return connected_sides
        elif side in connected_sides_2:
            connected_sides = connected_sides_2
            connected_sides.remove(side)
            return connected_sides
        else:
            connected_sides = []
            return connected_sides

    def rotate(self, direction):
        """
        Rotates a pipe one turn, changing orientation, based on the specified direction.

        Parameters:
            direction(str): A positive direction implies clockwise rotation, 
                            and a negative direction implies counter-clockwise rotation 
                            and 0 means no rotation.
        """
        if self._orientation == 0 and direction < 0:
            self._orientation = 3
        elif self._orientation == 3 and direction > 0:
            self._orientation = 0
        else:
            self._orientation += direction

    def get_orientation(self):
        """
        (int): Orientation of a tile. Must be in range [0, 3].
        """
        return self._orientation

    def __str__(self):
        str_repre = "Pipe('" + self.get_name() + "', " + str(self.get_orientation()) + ")"        
        return str_repre

    def __repr__(self):
        return str(self)


class SpecialPipe(Pipe):
    """
    Abstract representation of a special pipe.
    """
    def __init__(self, name = "SpecialPipe", orientation = 0, selectable = False):
        """
        Construct a special pipe with an assigned name, orientation
        and set if the tile should be selectable.

        Parameters:
            name (str): The name of the tile.
            orientation (int): Orientation of a tile. Must be in range [0, 3].
            selectable(bool): If true, the pipe can be selected and manipulated with.
        """
        super().__init__(name, orientation, selectable)
        self._id = "special_pipe"

    def __str__(self):
        str_repre = self.__class__.__name__ + "(" + str(self.get_orientation()) + ")"
        return str_repre

    def __repr__(self):
        return str(self)


class StartPipe(SpecialPipe):
    """
    Representation of a start pipe.
    """
    def __init__(self, orientation = 0, name = "start", selectable = False):
        """
        Construct a start pipe with an assigned name, orientation
        and set if the tile should be selectable.

        Parameters:
            name (str): The name of the tile.
            orientation (int): Orientation of a tile. Must be in range [0, 3].
            selectable(bool): If true, the pipe can be selected and manipulated with.
        """
        super().__init__(name, orientation, selectable)
    
    def get_connected(self, side=None):
        """
        Returns a list of all sides that are connected to the given side.

        Parameters:
            side(str): Given side. ‘N’, ‘S’, ‘E’, ‘W’.
        
        Returns:
            (list<str>): List of all sides that are connected to the given side.
        """
        conect_sides = []
        if self.get_orientation() == 0:
            conect_sides.append("N")
        elif self.get_orientation() == 1:
            conect_sides.append("E")
        elif self.get_orientation() == 2:
            conect_sides.append("S")
        elif self.get_orientation() == 3:
            conect_sides.append("W")

        return conect_sides


class EndPipe(SpecialPipe):
    """
    Representation of an end pipe.
    """
    def __init__(self, orientation = 0, name = "end", selectable = False):
        """
        Construct an end pipe with an assigned name, orientation
        and set if the tile should be selectable.

        Parameters:
            name (str): The name of the tile.
            orientation (int): Orientation of a tile. Must be in range [0, 3].
            selectable(bool): If true, the pipe can be selected and manipulated with.
        """
        super().__init__(name, orientation, selectable)

    def get_connected(self, side=None):
        """
        Returns a list of all sides that are connected to the given side.

        Parameters:
            side(str): Given side. ‘N’, ‘S’, ‘E’, ‘W’.
        
        Returns:
            (list<str>): List of all sides that are connected to the given side.
        """
        conect_sides = []
        if self.get_orientation() == 0:
            conect_sides.append("S")
        elif self.get_orientation() == 1:
            conect_sides.append("W")
        elif self.get_orientation() == 2:
            conect_sides.append("N")
        elif self.get_orientation() == 3:
            conect_sides.append("E")

        return conect_sides


class PipeGame:
    """
    A game of Pipes.
    """
    def __init__(self, game_file='game_1.csv'):
        """
        Construct a game of Pipes from a file name.

        Parameters:
            game_file (str): name of the game file.
        """
        #########################COMMENT THIS SECTION OUT WHEN DOING load_file#######################
        self.board_layout = [[Tile('tile', True), Tile('tile', True), Tile('tile', True), Tile('tile', True), \
        Tile('tile', True), Tile('tile', True)], [StartPipe(1), Tile('tile', True), Tile('tile', True), \
        Tile('tile', True), Tile('tile', True), Tile('tile', True)], [Tile('tile', True), Tile('tile', True), \
        Tile('tile', True), Pipe('junction-t', 0, False), Tile('tile', True), Tile('tile', True)], [Tile('tile', True), \
        Tile('tile', True), Tile('tile', True), Tile('tile', True), Tile('locked', False), Tile('tile', True)], \
        [Tile('tile', True), Tile('tile', True), Tile('tile', True), Tile('tile', True), EndPipe(3), \
        Tile('tile', True)], [Tile('tile', True), Tile('tile', True), Tile('tile', True), Tile('tile', True), \
        Tile('tile', True), Tile('tile', True)]]

        self.playable_pipes = {'straight': 1, 'corner': 1, 'cross': 1, 'junction-t': 1, 'diagonals': 1, 'over-under': 1}
        #########################COMMENT THIS SECTION OUT WHEN DOING load_file#######################

        ### add code here ###
        self.end_pipe_positions()

    def get_board_layout(self):
        """
        list<list<Tile, ...>>: The board layout of a current game.
        """
        return self.board_layout

    def get_playable_pipes(self):
        """
        dict<str:int>: Distionary of playable pipes in a current game.
        """
        return self.playable_pipes

    def change_playable_amount(self, pipe_name, number):
        """
        Add the quantity of playable pipes of type specified 
        by pipe_name to number (in the selection panel).

        Parameters:
            pipe_name (str): Name of the pipe.
            number (int): Number by which the specified playable pipe should be increased.
        """
        self.playable_pipes[pipe_name] += number

    def get_pipe(self, position):
        """
        Returns the Pipe at the position or the tile 
        if there is no pipe at that position.

        Parameters:
            position (tuple<int, int>): A tuple of row and number, representing the position.

        Returns:
            (Pipe|Tile): A pipe or a tile at a specified position.
        """
        pipe = self.board_layout[position[0]][position[1]]
        return pipe

    def set_pipe(self, pipe, position):
        """
        Place the specified pipe at the given position (row, col) in the game board.

        Parameters:
            position (tuple<int, int>): A tuple of row and number, representing the position.
        """
        self.board_layout[position[0]][position[1]] = pipe
        self.change_playable_amount(pipe.get_name(), -1)

    def pipe_in_position(self, position):
        """
        Returns the pipe in the given position (row, col) of the game board 
        if there is a Pipe in the given position. Returns None if the position given 
        is None or if the object in the given position is not a Pipe.
        
        Parameters:
            position (tuple<int, int>): A tuple of row and number, representing the position.
        
        Returns:
            (Pipe): Instance of a pipe.
        """
        pipe = self.board_layout[position[0]][position[1]]

        if pipe.get_id() == 'pipe' or pipe.get_id() == 'special_pipe':
            return pipe
        else:
            return None

    def remove_pipe(self, position):
        """
        Removes the pipe at the given position from the board.
        Returns the pipe back to the playable pipes.
        
        Parameters:
            position (tuple<int, int>): A tuple of row and number, representing the position.
        """
        pipe = self.board_layout[position[0]][position[1]]
        tile = Tile('tile', True)

        self.board_layout[position[0]][position[1]] = tile
        self.change_playable_amount(pipe.get_name(), 1)

    def position_in_direction(self, direction, position):
        """
        Returns the direction and position (row, col) in the given 
        direction from the given position, if the resulting 
        position is within the game grid.
        
        Parameters:
            position (tuple<int, int>): A tuple of row and number, representing the position.
            direction(str): Given direction. ‘N’, ‘S’, ‘E’ or ‘W’.
        
        Returns:
            (tuple<str, tuple<int, int>>): Side and position in the specified direction.
        """
        if direction == "N" and position[0] != 0:
            pos_in_dir = ("S", (position[0] - 1, position[1]))
        elif direction == "E" and position[1] != 5:
            pos_in_dir = ("W", (position[0], position[1] + 1))
        elif direction == "S" and position[0] != 5:
            pos_in_dir = ("N", (position[0] + 1, position[1]))
        elif direction == "W" and position[1] != 0:
            pos_in_dir = ("E", (position[0], position[1] - 1))
        else:
            return None

        return pos_in_dir

    def end_pipe_positions(self):
        """
        Finds and saves the start and end pipe 
        positions from the game board.
        """
        self.start_position = self.get_starting_position()
        self.end_position = self.get_ending_position()

    def get_starting_position(self):
        """
        Returns the (row, col) position of the start pipe.

        Returns:
            (tuple<int, int>): (row, col) position of the start pipe.
        """
        for row in self.board_layout:
            for column in row:
                if column.get_name() == "start":
                    start_position = (self.board_layout.index(row), row.index(column))

        return start_position

    def get_ending_position(self):
        """
        Returns the (row, col) position of the end pipe.

        Returns:
            (tuple<int, int>): (row, col) position of the end pipe.
        """
        for row in self.board_layout:
            for column in row:
                if column.get_name() == "end":
                    end_position = (self.board_layout.index(row), row.index(column))

        return end_position

    #########################UNCOMMENT THIS FUNCTION WHEN READY#######################
    def check_win(self):
        """
        (bool) Returns True  if the player has won the game False otherwise.
        """
        position = self.get_starting_position()
        pipe = self.pipe_in_position(position)
        queue = [(pipe, None, position)]
        discovered = [(pipe, None)]
        while queue:
            pipe, direction, position = queue.pop()
            for direction in pipe.get_connected(direction):
                
                if self.position_in_direction(direction, position) is None:
                    new_direction = None 
                    new_position = None
                else:
                    new_direction, new_position = self.position_in_direction(direction, position)
                if new_position == self.get_ending_position() and direction == self.pipe_in_position(
                        new_position).get_connected()[0]:
                    return True

                pipe = self.pipe_in_position(new_position)
                if pipe is None or (pipe, new_direction) in discovered:
                    continue
                discovered.append((pipe, new_direction))
                queue.append((pipe, new_direction, new_position))
        return False
    #########################UNCOMMENT THIS FUNCTION WHEN READY#######################


def main():
    print("Please run gui.py instead")


if __name__ == "__main__":
    main()
