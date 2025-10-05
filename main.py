from cogworks import Engine
from assets.scenes.physics_scene import setup_physics_scene
from assets.scenes.menu_scene import setup_menu_scene
from assets.scenes.pong_scene import setup_pong_scene
from assets.scenes.snake_scene import setup_snake_scene
from assets.scenes.trigger_test_scene import setup_trigger_test_scene


WINDOW_WIDTH = 800
WINDOW_HEIGHT = 800

engine = Engine(width=WINDOW_WIDTH, height=WINDOW_HEIGHT, fps=500)

# Setup scenes
main_scene = setup_physics_scene(engine)
pong_scene = setup_pong_scene(engine)
menu_scene = setup_menu_scene(engine)
trigger_test_scene = setup_trigger_test_scene(engine)
snake_scene = setup_snake_scene(engine)

engine.set_active_scene("Menu")

engine.run()
