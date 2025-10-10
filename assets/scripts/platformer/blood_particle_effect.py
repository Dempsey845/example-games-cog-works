from cogworks.components.particle_effect import ParticleEffect


class BloodParticleEffect(ParticleEffect):
    def __init__(self, particle_amount: int = 3):
        super().__init__(
            sprite_path="images/blood_particle.png",
            particle_amount=particle_amount,
            min_y=-150,
            max_y=-100,
            scale_with_lifetime=True,
            fade_over_lifetime=True,
            rotate_over_lifetime=True
        )
