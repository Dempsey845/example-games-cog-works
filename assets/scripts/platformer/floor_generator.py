import random
from cogworks.components.rigidbody2d import Rigidbody2D
from cogworks.components.script_component import ScriptComponent
from cogworks.components.sprite import Sprite
from cogworks.components.trigger_collider import TriggerCollider
from cogworks.game_object import GameObject
from assets.scripts.platformer.platform import Platform

class FloorGenerator(ScriptComponent):
    FLOOR_TEXTURES = ["images/floors/floor_1.png", "images/floors/floor_2.png", "images/floors/floor_3.png"]

    def __init__(self, window_height, floor_width=1000, ground_floor_count=20):
        super().__init__()
        self.window_height = window_height
        self.floor_width = floor_width
        self.ground_floor_count = ground_floor_count

    def start(self) -> None:
        floors = []

        for i in range(self.ground_floor_count):
            base_x = self.floor_width * i

            # --- Base ground floor ---
            floors.append(self._create_floor_data(base_x, self.window_height, scale=2))

            # --- Random small floor near ground ---
            rand_x = base_x + random.randint(-100, 100)
            rand_y = random.randint(0, 50)
            floors.append(self._create_floor_data(rand_x, rand_y, scale=1))

            # --- Upper platforms ---
            if random.random() < 0.7:  # 70% chance to spawn floating platforms
                upper_count = random.randint(2, 5)
                last_y = 0
                for j in range(upper_count):
                    # Larger vertical gaps (approx. double previous)
                    min_y = last_y - 600 - random.randint(0, 100)
                    max_y = min_y + 100  # slightly adjustable
                    y_pos = random.randint(min(min_y, max_y), max(min_y, max_y))
                    x_offset = base_x + random.randint(-200, 200)
                    scale = random.uniform(0.8, 1)
                    floors.append(self._create_floor_data(x_offset, y_pos, scale))
                    last_y = y_pos

        # --- Instantiate floors ---
        for i, floor in enumerate(floors):
            self._instantiate_floor(i, floor)

    # -------------------
    # Helper functions
    # -------------------

    def _create_floor_data(self, x, y, scale=1):
        return {"x": x, "y": y, "scale": scale, "texture": random.choice(self.FLOOR_TEXTURES)}

    def _instantiate_floor(self, index, floor_data):
        floor_object = GameObject(
            f"Floor{index}",
            x=floor_data["x"],
            y=floor_data["y"],
            scale_x=floor_data["scale"],
            scale_y=floor_data["scale"]
        )
        floor_sprite = Sprite(floor_data["texture"])
        floor_object.add_component(floor_sprite)
        floor_object.add_component(
            Rigidbody2D(
                static=True,
                debug=False,
                width=floor_sprite.get_width() * floor_data["scale"],
                height=floor_sprite.get_height() * floor_data["scale"]
            )
        )
        floor_object.add_component(TriggerCollider())
        floor_object.add_component(Platform())
        self.game_object.scene.instantiate_game_object(floor_object)
