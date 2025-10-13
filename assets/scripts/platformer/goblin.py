import weakref
import random

from assets.scripts.platformer.enemy_health import EnemyHealth
from assets.scripts.platformer.player import Player
from assets.scripts.platformer.player_health import PlayerHealth
from cogworks.components.audio_source import AudioSource
from cogworks.components.script_component import ScriptComponent
from cogworks.components.sprite import Sprite
from cogworks.components.sprite_animation import SpriteAnimation

CHASE_DISTANCE_SQUARED = 700_000
ATTACK_DISTANCE_SQUARED = 38_000
WONDER_TIME = 15
IDLE_TIME = 3
PLAYER_Y_RANGE = 350

class Goblin(ScriptComponent):
    EDGE_BUFFER = 20        # Distance from platform edge before turning
    ATTACK_COOLDOWN = 0.5   # Minimum seconds between attack/chase flips

    def __init__(self, platform):
        super().__init__()
        self.platform_ref = weakref.ref(platform)
        self.transform = None
        self.sprite = None
        self.player_transform_ref = None
        self.sprite_animation = None

        self.move_speed = 800
        self.edges = (0, 0)
        self.move_left = True
        self.distance_squared = 0
        self.chase_distance_squared = CHASE_DISTANCE_SQUARED * platform.game_object.transform.local_scale_x
        self.attack_distance_squared = ATTACK_DISTANCE_SQUARED

        self.states = ["idle", "wonder", "chase", "attack"]
        self.current_state = "wonder"

        self.wonder_timer = 0.0
        self.idle_timer = 0.0
        self.attack_cooldown_timer = 0.0
        self.wonder_direction = 1  # 1 = right, -1 = left

    def start(self) -> None:
        self.transform = self.game_object.transform
        self.sprite = self.game_object.get_component(Sprite)
        self.edges = self.platform_ref().get_edges()

        if Player.instance:
            self.player_transform_ref = weakref.ref(Player.instance.game_object.transform)

        # Set up animations
        self.sprite_animation = SpriteAnimation()
        self.sprite_animation.add_animation("Idle", "images/goblin/goblin.png", 1, 1, 1)
        self.sprite_animation.add_animation("Run", "images/goblin/run/run.png", 1, 6, 0.15)
        attack_anim = self.sprite_animation.add_animation("Attack", "images/goblin/attack/attack.png", 1, 6, 0.15)
        attack_anim.add_event(2, self.attack)

        self.game_object.add_component(self.sprite_animation)
        self.game_object.add_component(EnemyHealth())

        audio_source = AudioSource()
        audio_source.max_distance = 100
        self.game_object.add_component(audio_source)

    def update(self, dt: float) -> None:
        self.x, self.y = self.transform.get_local_position()

        player_transform = self.player_transform_ref() if self.player_transform_ref else None
        if not player_transform or not player_transform.exists():
            self._set_idle_state()
            return

        self.x2, self.y2 = player_transform.get_local_position()
        self.distance_squared = (self.x2 - self.x)**2 + (self.y2 - self.y)**2
        self.attack_cooldown_timer = max(0, self.attack_cooldown_timer - dt)

        match self.current_state:
            case "idle":
                self._update_idle(dt)
            case "wonder":
                self._update_wonder(dt)
            case "chase":
                self._update_chase(dt)
            case "attack":
                self._update_attack()

    # -------------------
    # State handling
    # -------------------

    def _update_idle(self, dt: float):
        self.idle_timer += dt
        if self._check_should_chase():
            self.idle_timer = 0
        elif self.idle_timer >= IDLE_TIME:
            self.current_state = "wonder"
            self.wonder_direction = random.choice([-1, 1])
            self.sprite_animation.set_animation("Run")
            self.idle_timer = 0

    def _update_wonder(self, dt: float):
        self.wonder_timer += dt
        self._move_wonder(dt)
        self._check_bounds_buffer()

        if self._check_should_chase():
            self.wonder_timer = 0
        elif self.wonder_timer >= WONDER_TIME:
            self._set_idle_state()

    def _update_chase(self, dt: float):
        if not self._is_player_beyond_bounds():
            self._move_chase(dt)

        if self.distance_squared > self.chase_distance_squared or not self._is_player_within_y_range():
            self._set_idle_state()
        elif self.distance_squared <= self.attack_distance_squared and self.attack_cooldown_timer <= 0:
            self.current_state = "attack"
            self.sprite_animation.set_animation("Attack")
            self.attack_cooldown_timer = self.ATTACK_COOLDOWN

    def _update_attack(self):
        if self.distance_squared > self.attack_distance_squared:
            self.current_state = "chase"
            self.sprite_animation.set_animation("Run")

    # -------------------
    # Movement helpers
    # -------------------

    def _move_chase(self, dt: float):
        # Predictive chase: moves toward player but with small tolerance
        tolerance = 5
        if abs(self.x - self.x2) > tolerance:
            self.move_left = self.x > self.x2
        self._move(dt, self.move_left)

    def _move_wonder(self, dt: float):
        # Move in random wander direction
        self._move(dt, self.wonder_direction == -1)

    def _move(self, dt: float, move_left: bool):
        new_x = self.x - self.move_speed * dt if move_left else self.x + self.move_speed * dt
        self.sprite.flip_x = move_left
        self.transform.set_local_position(new_x, self.y)

    def _check_bounds_buffer(self):
        half_width = self.sprite.get_width() // 2
        left_edge, right_edge = self.edges
        if self.x - half_width < left_edge + self.EDGE_BUFFER:
            self.wonder_direction = 1
        elif self.x + half_width > right_edge - self.EDGE_BUFFER:
            self.wonder_direction = -1

    # -------------------
    # AI helpers
    # -------------------

    def _check_should_chase(self):
        if self.distance_squared <= self.chase_distance_squared and self._is_player_within_y_range():
            self.current_state = "chase"
            self.sprite_animation.set_animation("Run")
            return True
        return False

    def _is_player_beyond_bounds(self):
        return self.x2 < self.edges[0] or self.x2 > self.edges[1]

    def _is_player_within_y_range(self):
        return abs(self.y2 - self.y) <= PLAYER_Y_RANGE

    def _set_idle_state(self):
        self.sprite_animation.set_animation("Idle")
        self.current_state = "idle"
        self.idle_timer = 0
        self.wonder_timer = 0

    def attack(self):
        audio_source = self.game_object.get_component(AudioSource)
        audio_source.play_one_shot("sounds/slash.mp3")

        player_health = Player.instance.game_object.get_component(PlayerHealth) if Player.instance else None
        if player_health:
            player_health.take_damage(15)
            if player_health.current_health <= 0:
                self._set_idle_state()
