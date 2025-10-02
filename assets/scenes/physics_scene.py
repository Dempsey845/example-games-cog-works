import random

from cogworks.components.background import Background
from cogworks.components.ui.ui_button import UIButton
from cogworks.components.ui.ui_fill_image import UIFillImage
from cogworks.components.ui.ui_image import UIImage
from cogworks.components.ui.ui_transform import UITransform
from cogworks.game_object import GameObject
from cogworks.components.transform import Transform
from cogworks.components.sprite import Sprite
from cogworks.components.rigidbody2d import Rigidbody2D
from assets.scripts.platformer_movement import PlatformerMovement
from assets.scripts.camera_controller import CameraController

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 800

def setup_physics_scene(engine):
    main_scene = engine.create_scene("Physics")

    # --- Background Setup ---
    background = GameObject("Background")
    background.add_component(Sprite("images/sky_background.png"))
    background.add_component(Background())
    main_scene.add_game_object(background)

    # --- Player Setup ---
    player = GameObject("Player", 1)
    player.add_component(Sprite("images/cow.png"))
    player.add_component(Rigidbody2D(freeze_rotation=True, width=80, height=100, debug=False))
    player.add_component(PlatformerMovement(speed=1000, jump_force=1000))

    player_transform = player.get_component(Transform)
    player_transform.set_world_position(WINDOW_WIDTH, 0)
    player_transform.set_local_scale(2)
    main_scene.add_game_object(player)

    # --- Game Buttons ---
    def exit_game(go):
        engine.change_active_scene("Menu")

    exit_btn = GameObject("ExitButton", 5)
    exit_btn.add_component(UITransform(width=0.2, height=0.05, y=0.02, x=0.98, anchor="topright"))
    exit_btn.add_component(UIButton("Exit", on_click=exit_game, bg_color=(255, 0, 0), border_radius=20))
    main_scene.add_game_object(exit_btn)

    # --- Heart Background Image ---
    heart_background = GameObject("HeartBackground", 5)
    heart_background.add_component(UITransform(
        width=0.1, height=0.1, y=0, x=0, anchor="topleft"
    ))
    background_image = UIImage("images/heart_background.png")
    heart_background.add_component(background_image)
    main_scene.add_game_object(heart_background)

    # --- Health Fill Image ---
    heart_fill_image = GameObject("HeartFill")

    # Add UITransform as child, relative to parent
    heart_fill_image.add_component(UITransform())

    # Add the fill image component
    fill_image = UIFillImage("images/heart.png", fill_direction="vertical", fill_origin="bottom",  fill_speed=0.5)
    heart_fill_image.add_component(fill_image)
    fill_image.set_fill(0.01, smooth=True)

    heart_background.add_child(heart_fill_image)

    # --- Circle Container & Circles ---
    circle_container = GameObject("Circle Container")
    main_scene.add_game_object(circle_container)

    for i in range(100):
        circle = GameObject(f"Circle{i}")
        circle.add_component(Sprite("images/football.png"))
        circle.add_component(
            Rigidbody2D(shape_type="circle", radius=50, debug=False, freeze_rotation=False, friction=0.1)
        )

        circle_transform = circle.get_component(Transform)
        circle_transform.set_local_position(WINDOW_WIDTH + (i * 0.1), -300 - (i * 2))
        circle_transform.set_local_scale(random.random() * 0.5 + 0.5)

        circle_container.add_child(circle)

    # --- Camera ---
    main_scene.camera.add_component(CameraController(player_transform, fixed=True))
    main_scene.camera_component.set_zoom(0.4)

    # --- Floor ---
    floor = GameObject("Floor")
    floor_transform = floor.get_component(Transform)
    floor_transform.set_local_scale(5)
    floor_transform.set_local_rotation(0)

    floor_sprite = Sprite("images/floor.png")
    floor.add_component(floor_sprite)
    floor.add_component(Rigidbody2D(static=True, debug=True))

    floor_transform.set_world_position(WINDOW_WIDTH, WINDOW_HEIGHT)

    main_scene.add_game_object(floor)

    # --- Wall ---
    wall1 = GameObject("Wall 1")
    wall1_transform = wall1.get_component(Transform)
    wall1_transform.set_local_scale(10)

    wall1_sprite = Sprite("images/Wall.png")
    wall1.add_component(wall1_sprite)
    wall1.add_component(Rigidbody2D(static=True, debug=True))

    floor_x, floor_y = floor_transform.get_local_position()
    left_side_of_floor = floor_x + (floor_sprite.get_width(floor_transform) // 2)
    wall1_transform.set_local_position(left_side_of_floor - wall1_sprite.get_width(wall1_transform) // 2, floor_y)

    main_scene.add_game_object(wall1)

    return main_scene
