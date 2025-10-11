from cogworks.components.script_component import ScriptComponent
from cogworks.components.sprite import Sprite
from cogworks.components.trigger_collider import TriggerCollider

from assets.scripts.platformer.enemy_health import EnemyHealth


class Bullet(ScriptComponent):

    def __init__(self):
        super().__init__()
        self.speed = 2500
        self.lifespan = 1
        self.lifetime = 0.0
        self.damage = 50

    def start(self):
        self.game_object.add_component(Sprite("images/bullet.png", flip_y=True))
        self.game_object.add_component(TriggerCollider(layer="Bullet", debug=False))

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

    def on_trigger_enter(self, other):
        enemy_health = other.game_object.get_component(EnemyHealth)
        if enemy_health is not None:
            enemy_health.take_damage(self.damage)
        self.game_object.destroy()