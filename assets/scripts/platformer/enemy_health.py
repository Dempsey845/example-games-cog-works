import weakref

from cogworks import GameObject
from cogworks.components.script_component import ScriptComponent
from cogworks.components.ui.ui_fill_image import UIFillImage

from assets.scripts.platformer.blood_particle_effect import BloodParticleEffect
from assets.scripts.platformer.death_screen import DeathScreen


class EnemyHealth(ScriptComponent):
    def __init__(self, start_health: int = 100, max_health: int = 100):
        super().__init__()
        self.start_health = start_health
        self.max_health = max_health
        self.current_health = start_health

    def start(self):
        self.current_health = self.start_health

    def take_damage(self, damage: int):
        self.current_health -= damage
        self.current_health = max(self.current_health, 0)

        x, y = self.game_object.transform.get_local_position()
        blood = GameObject("Blood Effect", x=x, y=y)
        blood_effect = BloodParticleEffect()
        blood.add_component(blood_effect)
        self.game_object.scene.instantiate_game_object(blood)

        self.game_object.get_component("AudioSource").play_one_shot("sounds/growl.mp3")

        if self.current_health <= 0:
            self.game_object.destroy()
            return
