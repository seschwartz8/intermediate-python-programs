"""
Student portion of Zombie Apocalypse mini-project
by Sarah Schwartz
"""

# these are imported from other Code Skulptor files made by Rice University
import random
import poc_grid
import poc_queue
import poc_zombie_gui

# global constants
EMPTY = 0 
FULL = 1
FOUR_WAY = 0
EIGHT_WAY = 1
OBSTACLE = 5
HUMAN = 6
ZOMBIE = 7


class Apocalypse(poc_grid.Grid):
    """
    Class for simulating zombie pursuit of human on grid with
    obstacles
    """

    def __init__(self, grid_height, grid_width, obstacle_list = None, 
                 zombie_list = None, human_list = None):
        """
        Create a simulation of given size with given obstacles,
        humans, and zombies
        """
        poc_grid.Grid.__init__(self, grid_height, grid_width)
        if obstacle_list != None:
            for cell in obstacle_list:
                self.set_full(cell[0], cell[1])
        else:
            self._obstacle_list = []
        if zombie_list != None:
            self._zombie_list = list(zombie_list)
        else:
            self._zombie_list = []
        if human_list != None:
            self._human_list = list(human_list)  
        else:
            self._human_list = []
        
    def clear(self):
        """
        Set cells in obstacle grid to be empty
        Reset zombie and human lists to be empty
        """
        poc_grid.Grid.clear(self)
        self._zombie_list = []
        self._human_list = []
        
        
    def add_zombie(self, row, col):
        """
        Add zombie to the zombie list
        """
        self._zombie_list.append([row, col])
                
    def num_zombies(self):
        """
        Return number of zombies
        """
        return len(self._zombie_list)     
    
    def clear_zombies(self):
        """
        Clear zombie list only
        """
        self._zombie_list = []
          
    def zombies(self):
        """
        Generator that yields the zombies in the order they were
        added.
        """
        index = 0
        while index < self.num_zombies():
            yield tuple(self._zombie_list[index])
            index = index + 1

    def add_human(self, row, col):
        """
        Add human to the human list
        """
        self._human_list.append([row, col])
        
    def clear_humans(self):
        """
        Clear human list only
        """
        self._human_list = []
        
    def num_humans(self):
        """
        Return number of humans
        """
        return len(self._human_list)  
    
    def humans(self):
        """
        Generator that yields the humans in the order they were added.
        """
        index = 0
        while index < self.num_humans():
            yield tuple(self._human_list[index])
            index = index + 1
        
    def compute_distance_field(self, entity_type):
        """
        Function computes and returns a 2D distance field
        Distance at member of entity_list is zero
        Shortest paths avoid obstacles and use four-way distances
        Manhattan distance = abs(x0-x1) + abs(y0-y1)
        """
        # Create grid of same size to track visited cells
        visited_grid = poc_grid.Grid(self._grid_height, self._grid_width)
        # Create 2D list with each entry initialized as product of heigh times width of grid
        distance_field = [[(self._grid_height * self._grid_width)
                           for col in range(self._grid_width)]
                           for row in range(self._grid_height)]
        # Create queue boundary that's a copy of the human or zombie list
        boundary = poc_queue.Queue()
        if entity_type == ZOMBIE:
            target_list = self.zombies()
        elif entity_type == HUMAN:
            target_list = self.humans()
        for cell in list(target_list):
            boundary.enqueue(cell)
        # Initialize cells in boundary queue to be visited (FULL) and distance to 0
        for cell in boundary:
            visited_grid.set_full(cell[0], cell[1])
            distance_field[cell[0]][cell[1]] = 0
        # For each inner neighbor of each zombie/human cell, check if visited and passable
        for cell in boundary:
            for neighbor_cell in self.four_neighbors(cell[0], cell[1]):
                if (visited_grid.is_empty(neighbor_cell[0], neighbor_cell[1])):
                    # Add neighbor to visited list and boundary
                    visited_grid.set_full(neighbor_cell[0], neighbor_cell[1])
                    boundary.enqueue(neighbor_cell)
                    # Update neighbor's distance to be current cell + 1
                    distance_field[neighbor_cell[0]][neighbor_cell[1]] = (distance_field[cell[0]][cell[1]] + 1)
        return distance_field
    
    def move_humans(self, zombie_distance_field):
        """
        Function that moves humans away from zombies, diagonal moves
        are allowed
        """
        new_humans = []
        for human in list(self.humans()):
            # Calculate all cells neighboring human
            neighbors = self.eight_neighbors(human[0], human[1])
            # Calculate distance from zombies of each neighboring cell
            largest_distance = zombie_distance_field[human[0]][human[1]]
            best_position = human
            for neighbor in neighbors:
                if self.is_empty(neighbor[0], neighbor[1]):
                    distance = zombie_distance_field[neighbor[0]][neighbor[1]]
                    if distance > largest_distance:
                        largest_distance = distance
                        best_position = neighbor
            # Store best position for refreshed human list
            new_humans.append(best_position)
        # Clear initial human list and replace with best positions
        self.clear_humans()
        for position in new_humans:
            self.add_human(position[0], position[1])
            
        
            

    
    def move_zombies(self, human_distance_field):
        """
        Function that moves zombies towards humans, no diagonal moves
        are allowed
        """
        new_zombies = []
        for zombie in list(self.zombies()):
            # Calculate all cells neighboring zombie (no diagonals)
            neighbors = self.four_neighbors(zombie[0], zombie[1])
            # Calculate distance from humans of each neighboring cell
            smallest_distance = human_distance_field[zombie[0]][zombie[1]]
            best_position = zombie
            for neighbor in neighbors:
                if self.is_empty(neighbor[0], neighbor[1]):
                    distance = human_distance_field[neighbor[0]][neighbor[1]]
                    if distance < smallest_distance:
                        smallest_distance = distance
                        best_position = neighbor
            # Store best position for refreshed zombie list
            new_zombies.append(best_position)
        # Clear initial zombie list and replace with best positions
        self.clear_zombies()
        for position in new_zombies:
            self.add_zombie(position[0], position[1])

    


poc_zombie_gui.run_gui(Apocalypse(30, 40))
