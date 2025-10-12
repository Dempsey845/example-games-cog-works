from cogworks import GameObject
from cogworks.components.audio_source import AudioSource

from cogworks.components.sprite_animation import SpriteAnimation
from cogworks.components.script_component import ScriptComponent
from cogworks.components.sprite import Sprite
from cogworks.components.trigger_collider import TriggerCollider

from assets.scripts.platformer.sparkle_particle_effect import SparkleParticleEffect
from assets.scripts.platformer.player_coins import PlayerCoins


class Coin(ScriptComponent):
    def __init__(self):
        super().__init__()
        self.sprite = None
        self.max_coin_index = 7
        self.spin_rate = 0.1
        self.collided = False
        self.fade_out_speed = 400

    def start(self):
        self.collided = False

        self.sprite = Sprite("images/coins/coin0.png", pixel_art_mode=True)
        trigger_collider = TriggerCollider(debug=False, layer="Coin", layer_mask=["Player"])
        self.game_object.add_component(self.sprite)
        self.game_object.add_component(trigger_collider)

        sprite_animation = SpriteAnimation()
        sprite_animation.add_animation("Spin", "images/coins/coin.png", 0, self.max_coin_index, self.spin_rate)
        sprite_animation.set_animation("Spin")
        self.game_object.add_component(sprite_animation)

        self.game_object.add_component(AudioSource())

    def update(self, dt):
        if self.sprite:
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
            self.game_object.get_component("AudioSource").play_one_shot("sounds/coin.mp3")
            self.collided = True
