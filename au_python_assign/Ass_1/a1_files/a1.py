from a1_support import *


def display_game(game, grid_size):
    """Prints the current game to the player.

    First loop takes care of the first line only.
    Second loop adds rest of the rows to the print string.

	Parameters:
		game (str): Game string.
        grid_size (int): Size of the game grid.
	"""
    wall_h = WALL_HORIZONTAL * 5 * grid_size + WALL_HORIZONTAL
    i = 0
    print_game = ""
    while i <= grid_size: # first line
        if i == 0:
            print_game += "  " + WALL_VERTICAL
        else:
            if i < 10:
                print_game += " " + str(i) + " " + WALL_VERTICAL
            else:
                print_game += " " + str(i) + WALL_VERTICAL
        i += 1

    print_game += '\n' + wall_h
    i = 0
    j = 0
    while i < grid_size: # row
        print_game += '\n' + ALPHA[i] + " " + WALL_VERTICAL
        while j < grid_size: # cell
            print_game += " " + game[j+i*grid_size] + " " + WALL_VERTICAL
            j += 1
        print_game += '\n' + wall_h
        i += 1
        j = 0

    print(print_game)

def parse_position(action, grid_size):
    """Checking validity of player input.

    Dealing with other player inputs, such as reset, help or quit.

	Parameters:
		action (str): Player input - action.
        grid_size (int): Size of the game grid.

    Returns:
        (tuple<int, int>): Tuple of position if player inputs flag on move to cell.
        (str): String for game to decide what to do based on player input.
	"""
    if action == "h": # Help
        print(HELP_TEXT)
        return None
    elif action == "q": # Quit
        quit_yn = str(input("You sure about that buddy? (y/n): "))
        if quit_yn == "y":
            print("Catch you on the flip side.")
            return "quit"
        elif quit_yn == "n":
            print("Let's keep going.")
        else:
            print(INVALID)
            return None
    elif len(action) >= 2 and len(action) <= 3 and action[0] in ALPHA and action[1:].isdigit(): # Move to cell
        if ALPHA.find(action[0]) < grid_size and int(action[1:]) <= grid_size:
            position = ALPHA.find(action[0]), int(action[1:]) - 1
            return position
        else:
            print(INVALID)
            return None
    elif len(action) >= 4 and len(action) <= 5 and action[0] =="f" and action[1] == " " and action[2] in ALPHA and action[3:].isdigit(): # Flag cell
        if ALPHA.find(action[2]) < grid_size and int(action[3:]) <= grid_size:
            position = ALPHA.find(action[2]), int(action[3:]) - 1
            return position
        else:
            print(INVALID)
            return None
    elif action == ":)": # Restart
        print("It's rewind time.")
        return "reset"
    else:
        print(INVALID)
        return None


def position_to_index(position, grid_size):
    """Coverts position into index.

	Parameters:
		position (tuple): Position in the game; row, column.
        grid_size (int): Size of the game grid.

    Returns:
        (int): Index in a game string, converted from position tuple.
	"""
    index = position[0] * grid_size + position[1]
    return index


def index_to_position(index, grid_size):
    """Coverts index into position.

	Parameters:
		index (int): Index in a game string.
        grid_size (int): Size of the game grid.

    Returns:
        (int): Position in the game; row, column.
	"""
    position = index % grid_size , index // grid_size
    return position


def replace_character_at_index(game, index, character):
    """Replaces character at game index to a different one.

	Parameters:
        game (str): Game string.
		index (int): Index in a game string.
        character (str): Character to replace at game index.

    Returns:
        (str): Game string.
	"""
    game = game[:index] + character + game[index + 1:]
    return game


def flag_cell(game, index):
    """Flags a selected cell using a heart character.

	Parameters:
        game (str): Game string.
		index (int): Index in a game string.

    Returns:
        (str): Game string.
	"""
    if game[index] != FLAG:
        game = replace_character_at_index(game, index, FLAG)
    else:
        game = game[:index] + UNEXPOSED + game[index + 1:]
    return game


def index_in_direction(index, grid_size, direction):
    """Returns an index in a game based of requested direction.

	Parameters:
		index (int): Index in a game string.
        grid_size (int): Size of the game grid.
        direction (str): Up, down, left, right or diagonal.

    Returns:
        (int): Index in a game string.
	"""
    position_0 = index_to_position(index, grid_size)[0]
    position_1 = index_to_position(index, grid_size)[1]

    if direction == UP and position_1 > 0:
        index -= grid_size
    elif direction == DOWN and position_1 < grid_size - 1:
        index += grid_size
    elif direction == LEFT and position_0 > 0:
        index -= 1
    elif direction == RIGHT and position_0 < grid_size - 1:
        index += 1
    elif direction == f"{UP}-{LEFT}" and position_1 > 0 and position_0 > 0:
        index -= grid_size + 1
    elif direction == f"{UP}-{RIGHT}" and position_1 > 0 and position_0 < grid_size - 1:
        index -= grid_size - 1
    elif direction == f"{DOWN}-{LEFT}" and position_1 < grid_size - 1 and position_0 > 0:
        index += grid_size - 1
    elif direction == f"{DOWN}-{RIGHT}" and position_1 < grid_size - 1 and position_0 < grid_size - 1:
        index += grid_size + 1
    else:
        return None

    return index


