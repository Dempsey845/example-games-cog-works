import weakref

from assets.scripts.player import Player
from assets.scripts.player_health import PlayerHealth
from cogworks.components.script_component import ScriptComponent
from cogworks.components.sprite import Sprite

CHASE_DISTANCE_SQUARED = 700000
ATTACK_DISTANCE_SQUARED = 28000
WONDER_TIME = 5
IDLE_TIME = 5
PLAYER_Y_RANGE = 350

class Goblin(ScriptComponent):
    def __init__(self, platform):
        super().__init__()
        self.platform_ref = weakref.ref(platform)
        self.transform = None
        self.sprite = None
        self.player_transform_ref = None

        self.move_speed = 500
        self.edges = (0, 0)
        self.x = 0
        self.y = 0
        self.x2 = 0
        self.y2 = 0
        self.move_left = True

        self.animation_timer = 0.0
        self.anim_counter = 1

        self.distance_squared = 0
        self.chase_distance_squared = CHASE_DISTANCE_SQUARED * platform.game_object.transform.local_scale_x
        self.attack_distance_squared = ATTACK_DISTANCE_SQUARED

        self.states = ["idle", "wonder", "chase", "attack"]
        self.current_state = self.states[1]

        self.wonder_timer = 0.0
        self.idle_timer = 0.0

    def start(self) -> None:
        self.transform = self.game_object.transform
        self.sprite = self.game_object.get_component(Sprite)

        self.x, self.y = self.transform.get_local_position()
        self.x2 = 0
        self.y2 = 0


        if Player.instance:
            self.player_transform_ref = weakref.ref(Player.instance.game_object.transform)

        self.edges = self.platform_ref().get_edges()
        self.current_state = self.states[1]

        self.wonder_timer = 0.0
        self.idle_timer = 0.0

    def update(self, dt: float) -> None:
        self.x, self.y = self.transform.get_local_position()

        if self.player_transform_ref().exists():
            player_pos = self.player_transform_ref().get_local_position()
            self.x2, self.y2 = player_pos[0], player_pos[1]
            x2, y2 = (self.x2, self.y2)
            self.distance_squared = (x2 - self.x)**2 + (y2 - self.y)**2

        match self.current_state:
            case "idle":
                self.idle_timer += dt

                if self.check_should_chase():
                    self.idle_timer = 0

                if self.idle_timer >= IDLE_TIME:
                    self.current_state = self.states[1]
                    self.idle_timer = 0

            case "wonder":
                self.move(dt)
                self.check_bounds()
                self.wonder_timer += dt

                if self.check_should_chase():
                    self.wonder_timer = 0

                if self.wonder_timer >= WONDER_TIME:
                    self.current_state = self.states[0]
                    self.sprite.change_image("images/goblin/goblin.png")
                    self.wonder_timer = 0

            case "chase":
                if not self.is_player_beyond_bounds():
                    self.move(dt)
                    self.determine_chase_direction()

                if self.distance_squared > self.chase_distance_squared or not self.is_player_within_y_range():
                    # Idle
                    self.sprite.change_image("images/goblin/goblin.png")
                    self.current_state = self.states[0]
                elif self.distance_squared <= self.attack_distance_squared:
                    # Attack
                    self.current_state = self.states[3]
                    pass
            case "attack":
                self.play_attack_animation(dt)
                if self.distance_squared > self.attack_distance_squared:
                    # Chase
                    self.current_state = self.states[2]

    def check_should_chase(self):
        if self.distance_squared <= self.chase_distance_squared and self.is_player_within_y_range():
            # Chase
            self.current_state = self.states[2]
            return True
        return False

    def determine_chase_direction(self):
        self.move_left = self.x > self.x2

    def is_player_beyond_bounds(self):
        return self.x2 < self.edges[0] or self.x2 > self.edges[1]

    def is_player_within_y_range(self):
        return abs(self.y2 - self.y) <= PLAYER_Y_RANGE

    def check_bounds(self):
        if self.x < self.edges[0]:
            self.move_left = False
        elif self.x > self.edges[1]:
            self.move_left = True

    def move(self, dt: float):
        if self.move_left:
            new_pos_x = self.x - self.move_speed * dt
        else:
            new_pos_x = self.x + self.move_speed * dt

        self.sprite.flip_x = self.move_left

        self.transform.set_local_position(new_pos_x, self.y)
        self.play_run_animation(dt)

    def attack(self):
        player_health_ref = weakref.ref(self.player_transform_ref().game_object.get_component(PlayerHealth))
        if player_health_ref() and player_health_ref().exists():
            player_health_ref().take_damage(15)
            if player_health_ref().current_health <= 0:
                self.current_state = self.states[0]

    def play_run_animation(self, dt: float):
        self.animation_timer += dt
        if self.animation_timer > 0.15:
            self.sprite.change_image(f"images/goblin/run/run{self.anim_counter}.png")
            self.animation_timer = 0
            self.anim_counter += 1
            if self.anim_counter >= 6:
                self.anim_counter = 1

    def play_attack_animation(self, dt: float):
        self.animation_timer += dt
        if self.animation_timer > 0.15:
            if self.anim_counter == 3:
                self.attack()
            self.sprite.change_image(f"images/goblin/attack/attack{self.anim_counter}.png")
            self.animation_timer = 0
            self.anim_counter += 1
            if self.anim_counter >= 6:
                self.anim_counter = 1