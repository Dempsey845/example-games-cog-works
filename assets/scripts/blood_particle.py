import random
from cogworks.components.script_component import ScriptComponent
from cogworks.components.sprite import Sprite


class BloodParticle(ScriptComponent):
    def __init__(
        self,
        min_x: float = 0,
        max_x: float = 50,
        min_y: float = 0,
        max_y: float = 50,
        min_rotation: float = -180,
        max_rotation: float = 180,
        min_scale: float = 0.4,
        max_scale: float = 0.8,
        move_speed: float = 500,
        gravity: float = 500,
        min_direction: tuple[float, float] = (-1, -1),
        max_direction: tuple[float, float] = (1, 1),
        lifetime: float = 1.5,
        end_scale: float = 0.1,
    ):
        super().__init__()
        self.min_x = min_x
        self.max_x = max_x
        self.min_y = min_y
        self.max_y = max_y
        self.min_rotation = min_rotation
        self.max_rotation = max_rotation
        self.min_scale = min_scale
        self.max_scale = max_scale
        self.move_speed = move_speed
        self.gravity = gravity
        self.min_direction = min_direction
        self.max_direction = max_direction
        self.lifetime = lifetime
        self.end_scale = end_scale

        self.age = 0.0
        self.initial_scale = 1.0

        # Movement state
        self.direction: list[float] = [0.0, 0.0]
        self.velocity: list[float] = [0.0, 0.0]

    def start(self) -> None:
        # Randomise initial position, rotation, and scale
        random_x = random.uniform(self.min_x, self.max_x)
        random_y = random.uniform(self.min_y, self.max_y)
        random_rotation = random.uniform(self.min_rotation, self.max_rotation)
        random_scale = random.uniform(self.min_scale, self.max_scale)
        self.initial_scale = random_scale  # store starting scale for interpolation

        # Randomise initial direction
        random_x_dir = random.uniform(self.min_direction[0], self.max_direction[0])
        random_y_dir = random.uniform(self.min_direction[1], self.max_direction[1])
        self.direction = [random_x_dir, random_y_dir]

        # Set initial velocity based on direction
        self.velocity = [
            self.direction[0] * self.move_speed,
            self.direction[1] * self.move_speed,
        ]

        # Apply initial transform
        self.game_object.transform.set_local_position(random_x, random_y)
        self.game_object.transform.set_local_rotation(random_rotation)
        self.game_object.transform.set_local_scale(random_scale, random_scale)

        # Add sprite
        sprite = Sprite("images/blood_particle.png")
        self.game_object.add_component(sprite)

    def update(self, dt: float) -> None:
        self.age += dt
        t = min(self.age / self.lifetime, 1.0)  # progress ratio (0 → 1)

        # Destroy when lifetime ends
        if self.age >= self.lifetime:
            self.game_object.destroy()
            return

        # Apply gravity
        self.velocity[1] += self.gravity * dt

        # Update position
        pos_x, pos_y = self.game_object.transform.get_local_position()
        new_x = pos_x + self.velocity[0] * dt
        new_y = pos_y + self.velocity[1] * dt
        self.game_object.transform.set_local_position(new_x, new_y)

        #Scale linearly from initial_scale to end_scale over lifetime
        new_scale = self.initial_scale + (self.end_scale - self.initial_scale) * t
        self.game_object.transform.set_local_scale(new_scale, new_scale)
