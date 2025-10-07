import weakref

from cogworks.components.script_component import ScriptComponent
from cogworks.components.ui.ui_label import UILabel


class PlayerCoins(ScriptComponent):
    def __init__(self, coin_counter_label:UILabel):
        super().__init__()
        self.coins = 0
        self.coin_counter_label_ref = weakref.ref(coin_counter_label)

    def start(self):
        self.coins = 0

    def add_coin(self):
        self.coins += 1
        coin_counter_label = self.coin_counter_label_ref()
        if coin_counter_label:
            coin_counter_label.set_text(f"Coins: {self.coins}")
