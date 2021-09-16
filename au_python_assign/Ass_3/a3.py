import random
import tkinter as tk
from tkinter import messagebox

UP = "up"
DOWN = "down"
LEFT = "left"
RIGHT = "right"
DIRECTIONS = (UP, DOWN, LEFT, RIGHT,
              f"{UP}-{LEFT}", f"{UP}-{RIGHT}",
              f"{DOWN}-{LEFT}", f"{DOWN}-{RIGHT}")
POKEMON = "☺"
FLAG = "♥"
UNEXPOSED = "~"
EXPOSED = "0"

TASK_ONE = 1
TASK_TWO = 2


class BoardModel:
    """
    Model of the game board
    """
    def __init__(self, grid_size, num_pokemon):
        self._grid_size = grid_size
        self._num_pokemon = num_pokemon
        self._game = UNEXPOSED * grid_size ** 2
        self._pokemon_locations = self.generate_pokemons(grid_size, num_pokemon)
        self._num_attempted_catches = 0

    def set_game(self, game):
        """ Sets the game string to a new one.

        Parameters:
            game (str): The game string.
        """
        self._game = game

    def get_game(self):
        """ Get the game string.

        Returns:
            (str): Game string.
        """
        return self._game
    
    def get_pokemon_locations(self):
        """ Get pokemon lcoations.
        
        Returns:
            (tuple<int, ...>): Tuple of all Pokemon's locations.
        """
        return self._pokemon_locations

    def get_num_attempted_catches(self):
        """ Get number of attempted catches.
        
        Returns:
            (int): Number of attempted catches.
        """
        return self._num_attempted_catches

    def get_num_pokemon(self):
        """ Get number of pokemons.
        
        Returns:
            (int): Number of pokemons.
        """
        return self._num_pokemon

    def check_loss(self, index):
        """ Checks, if the player lost the game. If yes, returns True.
            Updates the game string with pokemon locations to show to the player.

        Parameters:
            index (int): The index of the cell in the game string.

        Returns:
            (bool): True if player lost.
        """
        if index in self._pokemon_locations:
            for i in self._pokemon_locations:
                self._game = self.replace_character_at_index(self._game, i, POKEMON)
            return True
        else:
            return False

    def position_to_index(self, position, grid_size):
        """Convert the row, column coordinate in the grid to the game strings index.

        Parameters:
            position (tuple<int, int>): The row, column position of a cell.
            grid_size (int): The grid size of the game.

        Returns:
            (int): The index of the cell in the game string.
        """
        index = position[0] * grid_size + position[1]
        return index

    def index_to_position(self, index, grid_size):
        """ Converts the game string index to row, column coordinate.

        Parameters:
            index (int): The index of the cell in the game string.
            grid_size (int): The grid size of the game.

        Returns:
            (tuple<int, int>): The row, column position of a cell.
        """
        position = index % grid_size , index // grid_size
        return position

    def replace_character_at_index(self, game, index, character):
        """A specified index in the game string 
        at the specified index is replaced by a new character.

        Parameters:
            game (str): The game string.
            index (int): The index in the game string where the character is replaced.
            character (str): The new character that will be replacing the old character.

        Returns:
            (str): The updated game string.
        """
        game = game[:index] + character + game[index + 1:]
        return game

    def flag_cell(self, game, index):
        """Toggle Flag on or off at selected index. If the selected index is already
        revealed, the game would return with no changes.

        Parameters:
            game (str): The game string.
            index (int): The index in the game string where a flag is placed.

        Returns:
            (str): The updated game string.
        """
        if game[index] == FLAG:
            self._game = self.replace_character_at_index(game, index, UNEXPOSED)

        elif game[index] == UNEXPOSED:
            self._game = self.replace_character_at_index(game, index, FLAG)

        return game

    def index_in_direction(self, index, grid_size, direction):
        """The index in the game string is updated by determining the
        adjacent cell given the direction.
        The index of the adjacent cell in the game is then calculated and returned.

        For example:
        | 1 | 2 | 3 |
        A | i | j | k |
        B | l | m | n |
        C | o | p | q |

        The index of m is 4 in the game string.
        if the direction specified is "up" then:
        the updated position corresponds with j which has the index of 1 in the game string.

        Parameters:
            index (int): The index in the game string.
            grid_size (int): The grid size of the game.
            direction (str): The direction of the adjacent cell.

        Returns:
            (int): The index in the game string corresponding to the new cell position
            in the game.

            None for invalid direction.
        """
        # convert index to row, col coordinate
        col = index % grid_size
        row = index // grid_size
        if RIGHT in direction:
            col += 1
        elif LEFT in direction:
            col -= 1
        
        if UP in direction:
            row -= 1
        elif DOWN in direction:
            row += 1

        if not (0 <= col < grid_size and 0 <= row < grid_size):
            return None

        return self.position_to_index((row, col), grid_size)

    def neighbour_directions(self, index, grid_size):
        """Seek out all direction that has a neighbouring cell.

        Parameters:
            index (int): The index in the game string.
            grid_size (int): The grid size of the game.

        Returns:
            (list<int>): A list of index that has a neighbouring cell.
        """
        neighbours = []
        for direction in DIRECTIONS:
            neighbour = self.index_in_direction(index, grid_size, direction)
            if neighbour is not None:
                neighbours.append(neighbour)

        return neighbours

    def number_at_cell(self, game, pokemon_locations, grid_size, index):
        """Calculates what number should be displayed at that specific index in the game.

        Parameters:
            game (str): Game string.
            pokemon_locations (tuple<int, ...>): Tuple of all Pokemon's locations.
            grid_size (int): Size of game.
            index (int): Index of the currently selected cell

        Returns:
            (int): Number to be displayed at the given index in the game string.
        """
        if game[index] != UNEXPOSED:
            return int(game[index])

        number = 0
        for neighbour in self.neighbour_directions(index, grid_size):
            if neighbour in pokemon_locations:
                number += 1

        return number

    def check_win(self, game, pokemon_locations):
        """Checking if the player has won the game.

        Parameters:
            game (str): Game string.
            pokemon_locations (tuple<int, ...>): Tuple of all Pokemon's locations.

        Returns:
            (bool): True if the player has won the game, false if not.
        """
        return UNEXPOSED not in self._game and self._game.count(FLAG) == len(pokemon_locations)

    def reveal_cells(self, game, grid_size, pokemon_locations, index):
        """Reveals all neighbouring cells at index and repeats for all
        cells that had a 0.

        Does not reveal flagged cells or cells with Pokemon.

        Parameters:
            game (str): Game string.
            pokemon_locations (tuple<int, ...>): Tuple of all Pokemon's locations.
            grid_size (int): Size of game.
            index (int): Index of the currently selected cell

        Returns:
            (str): The updated game string
        """
        number = self.number_at_cell(game, pokemon_locations, grid_size, index)
        game = self.replace_character_at_index(game, index, str(number))
        clear = self.big_fun_search(game, grid_size, pokemon_locations, index)
        for i in clear:
            if game[i] != FLAG:
                number = self.number_at_cell(game, pokemon_locations, grid_size, i)
                game = self.replace_character_at_index(game, i, str(number))

        return game

    def big_fun_search(self, game, grid_size, pokemon_locations, index):
        """Searching adjacent cells to see if there are any Pokemon"s present.

        Using some sick algorithms.

        Find all cells which should be revealed when a cell is selected.

        For cells which have a zero value (i.e. no neighbouring pokemons) all the cell"s
        neighbours are revealed. If one of the neighbouring cells is also zero then
        all of that cell"s neighbours are also revealed. This repeats until no
        zero value neighbours exist.

        For cells which have a non-zero value (i.e. cells with neighbour pokemons), only
        the cell itself is revealed.

        Parameters:
            game (str): Game string.
            grid_size (int): Size of game.
            pokemon_locations (tuple<int, ...>): Tuple of all Pokemon's locations.
            index (int): Index of the currently selected cell

        Returns:
            (list<int>): List of cells to turn visible.
        """
        queue = [index]
        discovered = [index]
        visible = []

        if game[index] == FLAG:
            return queue

        number = self.number_at_cell(game, pokemon_locations, grid_size, index)
        if number != 0:
            return queue

        while queue:
            node = queue.pop()
            for neighbour in self.neighbour_directions(node, grid_size):
                if neighbour in discovered:
                    continue

                discovered.append(neighbour)
                if game[neighbour] != FLAG:
                    number = self.number_at_cell(game, pokemon_locations, grid_size, neighbour)
                    if number == 0:
                        queue.append(neighbour)
                visible.append(neighbour)
        return visible

    def generate_pokemons(self, grid_size, number_of_pokemons):
        """Pokemons will be generated and given a random index within the game.

        Parameters:
            grid_size (int): The grid size of the game.
            number_of_pokemons (int): The number of pokemons that the game will have.

        Returns:
            (tuple<int>): A tuple containing  indexes where the pokemons are
            created for the game string.
        """
        cell_count = grid_size ** 2
        pokemon_locations = ()

        for _ in range(number_of_pokemons):
            if len(pokemon_locations) >= cell_count:
                break
            index = random.randint(0, cell_count-1)

            while index in pokemon_locations:
                index = random.randint(0, cell_count-1)

            pokemon_locations += (index,)

        return pokemon_locations

    def character_at_index(self, game, index):
        """ Returns character at the specified game string index.

        Parameters:
            game (str): Game string.
            index (int): Index of the currently selected cell

        Returns:
            (string): Character at game string index.
        """
        character = game[index]
        return character


