import random
import itertools
from BinaryHeap import BinHeap

class Board:
    """Board represents a minesweeper game instance.

    Attributes:
        rows: Number of rows in the minesweeper board.
        columns: Number of columns in the minesweeper board. 
        num_mines: Number of mines in the minesweeper board. 
        placed_mines: Number of mines in the minesweeper board that have been placed. Defaults to 0, can be any integer.
        revealed_count: Number of tiles which have been revealed. Defaults to 0, increases respectively with number of tiles revealed.
        the_board: Doubly nested list representation of the board, row count represents the number of elements in this list
                    and each row element has column count elements. Each board index has the value -1 assigned indicating that
                    it is has yet to be modified.
        mine_coords: Dictionary containing coordinates of every single mine within the board. Initially empty, filled when mines are placed.
        move_priority_queue: Priority queue represented as a minHeap which stores all potential plays. Initially empty, filled after intial play.
        marked_mines: Dictionary containing coordinates of what the AI has determined to be the location of a mine. Initially empty, filled after mines are discovered.
        int_coords: List containing the coordinates of all the visible integers within the game. Initially empty, filled as integers are discovered.
        no_mines: Dictionary containing the coordinates of tiles at which the AI determined it impossible for there to be mines.
    """
    def __init__(self, rows: int = 9, columns: int = 9, num_mines: int = 9):
        """Constructor for minesweeper board.
        Arguments:
            rows: Defaults to 9, can be any integer.
            columns: Defaults to 9, can be any integer.
            num_mines: Defaults to 9, can be any integer.
        """
        self.rows: int = rows
        self.columns: int = columns
        self.num_mines: int = num_mines
        self.placed_mines: int = 0
        self.revealed_count: int = 0
        self.the_board: List[List[Any]] = ([[[0] for _ in range(self.columns)] for _ in range(self.rows)])
        self.mine_coords = {}
        self.turn_count = 0
        self.place_mines()
        self.update_nums()
        self.print_board()
        self.move_priority_queue = BinHeap((self.rows*self.columns)**2, lambda x, y: x[1] < y[1])
        self.marked_mines = {}
        self.int_coords = []
        self.no_mines = {}

    def __str__(self) -> str:
        """printing a board instance allows you to see the array making up the board."""
        row_str = ""
        for r in self.the_board:
            row_str += f"{r}\n"
        return row_str
    
    def print_board(self):
        """print_board prints the player-observable game space."""

        #Initializing the middle section of the board (excluding header and footer)
        main_space = ""

        #Spacing to accomodate for rows that do not have the maximum-digit row numbers in front of them
        front_spacing = len(str(self.rows))*" "

        #Dashes for the top and bottom of the board
        top_bottom_edges = front_spacing + (self.columns + 2)*" -" + "\n"

        #Initializing the front spacing for where the column labels begin
        column_labels = "   " + front_spacing

        #Loop used to generate the string pertaining to the main space
        for row_index, board_row in enumerate(self.the_board):
            for column_index, board_column in enumerate(board_row):
                
                #Determines front spacing for each row (for equal space across all rows) determined by how long the row number is for that row
                front_spacing = (len(str(self.rows))-len(str(row_index+1))+1)*" "

                #If at the beginning of a row, adds to the main space the row number as well as front spacing, followed by the vertical border line
                #Otherwise, just adds a space to the current row in the main space so that the next placed tile can be properly aligned
                main_space += f"{row_index+1}" + front_spacing + "| " if (not column_index%self.columns) else " "

                #If the current tile is hidden, uses * to the corresponding position in the main space string representation
                #If the current tile is not hidden, adds the value of the tile to the main space string representation
                main_space += "*" if (type(board_column) != int and board_column != "X") else f"{board_column}"

            #Adds the row number to the end of each row and then moves to the next line
            main_space += f" | {row_index+1}\n"

        #Adds the column number labels to the column_labels string (which may span multiple lines depending on how long the largest column number is)
        column_labels += f"\n{column_labels}".join([" ".join(elem) for elem in itertools.zip_longest(*(str(i) for i in range(1,self.columns+1)), fillvalue=" ")]) + "\n"

        #Assigns the header (top) of the board column labels as well as edge dashes
        header = column_labels + top_bottom_edges

        #Assigns the footer (bottom) of the board column labels as well as edge dashes
        footer = top_bottom_edges + column_labels

        #Creates the representation of the entire board, containing the header, main space, and footer
        board_representation = header
        board_representation += main_space
        board_representation += footer

        print(board_representation)

    def place_mines(self, one_mine = False):
        """place_mines places all of the starting mines on our minesweeper board, ensures that mines are placed in unique locations.
        Arguments:
            one_mine: Optional parameter which defaults to False. If True is passed in, it will return the coordinates of the most recently placed mine.
        Returns:
            Tuple representation of coordinates of the most recently placed mine.
        """

        #Ensures that all mines are placed before ending the function
        while self.placed_mines < self.num_mines:

            #Obtains random x and y integers within the row and column ranges of the game 
            x = random.randrange(self.rows)
            y = random.randrange(self.columns)

            #Ensures that a mine is not placed where a mine already exists
            if self.the_board[x][y] != [9]:

                self.the_board[x][y] = [9]

                #Adds the location of the placed mine to a dictionary holding the locations of mines (used to later update the numbers of the board)
                self.mine_coords[(x,y)] = (x,y)

                self.placed_mines += 1

        #When only one mine is placed, as indicated by the optional boolean argument, the coordinates of that mine are returned
        if one_mine == True:
            return (x,y)
        
    def indices_around_coord(self, coord, adjacent = False, only_hidden = False):
        """indices_around_coord returns the indices around a coordinate (in a 3x3 area, or directly adjacent) in the game board.
        Arguments:
            coord: The coordinate at which to check for surrounding indices.
            adjacent: Optional argument which defaults to False. If True, only returns the indices directly adjacent to the passed in coordinates. When False, the indices within the 3x3 area are returned.
        Returns:
            List of indices (tuples of coordinates)   
        """

        #Assigns coordinate values to indices of all cardinal directions surrounding a central tile coordinate point
        n_indices = coord[0]-1, coord[1]
        e_indices = coord[0], coord[1]+1
        s_indices = coord[0]+1, coord[1]
        w_indices = coord[0], coord[1]-1
        ne_indices = coord[0]-1, coord[1]+1
        se_indices = coord[0]+1, coord[1]+1
        sw_indices = coord[0]+1, coord[1]-1
        nw_indices = coord[0]-1, coord[1]-1

        #If the adjacent is False, all indices in a 3x3 area around the central tile are considered to be surrounding indices
        if adjacent == False:
            surrounding_indices = [n_indices, e_indices, s_indices, w_indices, ne_indices, se_indices, sw_indices, nw_indices]

        #If adjacent is True, only adjacent indices are considered to be surrounding indices
        else:
            surrounding_indices = [n_indices, e_indices, s_indices, w_indices]

        #Output indices initialized as an empty list
        output_indices = []

        #Loop that ensures that all indices appended to the output indice list are valid
        for each_coord in surrounding_indices:

            #Ensures that all indices are within the bounds of the game board
            if each_coord[0] < self.rows and each_coord[0] >= 0 and each_coord[1] < self.columns and each_coord[1] >= 0: #Makes sure that the coordinates are within the bounds of the game board.

                #If only_hidden is True, the output_indices will not contain the coordinates of tiles which are revealed 
                if only_hidden:

                    #Revealed tiles have an integer value
                    if type(self.the_board[each_coord[0]][each_coord[1]]) == int:
                        continue
                
                #Appends the valid tile to the list of output indices
                output_indices.append(each_coord)
                
        return output_indices
        
    def nums_around_mine(self, coords = None):
        """nums_around_mine keeps track of the tiles in a 3x3 radius of mines and assigns them a value with respect to how many mines there are near.
        Arguments:
            coords: Optional argument which defaults to None. Can be used to specify the coordinates (as a tuple) of a removed mine.
        Returns:
            A dictionary containing coordinates of all of the tiles in a 3x3 radius of mines and their pertaining values.
        """
        
        if coords == None:
            coord_list = list(self.mine_coords.keys())
        else:
            coord_list = [coords]
        known_indices = {}
        for each_mine_index in coord_list:
            indices_to_add = self.indices_around_coord(each_mine_index)   
            for coords in indices_to_add:
                if coords in known_indices:
                    known_indices[coords] += 1
                else:
                    known_indices[coords] = 1
        return known_indices
    
    def update_nums(self, coords = None):
        """update_nums updates the numbers on the minesweeper board with respect to where the mines are placed.
        Arguments:
            coords: A tuple representing coordinates at which a mine was previously contained.
        """
        
        if coords == None:
            coord_dict = self.nums_around_mine()
        else:
            coord_dict = self.nums_around_mine(coords)
            if self.placed_mines < self.num_mines:
                self.the_board[coords[0]][coords[1]] = [0]
        for each_coord in list(coord_dict.keys()):
            if self.placed_mines == self.num_mines and each_coord not in self.mine_coords and coords == None:
                self.the_board[each_coord[0]][each_coord[1]] = [coord_dict[each_coord]]
            elif self.placed_mines == self.num_mines and each_coord not in self.mine_coords:
                self.the_board[each_coord[0]][each_coord[1]][0] += 1
            elif self.placed_mines != self.num_mines and each_coord in self.mine_coords:
                self.the_board[coords[0]][coords[1]][0] += 1
            elif self.placed_mines != self.num_mines and each_coord not in self.mine_coords:
                self.the_board[each_coord[0]][each_coord[1]][0] -= 1

    def remove_mine(self, coords):
        """remove_mine removes the mine at the specified coordinates.
        Arguments:
            coords: Coordinates for the mine to be removed. Represented as a tuple.
        """
        
        self.placed_mines -= 1
        self.mine_coords.pop(coords)
        self.update_nums(coords)
        new_mine = self.place_mines(True)
        self.update_nums(new_mine)
        self.mine_coords[new_mine] = new_mine

    def is_mine(self, coords):
        """is_mine
        Arguments:
            coords: Coordinates to check for a mine. Represented as a tuple.
        Returns:
            A boolean value. True if the coordinates contain a mine, False if they do not.
        """
        
        element = self.the_board[coords[0]][coords[1]]
        if element == [9] or element == "X":
            return True
        else:
            return False

    def reveal_turn(self, coords):
        """reveal_turn changes the hidden tile to a revealed value, either a mine or an integer.
        Arguments:
            coords: Coordinates at which to reveal a turn. Represented as a tuple.
        """
        
        element = self.the_board[coords[0]][coords[1]]
        if self.is_mine(coords):
            self.the_board[coords[0]][coords[1]] = "X"
        else:
            self.the_board[coords[0]][coords[1]] = element[0]
            self.revealed_count += 1

    def find_mines(self):
        """find_mines takes a look at all the integers on the board and deduces the locations of mines based off of the surrounding tiles of these integers.
        """
        
        self.no_mines = {}
        for each_int_tile in self.int_coords:
            hidden_tiles = self.indices_around_coord(each_int_tile, False, only_hidden = True)
            num_bombs = 0
            int_tile_val = self.the_board[each_int_tile[0]][each_int_tile[1]]
            #print(self.marked_mines.keys())
            if int_tile_val == len(hidden_tiles):
                #print(each_int_tile)
                for each_hidden in hidden_tiles:
                    self.marked_mines[each_hidden] = None
            for each_hidden in hidden_tiles:
                if each_hidden in self.marked_mines:
                    #print("hidden: ", each_hidden, "int_tile: ", each_int_tile, "tile_val: ", int_tile_val)
                    num_bombs += 1
            if int_tile_val - num_bombs <= 0:
                #if num_hidden == int_tile_val and int_tile_val != 1:
                #    continue
                for each_hidden in hidden_tiles:
                    if each_hidden not in self.marked_mines:
                        self.move_priority_queue.insert([each_hidden, 0])
                        #print("EH: ", each_hidden)
                        self.no_mines[each_hidden] = None
        #print("No Mines: ", self.no_mines.keys())
        #print("Mines: ", self.marked_mines.keys())
    
    def clear_path(self, coords):
        """clear_path takes coordinates and clears all hidden tiles around it recursively until non-zero values are encountered.
        Arguments:
            coords: Coordinates at which the clear_path algorithm should originate at. Represented as a tuple.
        """
        
        board_tile = self.the_board[coords[0]][coords[1]]
        if self.turn_count == 0 or board_tile == [0]:
            surrounding_list = self.indices_around_coord(coords, only_hidden = True)
            surrounding_list.append(coords) 
        else:
            surrounding_list = [coords]
        for each_tile in surrounding_list:
            tile_value = self.the_board[each_tile[0]][each_tile[1]]
            if tile_value == [0]:
                for each_surrounding_tile in self.indices_around_coord(each_tile, False, True):
                    if each_surrounding_tile not in surrounding_list:
                        surrounding_list.append(each_surrounding_tile)
            if not self.is_mine(each_tile) and type(tile_value) != int:
                self.reveal_turn(each_tile)
            tile_value = self.the_board[each_tile[0]][each_tile[1]]
            if type(tile_value) == int and tile_value != 0:
                insert_tiles = self.indices_around_coord(each_tile, False, True)
                for each_insert_tile in insert_tiles:
                    self.move_priority_queue.insert([each_insert_tile, self.tile_weight(each_insert_tile)])
                self.int_coords.append(each_tile)
        self.find_mines()
            
    def turn_one_mine_check(self, coords):
        """turn_one_mine_check checks to see if there is a mine at the location of the first player turn. If there is the mine is shifted elsewhere so that the game can continue.
        Arguments:
            coords: Coordinates at which the first turn was executed at. Represented as a tuple.
        """
        
        element = self.the_board[coords[0]][coords[1]]
        while element == "X" or element == [9]:
            self.remove_mine(coords)
            element = self.the_board[coords[0]][coords[1]]

    def coord_weight(self, coords):
        """coord_weight returns an integer weight of a tile (determined by its value), if the tile is hidden, returns an arbitrary value.
        Arguments:
            coords: Coordinates of the tile to get a weight for.
        Returns:
            An integer representing a weight.
        """
        
        if type(self.the_board[coords[0]][coords[1]]) == list:
            return 0
        else:
            return self.the_board[coords[0]][coords[1]]
        
    def tile_weight(self, coords):
        """tile_weight returns the weight of a hidden tile, determined by the weights of all of its surrounding tiles.
        Arguments:
            coords: Coordinates of a hidden tile to get a weight for.
        Returns:
            A double representing a weight.
        """
        
        surrounding = self.indices_around_coord(coords)
        weight = 0
        num_nums = 0
        for each_tile in surrounding:
            weight += self.coord_weight(each_tile)
        weight = weight / (len(surrounding) - len(self.indices_around_coord(coords, only_hidden = True)) + 1)
        return weight
    
    def find_play(self):
        """find_play loops through the priority queue of potential moves until it finds a viable play, the play is then printed for the player to execute.
        Returns:
            coords: Tuple representation of coordinates (x,y)
        """
        
        if len(self.marked_mines) == self.num_mines:
            for row_index, each_board_row in enumerate(self.the_board):
                for column_index, each_board_tile in enumerate(each_board_row):
                    if type(each_board_tile) == list and (row_index, column_index) not in self.marked_mines:
                        self.move_priority_queue.insert([(row_index, column_index), 0])
        tile_wt = self.tile_weight(self.move_priority_queue.find_min()[0])
        stored_wt = self.move_priority_queue.find_min()[1]
        min_val = self.move_priority_queue.find_min()
        while (type(self.the_board[min_val[0][0]][min_val[0][1]]) == int) or (tile_wt != stored_wt and stored_wt != 0) or (min_val[0] in self.marked_mines): #or (min_val[0] not in self.no_mines):
            self.move_priority_queue.remove_min()
            if tile_wt != stored_wt:
                self.move_priority_queue.insert([min_val[0], tile_wt])
            min_val = self.move_priority_queue.find_min()
            tile_wt = self.tile_weight(min_val[0])
            stored_wt = min_val[1]
        print("SOLVER\nRow: ", min_val[0][0]+1, "Column: ", min_val[0][1]+1, "Weight: ", stored_wt)
        #print(self.move_priority_queue.find_min()[1])
        return min_val[0]

    def get_player_input(self):
        """get_player_input asks the player for row and column coordinates at which a move will be executed.
        Returns:
            Tuple containing coordinates of the next move to be made.
        """
        
        x = None
        y = None
        tile_selection = -1
        while type(tile_selection) == int:
            while (type(x) != int) or (x < 0) or (x > self.rows):
                try:
                    x = int(input("Please enter a valid row number: ")) - 1
                except ValueError:
                    pass #Input was not an integer type
            while (type(y) != int) or (y < 0) or (y > self.columns):
                try:
                    y = int(input("Please enter a valid column number: ")) - 1
                except ValueError:
                    pass #Input column was not an integer type
            coords = (x,y)
            tile_selection = self.the_board[coords[0]][coords[1]]
            x = None
            y = None
        return coords

    def is_game_lost(self, coords):
        """is_game_lost 
        Arguments:
            coords: Coordinates at which the game will check for mines at to determine game status. Returns True if game is lost due to player hitting a mine, False otherwise.
        Returns:
            Boolean
        """
        
        if self.is_mine(coords):
            return True
        else:
            return False

    def is_game_won(self):
        """is_game_won returns True if the player won the game in the current game status, False if they lost.
        Returns:
            Boolean
        """
        
        if self.revealed_count == (self.rows*self.columns - self.num_mines):
            return True
        else:
            return False

    def game_over(self, coords):
        """game_over returns True or False depending on whether or not the game is over.
        Arguments:
            coords: Coordinates at which the most recent turn was executed at. Represented as a tuple.
        Returns:
            A boolean value. True if the game is over, False if it is not.
        """
        
        if self.is_game_lost(coords):
            self.reveal_turn(coords)
            self.print_board()
            print("Game over! You lost!")
            return True
        elif self.is_game_won():
            self.print_board()
            print("Game over! You won!")
            return True
        else:
            return False
    
    def player_turns(self):
        """player_turns initiates the game for the player."""
        
        game_over = False
        while game_over == False:
            #coords = self.get_player_input()
            if self.turn_count == 0:
                coords = (5,5)
                self.turn_one_mine_check(coords)
            else:
                #coords = self.get_player_input()
                coords = self.find_play()
            self.clear_path(coords)
            if self.game_over(coords):
                game_over = True
                return self.is_game_won()
            else:
                tile_selection = -1
                self.print_board()
                self.turn_count += 1
                #self.find_play()

def play_minesweeper(wins, losses):
    
    print("Hello! This is my own implementation of minesweeper.")
    #rows = input("Please enter the number of rows you would like to have in the game board: ")
    #columns = input("Please enter the number of columns you would like to have in the game board: ")
    #mines = input("Please enter the number of mines you would like to have randomly generated across the board: ")
    rows = 9
    columns = 9
    mines = 10
    game = Board(int(rows), int(columns), int(mines))
    #print(game)
    status = game.player_turns()
    if status == True:
        wins += 1
    else:
        losses += 1
    print("wins: ", wins)
    print("losses: ", losses)
    #play_again = input("Would you like to play again? Enter y or n: ")
    #if play_again == "y":
    play_minesweeper(wins, losses)

wins = 0
losses = 0
play_minesweeper(wins, losses)
