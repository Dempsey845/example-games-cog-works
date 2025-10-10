from assets.scripts.snake.snake_grid import SnakeGrid
from cogworks import GameObject
from cogworks.components.sprite import Sprite

from assets.scripts.snake.snake_head import SnakeHead
from cogworks.components.ui.ui_button import UIButton
from cogworks.components.ui.ui_transform import UITransform


def setup_snake_scene(engine):
    scene = engine.create_scene("SnakeGame")

    grid = GameObject("Grid", -1)
    snake_grid = SnakeGrid(scene.camera_component)
    grid.add_component(snake_grid)

    snake_head = GameObject("SnakeHead", 1)
    snake_head.add_component(SnakeHead(snake_grid))
    snake_head.add_component(Sprite("images/snake_part.png"))

    scene.add_game_object(snake_head)
    scene.add_game_object(grid)

    # --- Exit Button ---
    def exit_scene(go):
        print("Exiting")
        engine.set_active_scene("Menu")

    exit_btn = GameObject("ExitButton")
    exit_btn.add_component(UITransform(width=0.1, height=0.05, x=1, anchor="topright"))
    exit_btn.add_component(UIButton("Exit", on_click=exit_scene, border_radius=20))
    scene.add_game_object(exit_btn)

    # --- Restart Button ---
    def restart_scene(go):
        engine.restart_active_scene()

    restart_btn = GameObject("RestartButton")
    restart_btn.add_component(UITransform(width=0.1, height=0.05, x=1, y=0.1, anchor="topright"))
    restart_btn.add_component(UIButton("Restart", on_click=restart_scene, border_radius=20))
    scene.add_game_object(restart_btn)

    return scene
