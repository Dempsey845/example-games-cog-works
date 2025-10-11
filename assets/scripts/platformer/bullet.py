from cogworks.components.script_component import ScriptComponent
from cogworks.components.sprite import Sprite
from cogworks.components.trigger_collider import TriggerCollider


class Bullet(ScriptComponent):

    def __init__(self):
        super().__init__()
        self.speed = 2500
        self.lifespan = 1
        self.lifetime = 0.0

    def start(self):
        self.game_object.add_component(Sprite("images/bullet.png"))
        self.game_object.add_component(TriggerCollider(layer="Bullet", layer_mask=["Enemy"], debug=True))

    def update(self, dt):
        forward = self.game_object.transform.get_forward()
        pos_x, pos_y = self.game_object.transform.get_local_position()

        # Move in the forward direction scaled by speed and delta time
        move_x = forward[0] * self.speed * dt
        move_y = forward[1] * self.speed * dt

        self.game_object.transform.set_local_position(pos_x + move_x, pos_y + move_y)

        self.lifetime += dt
        if self.lifetime >= self.lifespan:
            self.game_object.destroy()
