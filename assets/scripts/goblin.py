import weakref

from cogworks.components.script_component import ScriptComponent
from cogworks.components.sprite import Sprite


class Goblin(ScriptComponent):
    def __init__(self, platform):
        super().__init__()
        self.platform_ref = weakref.ref(platform)
        self.transform = None
        self.sprite = None
        self.move_speed = 500
        self.edges = (0, 0)
        self.move_left = True

    def start(self) -> None:
        self.transform = self.game_object.transform
        self.sprite = self.game_object.get_component(Sprite)
        self.edges = self.platform_ref().get_edges()
        print(self.edges)

    def update(self, dt: float) -> None:
        x, y = self.transform.get_local_position()

        if x < self.edges[0]:
            self.move_left = False
            self.sprite.flip_x = False
        elif x > self.edges[1]:
            self.move_left = True
            self.sprite.flip_x = True

        if self.move_left:
            new_pos_x = x - self.move_speed * dt
        else:
            new_pos_x = x + self.move_speed * dt

        self.transform.set_local_position(new_pos_x, y)