class PokemonGame:
    """Game application that manages communication between the board view and board model."""

    def __init__(self, master, grid_size = 10, num_pokemon = 15, task = TASK_TWO):
        """Create a new pokemon game within a master widget"""
        self._master = master

        self._task = task
        self._grid_size = grid_size
        self._num_pokemon = num_pokemon

        self._board = BoardModel(self._grid_size, self._num_pokemon)
        self._pok_locations = self._board.get_pokemon_locations()

        # Top panel is static, no need to draw it more than once
        self._top_panel = TopPanel(self._master)
        self._top_panel.pack()

        if self._task == 2:
            self.draw_menubar()

        self.draw()

    def redraw(self):
        """Redraw the board view."""
        self._board_view.destroy()
        self.draw()

    def draw(self):
        """Draw the board view."""
        self._board_view = BoardView(self._master, self._grid_size, self._board, self.move_to, self.flag_cell)
        self._board_view.pack()

    def draw_menubar(self):
        """Define and add menubar to the master widget."""
        self._menubar = tk.Menu(self._master)
        self._filemenu = tk.Menu(self._menubar, tearoff=0)
        self._filemenu.add_command(label="Open", command="")
        self._filemenu.add_command(label="Save", command="")
        self._filemenu.add_separator()
        self._filemenu.add_command(label="Exit", command=self._master.quit)
        self._menubar.add_cascade(label="File", menu=self._filemenu)

        self._master.config(menu=self._menubar)

    def move_to(self, e):
        """Discover what is in the unexposed cell.
        If there are no pokemon, reveal nearby cells.
        If there is a pokemon, player looses the game.

        Parameters:
            e (tkinter.Event): Event class generated by mouse click. Contains pixel coordinates on the canvas.
        """
        print(type(e))
        position = self._board_view.pixel_to_position(e)
        # messagebox.showinfo("Mouse 1", "LMB pressed, x = " + str(e.x) + ", y = " + str(e.y))

        index = self._board.position_to_index(position, self._grid_size)
        game = self._board.get_game()
        
        #update game string based on player movement
        if game[index] == FLAG or game[index] != UNEXPOSED:
            None
        # check, if there is a pokemon at the selected square and player lost
        elif self._board.check_loss(index):
            messagebox.showwarning("GG", "GAME OVER")
            self.redraw()
            self._board_view.unbind_mouse()
            game = self._board.get_game()
            print(game)
        else:
            game = self._board.reveal_cells(game, self._grid_size, self._pok_locations, index)
            self._board.set_game(game)
            print(game)
            self.redraw()

        # check for win
        if self._board.check_win(game, self._pok_locations):
            messagebox.showinfo("GG", "YOU WIN!")
            self._board_view.unbind_mouse()

    def flag_cell(self, e):
        """Flag a cell. 
        If there are no other unexposed cells and
        flags are at the correct positions; player wins.

        Parameters:
            e (tkinter.Event): Event class generated by mouse click. Contains pixel coordinates on the canvas.
        """
        position = self._board_view.pixel_to_position(e)
        game = self._board.get_game()
        index = self._board.position_to_index(position, self._grid_size)

        if game[index] == UNEXPOSED or game[index] == FLAG:
            # flag cell in model
            self._board.flag_cell(game, index)

            print(game)
            self.redraw()

        # check for win
        if self._board.check_win(game, self._pok_locations):
            messagebox.showinfo("GG", "YOU WIN!")
            self._board_view.unbind_mouse()


