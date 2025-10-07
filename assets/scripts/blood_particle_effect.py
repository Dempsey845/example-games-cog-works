from assets.scripts.particle import Particle
from cogworks import GameObject
from cogworks.components.script_component import ScriptComponent

class BloodParticleEffect(ScriptComponent):
    def __init__(self, particle_amount:int=3):
        super().__init__()
        self.particle_amount = particle_amount

    def start(self) -> None:
        self.spawn_particles()

    def spawn_particles(self):
        x, y = self.game_object.transform.get_local_position()
        for i in range(self.particle_amount):
            blood_particle = GameObject(f"Particle{i}", z_index=5)
            blood_particle_component = Particle(sprite_path="images/blood_particle.png",min_x=x, max_x=x, min_y=y-150,
                                                     max_y=y-100, scale_with_lifetime=True, fade_over_lifetime=True, rotate_over_lifetime=True)
            blood_particle.add_component(blood_particle_component)
            self.game_object.scene.instantiate_game_object(blood_particle)