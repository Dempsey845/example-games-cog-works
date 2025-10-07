import random
import weakref

import pygame

from cogworks.components.script_component import ScriptComponent

class SnakeGrid(ScriptComponent):
    def __init__(self, camera, cell_size=(20, 20)):
        super().__init__()
        self.camera_ref = weakref.ref(camera)
        self.cell_size = cell_size

    def render(self, surface) -> None:
        # Draw grid
        if self.cell_size == (0, 0):
            return  # grid can't be drawn before size is known

        camera = self.camera_ref()
        if not camera:
            return

        cell_width, cell_height = self.cell_size
        top, bottom, left, right = camera.get_bounds()

        # Convert bounds to integers for range
        top = int(top)
        bottom = int(bottom)
        left = int(left)
        right = int(right)

        grid_color = (40, 40, 40)

        # Draw vertical grid lines
        x = left - (left % cell_width)
        while x < right:
            pygame.draw.line(surface, grid_color, (x, top), (x, bottom))
            x += cell_width

        # Draw horizontal grid lines
        y = top - (top % cell_height)
        while y < bottom:
            pygame.draw.line(surface, grid_color, (left, y), (right, y))
            y += cell_height

    def get_random_point_in_grid_cell(self, margin=1):
        """Return a random point positioned in the middle of a grid cell, optionally ignoring edges by 'margin' cells."""
        camera = self.camera_ref()
        if not camera:
            return 0, 0

        cell_w, cell_h = self.cell_size
        top, bottom, left, right = camera.get_bounds()

        # Compute how many grid cells fit in the visible area
        cols = int((right - left) // cell_w)
        rows = int((bottom - top) // cell_h)

        # Make sure margin doesn't exceed half the grid size
        margin = min(margin, cols // 2, rows // 2)

        # Pick a random grid cell, respecting the margin
        rand_col = random.randint(margin, cols - 1 - margin)
        rand_row = random.randint(margin, rows - 1 - margin)

        # Compute the centre of that cell in world coordinates
        x = left + rand_col * cell_w + cell_w / 2
        y = top + rand_row * cell_h + cell_h / 2

        return x, y