from assets.scripts.coin import Coin
from cogworks import GameObject
from cogworks.components.script_component import ScriptComponent
from cogworks.components.sprite import Sprite


class Platform(ScriptComponent):
    def __init__(self):
        super().__init__()

    def start(self):
        x, y = self.game_object.transform.get_local_position()
        platform_height = self.game_object.get_component(Sprite).get_height()
        self.game_object.transform.debug = True
        coin_size = 128
        coin_y_offset = -coin_size//2
        coin_y = y - platform_height//2 - coin_size//2
        coin = GameObject("Coin", x=x, y=coin_y + coin_y_offset, scale_x=8, scale_y=8, z_index=4)
        coin.add_component(Coin())
        self.game_object.scene.instantiate_game_object(coin)
