from cogworks.components.particle_effect import ParticleEffect


class SparkleParticleEffect(ParticleEffect):
    def __init__(self, particle_amount: int = 5):
        super().__init__(
            sprite_path="images/sparkle_particle.png",
            particle_amount=particle_amount,
            min_y=-150,
            max_y=-100,
            scale_with_lifetime=True,
            fade_over_lifetime=True,
            rotate_over_lifetime=True,
            lifetime=2,
            gravity=200
        )