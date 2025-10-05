from cogworks.components.script_component import ScriptComponent
from cogworks.components.sprite import Sprite
from cogworks.components.trigger_collider import TriggerCollider


class SnakeBodyPart(ScriptComponent):
    def __init__(self, head, sprite_image_path: str, layer: str = "BodyPart"):
        super().__init__()
        self.head = head
        self.sprite_image_path = sprite_image_path
        self.layer = layer

        self.timer = 0.0
        self.collision_start_delay = 1
        self.has_collider = False

        self.sprite = None

    def start(self):
        self.game_object.add_component(Sprite(self.sprite_image_path))
        self.sprite = self.game_object.get_component(Sprite)

    def update(self, dt: float) -> None:
        if self.has_collider:
            return

        self.timer += dt

        if self.timer > self.collision_start_delay:
            self.game_object.add_component(
                TriggerCollider(layer=self.layer, layer_mask=["Head"], debug=True),
                runtime=True
            )
            self.has_collider = True

    def on_trigger_enter(self, other):
        self.head.on_game_over()
