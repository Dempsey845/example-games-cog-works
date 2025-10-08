from cogworks import GameObject

from assets.scripts.player_coins import PlayerCoins
from cogworks.components.script_component import ScriptComponent
from cogworks.components.sprite import Sprite
from cogworks.components.trigger_collider import TriggerCollider

from assets.scripts.sparkle_particle_effect import SparkleParticleEffect


class Coin(ScriptComponent):
    def __init__(self):
        super().__init__()
        self.sprite = None
        self.current_coin_index = 0
        self.max_coin_index = 7
        self.spin_rate = 0.1
        self.timer = 0
        self.collided = False
        self.fade_out_speed = 400

    def start(self):
        self.current_coin_index = 0
        self.timer = 0
        self.collided = False

        self.sprite = Sprite("images/coins/coin0.png")
        trigger_collider = TriggerCollider(debug=False, layer="Coin", layer_mask=["Player"])
        self.game_object.add_component(self.sprite)
        self.game_object.add_component(trigger_collider)

    def update(self, dt):
        if self.sprite:
            self.timer += dt
            if self.timer >= self.spin_rate:
                self.sprite.change_image(f"images/coins/coin{self.current_coin_index}.png")
                self.current_coin_index += 1
                if self.current_coin_index > self.max_coin_index:
                    self.current_coin_index = 0
                self.timer = 0.0

            if self.collided:
                alpha = self.sprite.alpha
                new_alpha = alpha - self.fade_out_speed * dt
                if new_alpha <= 0:
                    self.game_object.destroy()
                else:
                    self.sprite.set_alpha(new_alpha)

    def on_trigger_enter(self, other):
        if not self.collided:
            other.game_object.get_component(PlayerCoins).add_coin()
            x, y = self.game_object.transform.get_local_position()
            sparkle = GameObject("Blood Effect", x=x, y=y)
            sparkle.add_component(SparkleParticleEffect())
            self.game_object.scene.instantiate_game_object(sparkle)
            self.collided = True
