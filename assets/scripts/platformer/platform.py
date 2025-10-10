import random

from assets.scripts.platformer.spike import Spike
from cogworks.components.rigidbody2d import Rigidbody2D
from cogworks.components.trigger_collider import TriggerCollider

from assets.scripts.platformer.coin import Coin
from cogworks import GameObject
from cogworks.components.script_component import ScriptComponent
from cogworks.components.sprite import Sprite

from assets.scripts.platformer.goblin import Goblin


class Platform(ScriptComponent):
    def __init__(self):
        super().__init__()
        self.options = ["coin", "goblin", "spike"]

    def start(self):
        random_option = random.choice(self.options)
        match random_option:
            case "coin":
                self.spawn_coin()
            case "goblin":
                self.spawn_goblin()
            case "spike":
                self.spawn_spike()

    def spawn_coin(self):
        x, y = self.game_object.transform.get_local_position()
        platform_height = self.game_object.get_component(Sprite).get_height()

        coin_size = 128
        coin_y_offset = -75
        coin_y = y - platform_height // 2 - coin_size // 2
        coin = GameObject("Coin", x=x, y=coin_y + coin_y_offset, scale_x=8, scale_y=8, z_index=4)
        coin.add_component(Coin())
        self.game_object.scene.instantiate_game_object(coin)

    def spawn_goblin(self):
        x, y = self.game_object.transform.get_local_position()
        platform_height = self.game_object.get_component(Sprite).get_height()

        goblin_scale = 0.8
        goblin_size = 300 * goblin_scale
        goblin = GameObject("Goblin", z_index=1, x=x, y=y - platform_height//2 - goblin_size//2, scale_x=goblin_scale, scale_y=goblin_scale)
        goblin.add_component(Sprite("images/goblin/goblin.png", offset_y=-50, scale_factor=0.8))
        goblin.add_component(TriggerCollider(debug=True, width=150, height=250))
        goblin.add_component(Goblin(self))
        self.game_object.scene.instantiate_game_object(goblin)

    def spawn_spike(self):
        x, y = self.game_object.transform.get_local_position()
        platform_height = self.game_object.get_component(Sprite).get_height()

        spike_scale = 2
        spike_size = 100 * spike_scale
        spike = GameObject("Spike", z_index=3, x=x, y=y - platform_height // 2 - spike_size // 2, scale_x=spike_scale,
                           scale_y=spike_scale)
        spike_sprite = Sprite("images/spikes.png")
        spike.add_component(spike_sprite)
        spike.add_component(Rigidbody2D(static=True, debug=True, width=spike_sprite.get_width() * spike_scale - 50,
                                        height=spike_sprite.get_height() * spike_scale - 50))
        spike.add_component(Spike())
        self.game_object.scene.instantiate_game_object(spike)

    def get_edges(self):
        x, _ = self.game_object.transform.get_local_position()
        platform_width = self.game_object.get_component(Sprite).get_width()
        scale, _ = self.game_object.transform.get_local_scale()
        left_edge = x - (platform_width//2)
        right_edge = x + (platform_width//2)
        return left_edge, right_edge