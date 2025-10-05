import pygame
from collections import deque

from assets.scripts.apple import Apple
from cogworks import GameObject
from cogworks.components.script_component import ScriptComponent
from cogworks.components.sprite import Sprite
from cogworks.components.trigger_collider import TriggerCollider
from cogworks.pygame_wrappers.input_manager import InputManager

from assets.scripts.snake_body_part import SnakeBodyPart


class SnakeHead(ScriptComponent):
    def __init__(self, grid, move_interval: float = 0.1):
        super().__init__()
        self.move_interval = move_interval
        self.grid = grid

        self.move_direction = (0, 0)
        self.move_timer = 0
        self.can_move = True

        self.sprite = None
        self.camera = None

        # store world positions that body parts will follow
        self.position_history = deque(maxlen=5000)

        self.body_parts = []
        self.input_manager = InputManager.get_instance()

    def start(self):
        self.sprite = self.game_object.get_component(Sprite)
        self.camera = self.game_object.scene.camera_component
        # When we add a component we should tell that component whether it was added in start so that
        # we can use this in scene_manager to prevent saying a copy of it
        self.game_object.add_component(
            TriggerCollider(layer="Head", layer_mask=["BodyPart", "Apple"], debug=True), runtime=True
        )
        x, y = self.grid.get_random_point_in_grid_cell()
        self.game_object.transform.set_local_position(x, y)

        self.add_new_apple()

        for _ in range(3):
            self.add_body_part()

    def update(self, dt):
        if not self.can_move:
            return

        # Timer
        self.move_timer += dt
        if self.move_timer >= self.move_interval:
            self.move_timer = 0
            self.move_head()

            # Update direction once per movement
            x, y = self.move_direction
            new_direction = self.move_direction

            if self.input_manager.is_key_down(pygame.K_LEFT) and x != 1:
                new_direction = (-1, 0)
            elif self.input_manager.is_key_down(pygame.K_RIGHT) and x != -1:
                new_direction = (1, 0)
            elif self.input_manager.is_key_down(pygame.K_UP) and y != 1:
                new_direction = (0, -1)
            elif self.input_manager.is_key_down(pygame.K_DOWN) and y != -1:
                new_direction = (0, 1)

            self.move_direction = new_direction

    def on_trigger_enter(self, other):
        if other.layer == "Apple":
            self.add_body_part()
            self.add_new_apple()
            other.game_object.destroy()

    def move_head(self):
        head_x, head_y = self.game_object.transform.get_world_position()

        dx, dy = self.move_direction
        step_x = dx * self.sprite.get_width()
        step_y = dy * self.sprite.get_height()
        new_pos = (head_x + step_x, head_y + step_y)
        self.game_object.transform.set_world_position(*new_pos)

        self.position_history.appendleft(new_pos)

        # move body parts
        for index, part in enumerate(self.body_parts, start=1):
            if len(self.position_history) > index:
                part.transform.set_world_position(*self.position_history[index])

        # boundary check
        w, h = self.sprite.get_width(), self.sprite.get_height()
        top, bottom, left, right = self.camera.get_bounds()
        if (
            new_pos[1] - h / 2 < top
            or new_pos[1] + h / 2 > bottom
            or new_pos[0] - w / 2 < left
            or new_pos[0] + w / 2 > right
        ):
            self.on_game_over()

    def add_new_apple(self):
        apple = GameObject("Apple")

        x, y = self.grid.get_random_point_in_grid_cell()

        apple.transform.set_world_position(x, y)
        apple.transform.set_local_scale(0.5)
        apple.add_component(Apple())
        self.game_object.scene.add_game_object(apple)

    def add_body_part(self):
        body_part = GameObject("BodyPart")
        script = SnakeBodyPart(head=self, sprite_image_path="images/snake_part.png")
        body_part.add_component(script)
        self.game_object.add_child(body_part)

        # start at head position
        body_part.transform.set_world_position(*self.game_object.transform.get_world_position())
        self.body_parts.append(body_part)

    def on_game_over(self):
        self.move_direction = (0, 0)
        self.can_move = False
