"""
    Pygame of life module. Contains the short engine
    to simulate the grid of life.
    Also, we have different variants of game of life.

    We can decide if we implement one of the variants or
    multiple variants in the update_functions array in
    main def. I leave a comment to know what kind of
    variants can use.

    Variants:
    - High life: Similar to game of life, but a dead
    cell with exactly 6 dead neighbours can return to life.
    - Day & night: A dead cell survives if has 3,4,6,7 or 8
     live neighbours, a dead cell revive if has 3,6,7 or 8
     live neighbours.
    - Seeds: Live cells always die (they don't survive
    through generations). A dead cell with exactly 2 live
    neighbours return to life.
"""

import sys
import time
import random

import pygame

from grid_defs import Grid, Neighbours, Dim
from collections import defaultdict
from copy import deepcopy
from grid_defs import Grid, Neighbours


def get_neighbours(grid: Grid, x: int, y: int) -> Neighbours:
    """
        Gets the neighbour states for a particular cell in
        (x, y) on the grid.
    """
    offsets = [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]
    possible_neighbours = {(x + x_add, y + y_add) for x_add, y_add in offsets}
    alive = {(pos[0], pos[1]) for pos in possible_neighbours if pos in grid.cells}
    return Neighbours(alive, possible_neighbours - alive)


def update_grid(grid: Grid) -> Grid:
    """
        Given a grid, this function returns the next iteration
        of the game of life.
    """
    new_cells = deepcopy(grid.cells)
    undead = defaultdict(int)

    for x, y in grid.cells:
        alive_neighbours, dead_neighbours = get_neighbours(grid, x, y)
        if len(alive_neighbours) not in [2, 3]:
            new_cells.remove((x, y))

        for pos in dead_neighbours:
            undead[pos] += 1

    for pos, _ in filter(lambda elem: elem[1] == 3, undead.items()):
        new_cells.add((pos[0], pos[1]))

    return Grid(grid.dim, new_cells)


def draw_grid(screen: pygame.Surface, grid: Grid) -> None:
    """
        This function draws the game of life on the given
        pygame.Surface object.
    """
    cell_width = screen.get_width() / grid.dim.width
    cell_height = screen.get_height() / grid.dim.height
    border_size = 2

    for x, y in grid.cells:
        pygame.draw.rect(
            screen,
            (255, 0, 0),
            (
                x * cell_width + border_size,
                y * cell_height + border_size,
                cell_width - border_size,
                cell_height - border_size,
            ),
        )


def generate_random_grid(dim: Dim, live_cell_probability: float) -> Grid:
    """
        Generates a random grid with a given live cell probability.
    """
    cells = set()
    for x in range(dim.width):
        for y in range(dim.height):
            if random.random() < live_cell_probability:
                cells.add((x, y))
    return Grid(dim, cells)

"""
    Variants of update functions for the game of life.
"""

def update_grid_highlife(grid: Grid) -> Grid:
    """
        Conway's game of life varaint:
        Similar to game of life, but a dead
        cell with exactly 6 dead neighbours can return to life.
    """
    new_cells = deepcopy(grid.cells)
    undead = defaultdict(int)

    for x, y in grid.cells:
        alive_neighbours, dead_neighbours = get_neighbours(grid, x, y)
        if len(alive_neighbours) not in [2, 3]:
            new_cells.remove((x, y))

        for pos in dead_neighbours:
            undead[pos] += 1

    for pos, count in undead.items():
        if count in [3, 6]:
            new_cells.add((pos[0], pos[1]))

    return Grid(grid.dim, new_cells)


def update_grid_day_night(grid: Grid) -> Grid:
    """
        Conway's game of life variant:
        A dead cell survives if has 3,4,6,7 or 8
        live neighbours, a dead cell revive if has 3,6,7 or 8
        live neighbours.
    """
    new_cells = deepcopy(grid.cells)
    undead = defaultdict(int)

    for x, y in grid.cells:
        alive_neighbours, dead_neighbours = get_neighbours(grid, x, y)
        if len(alive_neighbours) not in [3, 4, 6, 7, 8]:
            new_cells.remove((x, y))

        for pos in dead_neighbours:
            undead[pos] += 1

    for pos, count in undead.items():
        if count in [3, 6, 7, 8]:
            new_cells.add((pos[0], pos[1]))

    return Grid(grid.dim, new_cells)


def update_grid_seeds(grid: Grid) -> Grid:
    """
        Conway's game of life variant.
        Live cells always die (they don't survive
        through generations). A dead cell with exactly 2 live
        neighbours return to life.
    """
    new_cells = deepcopy(grid.cells)
    undead = defaultdict(int)

    for x, y in grid.cells:
        alive_neighbours, dead_neighbours = get_neighbours(grid, x, y)
        # All cells die, so no need to check alive_neighbours for living cells

        for pos in dead_neighbours:
            undead[pos] += 1

    for pos, count in undead.items():
        if count == 2:
            new_cells.add((pos[0], pos[1]))

    return Grid(grid.dim, new_cells)



def main():
    """
        Main entry point
    """
    dim = Dim(200, 200)
    grid = generate_random_grid(dim, 0.1)  # 10% probability for a cell to be alive

    pygame.init()
    screen = pygame.display.set_mode((1000, 700))
    # Here we can update "gamemodes" or game variants
    # We can choose between one or multiple game variants at the same time
    # Variant def names:
    # update_grid_highlife
    # update_grid_day_night
    # update_grid_seeds
    # update_grid
    update_functions = [update_grid]

    while True:
        if pygame.QUIT in [e.type for e in pygame.event.get()]:
            sys.exit(0)

        # Of the selected variants, we randomize the selection of the variant per 'round'
        update_function = random.choice(update_functions)
        grid = update_function(grid)

        # Set title of window with the name of the game variant
        pygame.display.set_caption(f"Game of Life - {update_function.__name__}")

        screen.fill((0, 0, 0))
        draw_grid(screen, grid)
        pygame.display.flip()
        time.sleep(0.1)


if __name__ == "__main__":
    main()
