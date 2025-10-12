
from cogworks import GameObject

from assets.scripts.platformer.platformer_movement import PlatformerMovement
from assets.scripts.platformer.player_animation_controller import PlayerAnimationController
from assets.scripts.platformer.player_coins import PlayerCoins
from assets.scripts.platformer.player_health import PlayerHealth
from cogworks.components.audio_source import AudioSource
from cogworks.components.rigidbody2d import Rigidbody2D
from cogworks.components.script_component import ScriptComponent
from cogworks.components.sprite import Sprite
from cogworks.components.trigger_collider import TriggerCollider
from cogworks.components.ui.ui_fill_image import UIFillImage
from cogworks.components.ui.ui_image import UIImage
from cogworks.components.ui.ui_label import UILabel
from cogworks.components.ui.ui_transform import UITransform


class Player(ScriptComponent):
    instance = None

    def __init__(self):
        super().__init__()

    def start(self):
        Player.instance = self
        go = self.game_object

        # --- Heart Background Image ---
        heart_background = GameObject("HeartBackground", 5)
        heart_background.add_component(UITransform(
            width=0.1, height=0.1, y=0, x=0, anchor="topleft"
        ))
        heart_background.add_component(UIImage("images/heart_background.png"))
        go.scene.instantiate_game_object(heart_background)

        # --- Health Fill Image ---
        heart_fill_image = GameObject("HeartFill", 6)
        heart_fill_image.add_component(UITransform(
            width=0.1, height=0.1, y=0, x=0, anchor="topleft"
        ))
        heart_fill_image.add_component(UIFillImage(
            "images/heart.png", fill_direction="vertical", fill_origin="bottom", fill_speed=0.5
        ))
        go.scene.instantiate_game_object(heart_fill_image)

        # --- Coin Counter Label ---
        coin_counter = GameObject("CoinCounter")
        coin_counter.add_component(UITransform(y=0.2, x=0, width=0.2, height=0.1, anchor="topleft"))
        coin_counter_label = UILabel(text="Coins: 0", anchor="midleft")
        coin_counter.add_component(coin_counter_label)
        go.scene.instantiate_game_object(coin_counter)

        # --- Player Components ---
        go.add_component(Rigidbody2D(freeze_rotation=True, debug=False, width=150, height=300))
        go.add_component(Sprite("images/player/idle0.png", scale_factor=5, offset_y=-20, pixel_art_mode=True))
        go.add_component(PlatformerMovement(speed=1000, jump_force=1000))
        go.add_component(TriggerCollider(layer="Player", layer_mask=["Spike", "Coin"], debug=False, width=120, height=300))
        go.add_component(PlayerHealth(fill_image=heart_fill_image.get_component(UIFillImage)))
        go.add_component(PlayerCoins(coin_counter_label))
        go.add_component(PlayerAnimationController())
        go.add_component(AudioSource())

    def on_remove(self):
        Player.instance = None