def neighbour_directions(index, grid_size):
    """Returns indexes representing neighbour cells.

	Parameters:
		index (int): Index in a game string.
        grid_size (int): Size of the game grid.

    Returns:
        (list<int>): List of indexes representing neighbour cells.
	"""
    neighbours = []
    for direction in DIRECTIONS:
        neighbour = index_in_direction(index, grid_size, direction)
        if neighbour != None:
            neighbours.append(neighbour)
    return neighbours


def number_at_cell(game, pokemon_locations, grid_size, index):
    """Returns number of pokemons in neighbour cells to the selected one.

	Parameters:
        game (str): Game string.
        pokemon_locations (tuple<int, ...>): Tuple of all Pokemon's locations.
        grid_size (int): Size of the game grid.
		index (int): Index in a game string.

    Returns:
        (int): Number of pokemons in neighbour cells to the selected one.
	"""
    neighbours = neighbour_directions(index, grid_size)
    poke_num_neighbour = 0

    for pokemon_location in pokemon_locations:
        if pokemon_location in neighbours:
            poke_num_neighbour += 1

    return poke_num_neighbour


def check_win(game, pokemon_locations):
    """Returns True if win conditions were met.

    Win conditions: All cells are exposed and correct cells are flagged.

	Parameters:
        game (str): Game string.
        pokemon_locations (tuple<int, ...>): Tuple of all Pokemon's locations.

    Returns:
        (bool): True if win conditions were met.
	"""
    win = False
    if game.find(UNEXPOSED) == -1:
        for i in pokemon_locations:
            if game[i] != FLAG:
                return win
        if game.find(EXPOSED) == -1:
            return win
        win = True
    return win


def main():
    """Main function of the Pokemon game.

    The game starts with request for player input concerning grid size and number of pokemons.

    Game string is generated, printed out and player has to input an action.
    This repeats until end of game occurs.

    Until player inputs a "flag cell" or "move to cell" valid command, the request for input loops and game is not progressing.

    For list of valid actions, read string "HELP_TEXT" from a1_support.py.

    Game loops until a check_win function returns True or until the player looses, resets the game, or quits.
	"""
    grid_size = int(input("Please input the size of the grid: "))
    number_of_pokemons = int(input("Please input the number of pokemons: "))

    pokemon_locations = generate_pokemons(grid_size, number_of_pokemons)
    
    game = grid_size * grid_size * UNEXPOSED
    position = None
    
    while check_win(game, pokemon_locations) != True:
        while position == None:
            display_game(game, grid_size)
            action = str(input('\n' + "Please input action: "))
            position = parse_position(action, grid_size)
            if position == "quit":
                return
            elif position != None and position != "reset":
                index = position_to_index(position, grid_size)
                if game[index] == FLAG and action[0] != "f":
                        position = None
                    
        position = None
        if action[0] == "f":
            game = flag_cell(game, index)
        elif action == ":)":
            pokemon_locations = generate_pokemons(grid_size, number_of_pokemons)
            game = grid_size * grid_size * UNEXPOSED
        elif index in pokemon_locations:
            for i in pokemon_locations:
                game = replace_character_at_index(game, i, POKEMON)
            display_game(game, grid_size)
            print("You have scared away all the pokemons.")
            return
        else:
            search = big_fun_search(game, grid_size, pokemon_locations, index)
            game = replace_character_at_index(game, index, EXPOSED)
            for i in search:
                pok_num = number_at_cell(game, pokemon_locations, grid_size, i)
                if game[i] != FLAG:
                    game = replace_character_at_index(game, i, str(int(EXPOSED) + pok_num))
                    
    display_game(game, grid_size)
    print("You win.")
    return

def big_fun_search(game, grid_size, pokemon_locations, index):
    """Searching adjacent cells to see if there are any Pokemon"s present.

	Using some sick algorithms.

	Find all cells which should be revealed when a cell is selected.

	For cells which have a zero value (i.e. no neighbouring pokemons) all the cell"s
	neighbours are revealed. If one of the neighbouring cells is also zero then
	all of that cell"s neighbours are also revealed. This repeats until no
	zero value neighbours exist.

	For cells which have a non-zero value (i.e. cells with neightbour pokemons), only
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

    number = number_at_cell(game, pokemon_locations, grid_size, index)
    if number != 0:
	    return queue

    while queue:
	    node = queue.pop()
	    for neighbour in neighbour_directions(node, grid_size):
		    if neighbour in discovered or neighbour is None:
			    continue

		    discovered.append(neighbour)
		    if game[neighbour] != FLAG:
			    number = number_at_cell(game, pokemon_locations, grid_size, neighbour)
			    if number == 0:
				    queue.append(neighbour)
		    visible.append(neighbour)
    return visible
# #########################UNCOMMENT THIS FUNCTION WHEN READY#######################

if __name__ == "__main__":
    main()
