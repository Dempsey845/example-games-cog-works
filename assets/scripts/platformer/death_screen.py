from cogworks.components.script_component import ScriptComponent
from cogworks.components.ui.ui_label import UILabel
from cogworks.components.ui.ui_transform import UITransform


class DeathScreen(ScriptComponent):
    def __init__(self):
        super().__init__()
        self.label = None
        self.timer = 5

    def start(self):
        self.label = UILabel("You died! Restarting in.", color=(255, 0, 0), font_size=50)
        death_transform = UITransform(anchor="center", relative=True, x=0.5, y=0.3)
        self.game_object.add_component(self.label)
        self.game_object.add_component(death_transform)

    def update(self, dt):
        self.timer -= dt

        self.label.set_text(f"You died! Restarting in {int(self.timer)} seconds.")

        if self.timer <= 0:
            self.timer = 0
            self.game_object.scene.restart()