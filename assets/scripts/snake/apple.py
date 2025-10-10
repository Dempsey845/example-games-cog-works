from cogworks.components.script_component import ScriptComponent
from cogworks.components.sprite import Sprite
from cogworks.components.trigger_collider import TriggerCollider


class Apple(ScriptComponent):
    def __init__(self):
        super().__init__()

    def start(self) -> None:
        self.game_object.add_component(Sprite("images/apple.png"))
        self.game_object.add_component(TriggerCollider(layer="Apple", layer_mask=["Head"], debug=False))
