from cogworks import GameObject
from cogworks.components.sprite import Sprite

from assets.scripts.snake_head import SnakeHead


def setup_snake_scene(engine):
    scene = engine.create_scene("SnakeGame")

    def on_game_over():
        print("Game Over!")

    snake_head = GameObject("SnakeHead")
    snake_head.add_component(SnakeHead(on_game_over))
    snake_head.add_component(Sprite("images/player.png"))
    snake_head.transform.set_local_position(200, 200)

    scene.add_game_object(snake_head)

    return scene
