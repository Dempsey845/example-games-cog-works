import random

from assets.scripts.player_health import PlayerHealth
from assets.scripts.spike import Spike
from cogworks.components.background import Background
from cogworks.components.trigger_collider import TriggerCollider
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
    background.add_component(Sprite("images/star_background.png"))
    background.add_component(Background())
    main_scene.add_game_object(background)

    # --- Heart Background Image ---
    heart_background = GameObject("HeartBackground", 5)
    heart_background.add_component(UITransform(
        width=0.1, height=0.1, y=0, x=0, anchor="topleft"
    ))
    heart_background.add_component(UIImage("images/heart_background.png"))
    main_scene.add_game_object(heart_background)

    # --- Health Fill Image ---
    heart_fill_image = GameObject("HeartFill", 6)
    heart_fill_image.add_component(UITransform(
        width=0.1, height=0.1, y=0, x=0, anchor="topleft"
    ))
    heart_fill_image.add_component(UIFillImage(
        "images/heart.png", fill_direction="vertical", fill_origin="bottom", fill_speed=0.5
    ))
    main_scene.add_game_object(heart_fill_image)

    # --- Player Setup ---
    player = GameObject(
        "Player", 2, x=WINDOW_WIDTH, y=-500, scale_x=2, scale_y=2
    )
    player.add_component(Sprite("images/cow.png", offset_x=-80, offset_y=-85, scale_factor=0.5))
    player.add_component(Rigidbody2D(freeze_rotation=True, width=60, height=100, debug=True))
    player.add_component(PlatformerMovement(speed=1000, jump_force=1000))
    player.add_component(TriggerCollider(width=80, layer="Player", layer_mask=["Spike"], debug=False))
    player.add_component(PlayerHealth(fill_image=heart_fill_image.get_component(UIFillImage)))
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
    main_scene.add_game_object(circle_container)

    for i in range(50):
        scale = random.random() * 0.5 + 0.5
        circle = GameObject(
            f"Circle{i}",
            x=WINDOW_WIDTH + (i * 0.1),
            y=-300 - (i * 2),
            scale_x=scale,
            scale_y=scale
        )
        circle.add_component(Sprite("images/duck.png"))
        circle.add_component(Rigidbody2D(shape_type="circle", radius=100*scale, debug=False, freeze_rotation=False, friction=0.1))
        circle_container.add_child(circle)

    # --- Camera ---
    main_scene.camera.add_component(CameraController(player.get_component(Transform), fixed=True))
    main_scene.camera_component.set_zoom(0.4)

    # --- Floor ---
    floor = GameObject("Floor", WINDOW_WIDTH, WINDOW_HEIGHT, scale_x=4, scale_y=4)
    floor_sprite = Sprite("images/floor_2.png")
    floor.add_component(floor_sprite)
    floor.add_component(Rigidbody2D(static=True, debug=True))
    main_scene.add_game_object(floor)

    # --- Spike ---
    spike = GameObject("Spike", z_index=3, x=WINDOW_WIDTH, y=-WINDOW_HEIGHT//3.2, scale_x=2, scale_y=2)
    spike.add_component(Sprite("images/spikes.png"))
    spike.add_component(Rigidbody2D(static=True, debug=True))
    spike.add_component(Spike())
    main_scene.add_game_object(spike)

    # # --- Wall ---
    # floor_x, floor_y = floor.get_component(Transform).get_local_position()
    # wall1_sprite = Sprite("images/Wall.png")
    # wall1 = GameObject(
    #     "Wall 1",
    #     x=floor_x + (floor_sprite.get_width(floor.get_component(Transform)) // 2 + 200) - wall1_sprite.get_image_width() // 2,
    #     y=floor_y,
    #     scale_x=10,
    #     scale_y=10
    # )
    # wall1.add_component(wall1_sprite)
    # wall1.add_component(Rigidbody2D(static=True, debug=True))
    # main_scene.add_game_object(wall1)

    return main_scene