class BoardView(tk.Canvas):
    """View of the pokemon game board"""

    def __init__(self, master, grid_size, board, move_to, flag_cell, board_width = 600, *args, **kwargs):
        """Construct a board view based on board_width and grid_size.

        Parameters:
            master (tk.Widget): Widget within which the board is placed.
            grid_size (int): Sum of squares in one row or column.
            board (BoardModel): Board model of the Pokemon game.
            move_to (callable): Callable to call when player moves to an unexposed cell.
            flag_cell (callable): Callable to call when player flags an unexposed cell.
            board_width (int): Board width in pixels.
        """
        super().__init__(master, width = board_width-100, height = board_width-100, *args, **kwargs)
        self._master = master

        self._grid_size = grid_size
        self._board_width = board_width
        self._board = board

        # functions from the PokemonGame class to be called by clicks
        self.move_to = move_to
        self.flag_cell = flag_cell

        # square width based on board width
        self._square_width = self._board_width / 12

        self.bind_mouse()

        self.draw_board(self._square_width, self._board)

    def bind_mouse(self):
        """Bind left (b1) and right (b2, b3) mouse button."""
        self._b1 = self.bind("<Button-1>", self._handle_left_click)
        self._b2 = self.bind("<Button-2>", self._handle_right_click)
        self._b3 = self.bind("<Button-3>", self._handle_right_click)

    def unbind_mouse(self):
        """Unbind the mouse buttons."""
        self.unbind("<Button-1>", self._b1)
        self.unbind("<Button-2>", self._b2)
        self.unbind("<Button-3>", self._b3)

    def _handle_left_click(self, e):
        """Called when left mouse button is clicked."""
        self.move_to(e)

    def _handle_right_click(self, e):
        """Called when right mouse button is clicked."""
        self.flag_cell(e)

    def get_square_width(self):
        """Returns the square width.

        Returns:
            (int): Square width.
        """
        return self._square_width

    def draw_board(self, square_width, board):
        """Create squares on the canvas based on the current game.
        Dynamic square width based on board width.

        Parameters:
            square_width (int): Width of a square.
            board (BoardModel): Board model of the Pokemon game.
        """
        game = board.get_game()
        index = 0

        for row in range(self._grid_size):
            y0 = square_width * row
            y1 = square_width * (row + 1)

            for column in range(self._grid_size):
                x0 = square_width * column
                x1 = square_width * (column + 1)

                if game[index] == UNEXPOSED:
                    self.create_rectangle(x0, y0, x1, y1, fill="dark green")
                elif game[index] == FLAG:
                    self.create_rectangle(x0, y0, x1, y1, fill="red")
                elif game[index] == POKEMON:
                    self.create_rectangle(x0, y0, x1, y1, fill="yellow")
                    character = board.character_at_index(game, index)
                    self.create_text((x0 + 25, y0 + 25), text=character)
                else:
                    self.create_rectangle(x0, y0, x1, y1, fill="light green")
                    character = board.character_at_index(game, index)
                    self.create_text((x0 + 25, y0 + 25), text=character)

                index += 1

    def pixel_to_position(self, pixel):
        """ Convers pixel coordinates to row, col position. 
        
        Parameters:
            pixel(tkinter.Event): Event class generated by mouse click. Contains pixel coordinates on the canvas.
        
        Returns:
            (tuple<int, int>): The row, column position of a cell.
        """
        position = int(pixel.y // self._square_width), int(pixel.x // self._square_width)
        return position

class TopPanel(tk.Frame):
    """Top panel in the game window with the game name as a heading."""
    def __init__(self, master):
        """Crate new top panel"""
        super().__init__(master)

        self.draw()

    def draw(self):
        """Draw label with the game name."""
        tk.Label(text="Pokemon: Got 2 Find Them All!", bg = "IndianRed2", fg = "white", font=("Courier", 22, "bold")).pack()

def main():
    root = tk.Tk()
    root.title("Pokemon: Got 2 Find Them All!")

    PokemonGame(root)

    root.update()
    root.mainloop()


if __name__ == "__main__":
    main()