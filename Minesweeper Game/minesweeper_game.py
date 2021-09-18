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
        move_priority_queue:
        marked_mines:
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

    def __str__(self) -> str:
        """printing a board instance allows you to see the array making up the board."""
        row_str = ""
        for r in self.the_board:
            row_str += f"{r}\n"
        return row_str
    
    def print_board(self):
        """print_board prints the player-observable game space."""
        main_space = ""
        front_spacing = len(str(self.rows))*" "
        top_bottom_edges = front_spacing + (self.columns + 2)*" -" + "\n"
        column_labels = "   " + front_spacing
        for row_index, board_row in enumerate(self.the_board):
            for column_index, board_column in enumerate(board_row):
                front_spacing = (len(str(self.rows))-len(str(row_index+1))+1)*" "
                main_space += f"{row_index+1}" + front_spacing + "| " if (not column_index%self.columns) else " "
                main_space += "*" if (type(board_column) != int and board_column != "X") else f"{board_column}"
            main_space += f" | {row_index+1}\n"
        column_labels += f"\n{column_labels}".join([" ".join(elem) for elem in itertools.zip_longest(*(str(i) for i in range(1,self.columns+1)), fillvalue=" ")]) + "\n"
        header = column_labels + top_bottom_edges
        footer = top_bottom_edges + column_labels
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
        while self.placed_mines < self.num_mines:
            #print(self)
            x = random.randrange(self.rows)
            y = random.randrange(self.columns)
            if self.the_board[x][y] != [9] or "X":
                self.the_board[x][y] = [9]
                self.mine_coords[(x,y)] = (x,y)
                self.placed_mines += 1
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
        n_indices = coord[0]-1, coord[1]
        e_indices = coord[0], coord[1]+1
        s_indices = coord[0]+1, coord[1]
        w_indices = coord[0], coord[1]-1
        ne_indices = coord[0]-1, coord[1]+1
        se_indices = coord[0]+1, coord[1]+1
        sw_indices = coord[0]+1, coord[1]-1
        nw_indices = coord[0]-1, coord[1]-1
        if adjacent == False:
            surrounding_indices = [n_indices, e_indices, s_indices, w_indices, ne_indices, se_indices, sw_indices, nw_indices]
        else:
            surrounding_indices = [n_indices, e_indices, s_indices, w_indices]
            
        output_indices = []
        for each_coord in surrounding_indices:
            if each_coord[0] < self.rows and each_coord[0] >= 0 and each_coord[1] < self.columns and each_coord[1] >= 0: #Makes sure that the coordinates are within the bounds of the game board.
                if only_hidden:
                    if self.the_board[each_coord[0]][each_coord[1]] == int:
                        continue
                output_indices.append(each_coord)
        #print(coord, output_indices)
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
        self.update_nums(self.place_mines(True))

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
            if type(tile_value) == int:
                insert_tiles = self.indices_around_coord(each_tile, False, True)
                for each_insert_tile in insert_tiles:
                    print("queue_insert: ", each_insert_tile, self.tile_weight(each_insert_tile))
                    self.move_priority_queue.insert([each_insert_tile, self.tile_weight(each_insert_tile)])
            
    def turn_one_mine_check(self, coords):
        """turn_one_mine_check checks to see if there is a mine at the location of the first player turn. If there is the mine is shifted elsewhere so that the game can continue.
        Arguments:
            coords: Coordinates at which the first turn was executed at. Represented as a tuple.
        """
        element = self.the_board[coords[0]][coords[1]]
        while element == "X" or element == [9]:
            self.remove_mine(coords)
            element = self.the_board[coords[0]][coords[1]]
            
    def player_turns(self):
        """player_turns initiates the game for the player."""
        x = None
        y = None
        tile_selection = -1
        game_over = False
        while game_over == False:
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
            if self.turn_count == 0:
                self.turn_one_mine_check(coords)
            self.clear_path(coords)
            if self.game_over(coords):
                game_over = True
                continue
            else:
                tile_selection = -1
                self.print_board()
                self.turn_count += 1
                tile_wt = self.tile_weight(self.move_priority_queue.find_min()[0])
                stored_wt = self.move_priority_queue.find_min()[1]
                min_val = self.move_priority_queue.find_min()
                while (type(self.the_board[min_val[0][0]][min_val[0][1]]) == int) or (tile_wt != stored_wt):
                    if tile_wt != stored_wt:
                        self.move_priority_queue.insert([min_val[0], tile_wt])
                    self.move_priority_queue.remove_min()
                    min_val = self.move_priority_queue.find_min()
                    tile_wt = self.tile_weight(min_val[0])
                    stored_wt = min_val[1]
                print(self.move_priority_queue.find_min()[0][0]+1,self.move_priority_queue.find_min()[0][1]+1)
                print(self.move_priority_queue.find_min()[1])

    def game_over(self, coords):
        """game_over returns True or False depending on whether or not the game is over.
        Arguments:
            coords: Coordinates at which the most recent turn was executed at. Represented as a tuple.
        Returns:
            A boolean value. True if the game is over, False if it is not.
        """
        if self.is_mine(coords):
            self.reveal_turn(coords)
            self.print_board()
            print("Game over! You lost!")
            return True
        elif self.revealed_count == (self.rows*self.columns - self.num_mines):
            self.print_board()
            print("Game over! You won!")
            return True
        else:
            return False

    def coord_weight(self, coords):
        """coord_weight
        """
        if type(self.the_board[coords[0]][coords[1]]) == list:
            return 0
        else:
            return self.the_board[coords[0]][coords[1]]
        
    def tile_weight(self, coords):
        """
        """
        surrounding = self.indices_around_coord(coords)
        weight = 0*len(surrounding)
        for each_tile in surrounding:
            weight += self.coord_weight(each_tile)
        return weight
            
def play_minesweeper():
    print("Hello! This is my own implementation of minesweeper.")
    rows = input("Please enter the number of rows you would like to have in the game board: ")
    columns = input("Please enter the number of columns you would like to have in the game board: ")
    mines = input("Please enter the number of mines you would like to have randomly generated across the board: ")
    game = Board(int(rows), int(columns), int(mines))
    print(game)
    game.player_turns()
    play_again = input("Would you like to play again? Enter y or n: ")
    if play_again == "y":
        play_minesweeper()
        
play_minesweeper()
