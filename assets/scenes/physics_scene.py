import random

from cogworks.components.trigger_collider import TriggerCollider

from assets.scripts.platformer.background_music import BackgroundMusic
from assets.scripts.platformer.platform import Platform
from assets.scripts.platformer.platformer_manager import PlatformerManager
from assets.scripts.platformer.player import Player
from cogworks.pygame_wrappers.window import Window

from assets.scripts.platformer.ball_spawner import BallSpawner
from cogworks.components.background import Background
from cogworks.components.ui.ui_button import UIButton
from cogworks.components.ui.ui_transform import UITransform
from cogworks.game_object import GameObject
from cogworks.components.sprite import Sprite
from cogworks.components.rigidbody2d import Rigidbody2D
from assets.scripts.camera_controller import CameraController


def setup_physics_scene(engine):
    main_scene = engine.create_scene("Physics")

    window_width, window_height = Window.get_instance().get_size()

    # --- Background Setup ---
    background = GameObject("Background")
    background.add_component(Sprite("images/star_background.png"))
    background.add_component(Background())
    main_scene.add_game_object(background)

    background_music = GameObject("BackgroundMusic")
    background_music.add_component(BackgroundMusic())
    main_scene.add_game_object(background_music)

    # --- Player Setup ---
    player = GameObject(
        "Player", 2, x=window_width, y=-500, scale_x=2, scale_y=2
    )
    player.add_component(Player())
    main_scene.add_game_object(player)

    # --- Game Buttons ---
    def exit_game(go):
        engine.set_active_scene("Menu")

    exit_btn = GameObject("ExitButton", 5)
    exit_btn.add_component(UITransform(width=0.2, height=0.05, y=0.02, x=0.98, anchor="topright"))
    exit_btn.add_component(UIButton("Exit", on_click=exit_game, bg_color=(255, 0, 0), border_radius=20))
    main_scene.add_game_object(exit_btn)

    # --- Circle Container & Circles ---
    circle_container = GameObject("Circle Container")
    circle_container.add_component(BallSpawner())
    main_scene.add_game_object(circle_container)

    # --- Camera ---
    main_scene.camera.add_component(CameraController(player, fixed=True, offset_y=-300, max_y=-300))
    main_scene.camera_component.set_zoom(0.3)

    # --- Floor ---
    floor_width = 1000
    ground_floor_count = 20
    floors = [
    ]

    for i in range(ground_floor_count):
        rand_x_offset = random.randint(-100, 100)
        rand_y = random.randint(0, 50)

        spawn_third = random.randint(0, 1) == 1

        floors.append({"x": 0 + (floor_width * i), "y": window_height, "scale": 2})
        floors.append({"x": rand_x_offset + (floor_width * i), "y": rand_y, "scale": 1})
        if spawn_third:
            up_count = random.randint(2, 6)
            for j in range(up_count):
                rand_y = random.randint(-500 - (600 * j+1), -450 - (500 * j+1))
                rand_x_offset = random.randint(-200, 100)
                rand_scale = random.uniform(0.6, 1.4)
                floors.append({"x": rand_x_offset + (floor_width * i), "y": rand_y, "scale": rand_scale})


    for i, floor in enumerate(floors):
        floor_object = GameObject(
            f"Floor{i}",
            x=floor["x"],
            y=floor["y"],
            scale_x=floor["scale"],
            scale_y=floor["scale"]
        )
        floor_sprite = Sprite("images/floor_2.png")
        floor_object.add_component(floor_sprite)
        floor_object.add_component(Rigidbody2D(static=True, debug=False, width=floor_sprite.get_width() * floor["scale"], height=floor_sprite.get_height() * floor["scale"]))
        floor_object.add_component(TriggerCollider())
        floor_object.add_component(Platform())
        main_scene.add_game_object(floor_object)

    # --- Manager ---
    manager = GameObject("Manager")
    manager.add_component(PlatformerManager())
    main_scene.add_game_object(manager)

    return main_scene
