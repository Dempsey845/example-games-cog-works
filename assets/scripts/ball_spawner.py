from random import random

from cogworks import GameObject
from cogworks.components.rigidbody2d import Rigidbody2D
from cogworks.components.script_component import ScriptComponent
from cogworks.components.sprite import Sprite
from cogworks.components.trigger_collider import TriggerCollider
from cogworks.pygame_wrappers.window import Window


class BallSpawner(ScriptComponent):
    def __init__(self):
        super().__init__()

    def start(self) -> None:
        window_width, _ = Window.get_instance().get_size()
        ball_count = 0
        for i in range(ball_count):
            scale = random() * 0.5 + 0.5
            ball = GameObject(
                f"Ball{i}",
                x=i * 50,
                y=-600 - (i + 500),
                scale_x=scale,
                scale_y=scale
            )
            ball.add_component(Sprite("images/duck.png"))
            ball.add_component(
                Rigidbody2D(shape_type="circle", radius=100 * scale, debug=False, freeze_rotation=False, friction=0.1))
            ball.add_component(TriggerCollider(shape="circle", radius=int(100 * scale), debug=True, layer="Circle",
                                                 layer_mask=["Spike"]))

            self.game_object.scene.instantiate_game_object(ball)
            # self.game_object.add_child(ball) - discover why runtime children are a lot more expensive (even when destroyed)