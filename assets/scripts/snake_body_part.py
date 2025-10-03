from cogworks.components.script_component import ScriptComponent
from cogworks.components.sprite import Sprite
from cogworks.components.trigger_collider import TriggerCollider


class SnakeBodyPart(ScriptComponent):
    def __init__(self, sprite_image_path:str, layer:str = "BodyPart"):
        super().__init__()
        self.sprite_image_path = sprite_image_path
        self.layer = layer

    def start(self):
        self.game_object.add_component(Sprite(self.sprite_image_path))
        self.game_object.add_component(TriggerCollider(layer=self.layer, layer_mask=["Head"], debug=True))

    def on_trigger_enter(self, other):
        print("Collided with head")