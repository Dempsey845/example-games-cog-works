from assets.scripts.player_health import PlayerHealth
from cogworks.components.script_component import ScriptComponent
from cogworks.components.trigger_collider import TriggerCollider


class Spike(ScriptComponent):
    def __init__(self, damage: int = 10, tick_rate: float = 0.5):
        super().__init__()
        self.damage = damage
        self.tick_rate = tick_rate
        self.timer = 0
        self.is_colliding = False
        self.player_health = None

    def start(self):
        self.game_object.add_component(TriggerCollider(layer="Spike", layer_mask=["Player"], debug=False))
        self.timer = self.tick_rate
        self.is_colliding = False
        self.player_health = None

    def update(self, dt):
        if self.is_colliding:
            self.timer += dt
            if self.timer >= self.tick_rate:
                if self.player_health:
                    self.player_health.take_damage(self.damage)
                self.timer = 0

    def on_trigger_enter(self, other):
        self.is_colliding = True
        self.player_health = other.game_object.get_component(PlayerHealth)
    def on_trigger_exit(self, other):
        self.is_colliding = False