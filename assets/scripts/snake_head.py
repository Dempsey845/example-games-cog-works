import math

import pygame
from cogworks import GameObject
from cogworks.components.script_component import ScriptComponent
from cogworks.components.sprite import Sprite
from cogworks.components.trigger_collider import TriggerCollider
from cogworks.pygame_wrappers.input_manager import InputManager

from assets.scripts.snake_body_part import SnakeBodyPart


class SnakeHead(ScriptComponent):

    def __init__(self, on_game_over, speed: int = 100, gap: int = 15):
        super().__init__()

        self.on_game_over = on_game_over
        self.speed = speed
        self.gap = gap

        self.move_direction = (0, 0)
        self.body_parts = []

        self.head_pos = (0, 0)
        self.positions = [self.head_pos]

        self.segment_distances = []

        self.sprite = None
        self.camera = None

        self.input_manager = InputManager.get_instance()

    def start(self):
        self.head_pos = self.game_object.transform.get_local_position()
        self.sprite = self.game_object.get_component(Sprite)
        self.camera = self.game_object.scene.camera_component

        self.game_object.add_component(TriggerCollider(layer="Head", layer_mask=["BodyPart"], debug=True))
        first_head_part = GameObject("FirstHeadPart")
        first_head_part.add_component(SnakeBodyPart("images/player.png"))
        self.game_object.add_child(first_head_part)
        self.body_parts.append(first_head_part)

    def update(self, dt):
        x, y = (0, 0)

        if self.input_manager.is_key_down(pygame.K_LEFT):
            x = -1
        if self.input_manager.is_key_down(pygame.K_RIGHT):
            x = 1
        if self.input_manager.is_key_down(pygame.K_UP):
            y = -1
        if self.input_manager.is_key_down(pygame.K_DOWN):
            y = 1

        self.move_direction = (x, y)
        self.move_head(dt)
        self.update_body_parts()

    def render(self, surface):
        pass

    def move_head(self, dt):
        """Move the head according to the current move direction and check camera boundaries."""
        head_x, head_y = self.game_object.transform.get_local_position()
        dx, dy = self.move_direction
        new_head_pos = (head_x + dx * dt * self.speed, head_y + dy * dt * self.speed)
        self.game_object.transform.set_local_position(new_head_pos[0], new_head_pos[1])
        self.positions.insert(0, new_head_pos)  # add to history

        # Screen boundary collision check
        w = self.sprite.get_width()
        h = self.sprite.get_height()

        top, bottom, left, right = self.camera.get_bounds()

        out_of_bounds = new_head_pos[1] - h / 2 < top or new_head_pos[1] + h / 2 > bottom or new_head_pos[0] - w / 2 < left or new_head_pos[0] + w / 2 > right

        if out_of_bounds:
            self.on_game_over()

    def update_body_parts(self):
        """Update each body part smoothly along the positions path."""
        for i, body_part in enumerate(self.body_parts):
            distance_needed = self.segment_distances[i]
            accumulated = 0
            last_pos = self.positions[0]

            for j in range(1, len(self.positions)):
                pos = self.positions[j]
                dx = pos[0] - last_pos[0]
                dy = pos[1] - last_pos[1]
                step = math.hypot(dx, dy)

                if accumulated + step >= distance_needed:
                    remain = distance_needed - accumulated
                    t = remain / step if step != 0 else 0
                    interp_x = last_pos[0] + dx * min(t, 1)
                    interp_y = last_pos[1] + dy * min(t, 1)
                    body_part.rect_transform.set_position((interp_x, interp_y))
                    break

                accumulated += step
                last_pos = pos
            else:
                # If distance_needed exceeds history, use last recorded position
                body_part.rect_transform.set_position(self.positions[-1])

            body_part.update()

    # ---------------- Utility Methods ----------------
    def calculate_segments(self):
        """Calculate distance along the path for each body part."""
        segment_width = self.sprite.get_width()
        self.segment_distances = [
            (i + 1) * (segment_width + self.gap)
            for i in range(len(self.body_parts))
        ]

    def update_move_direction(self, move_direction):
        self.move_direction = move_direction