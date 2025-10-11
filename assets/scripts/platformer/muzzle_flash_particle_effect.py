from cogworks.components.particle_effect import ParticleEffect


class MuzzleFlashParticleEffect(ParticleEffect):
    def __init__(self, particle_amount: int = 3):
        super().__init__(
            sprite_path="images/muzzle_flash_particle.png",
            particle_amount=particle_amount,
            min_y=-10,
            max_y=10,
            scale_with_lifetime=True,
            fade_over_lifetime=True,
            rotate_over_lifetime=True,
            lifetime=0.5,
            gravity=200
        )