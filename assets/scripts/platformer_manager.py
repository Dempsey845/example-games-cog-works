from cogworks.components.script_component import ScriptComponent
from cogworks.components.trigger_collider import TriggerCollider


class PlatformerManager(ScriptComponent):
    def __init__(self):
        super().__init__()
        self.timer = 0.0

    def start(self):
        self.timer = 0.0

    def update(self, dt):
        # self.timer += dt
        # if self.timer >= 5:
        #     trigger_collider_count = len(self.game_object.scene.get_all_components_of_type(TriggerCollider))
        #     print(f"TriggerCollider count: {trigger_collider_count}")
        #     print(len(self.game_object.scene.trigger_collision_manager.colliders))
        #     self.timer = 0
        pass