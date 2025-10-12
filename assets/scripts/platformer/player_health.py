import weakref

from cogworks import GameObject
from cogworks.components.script_component import ScriptComponent
from cogworks.components.ui.ui_fill_image import UIFillImage

from assets.scripts.platformer.blood_particle_effect import BloodParticleEffect
from assets.scripts.platformer.death_screen import DeathScreen


class PlayerHealth(ScriptComponent):
    def __init__(self, start_health: int = 100, max_health: int = 100, fill_image: UIFillImage = None):
        super().__init__()
        self.start_health = start_health
        self.max_health = max_health
        self.current_health = start_health
        self.fill_image_ref = weakref.ref(fill_image)
        self.dead = False

    def start(self):
        self.current_health = self.start_health
        self.dead = False

        fill_image = self.fill_image_ref()
        if fill_image:
            self.fill_image_ref().set_fill(amount=self.current_health / self.max_health, smooth=True)

    def update(self, dt):
        x, y = self.game_object.transform.get_local_position()
        if y > 500:
            self.take_damage(self.max_health)

    def take_damage(self, damage: int, fill_speed: float = 0.5):
        self.current_health -= damage
        self.current_health = max(self.current_health, 0)

        if self.current_health <= 0:
            self.on_death()

        x, y = self.game_object.transform.get_local_position()
        blood = GameObject("Blood Effect", x=x, y=y)
        blood_effect = BloodParticleEffect()
        blood.add_component(blood_effect)
        self.game_object.scene.instantiate_game_object(blood)
        self.game_object.get_component("AudioSource").play_one_shot("sounds/impact.mp3")

        fill_image = self.fill_image_ref()
        if fill_image:
            self.fill_image_ref().fill_speed = fill_speed
            self.fill_image_ref().set_fill(amount=self.current_health / self.max_health, smooth=True)

    def on_death(self):
        if not self.dead:
            self.dead = True
            death_label_object = GameObject("DeathLabel", z_index=10)
            death_label_object.add_component(DeathScreen())
            self.game_object.scene.instantiate_game_object(death_label_object)
            self.game_object.destroy()