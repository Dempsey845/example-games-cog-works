from assets.scripts.platformer.player_health import PlayerHealth
from cogworks.components.script_component import ScriptComponent
from cogworks.components.trigger_collider import TriggerCollider


class Spike(ScriptComponent):
    def __init__(self, damage: int = 100):
        super().__init__()
        self.damage = damage

    def start(self):
        self.game_object.add_component(TriggerCollider(layer="Spike", width=200, height=20, offset_y=-100, layer_mask=["Player", "Circle"], debug=True))

    def on_trigger_enter(self, other):
        if other.layer == "Player":
            player_health = other.game_object.get_component(PlayerHealth)

            if player_health and player_health.exists():
                player_health.take_damage(self.damage)

        elif other.layer == "Circle":
            other.game_object.destroy()