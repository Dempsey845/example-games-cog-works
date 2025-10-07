from assets.scripts.player_health import PlayerHealth
from cogworks.components.rigidbody2d import Rigidbody2D
from cogworks.components.script_component import ScriptComponent
from cogworks.components.trigger_collider import TriggerCollider


class Spike(ScriptComponent):
    def __init__(self, damage: int = 50):
        super().__init__()
        self.damage = damage

    def start(self):
        self.game_object.add_component(TriggerCollider(layer="Spike", layer_mask=["Player", "Circle"], debug=True))

    def on_trigger_enter(self, other):
        if other.layer == "Player":
            player_health = other.game_object.get_component(PlayerHealth)
            player_body = other.game_object.get_component(Rigidbody2D)

            if player_health and player_body:
                _, y_vel = player_body.body.velocity
                if y_vel > 100:
                    player_health.take_damage(self.damage)

        elif other.layer == "Circle":
            other.game_object.destroy()