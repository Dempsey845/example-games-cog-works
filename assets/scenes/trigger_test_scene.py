import pygame
from cogworks import GameObject
from cogworks.components.transform import Transform
from cogworks.components.sprite import Sprite
from cogworks.components.script_component import ScriptComponent
from cogworks.components.trigger_collider import TriggerCollider
from cogworks.components.ui.ui_button import UIButton
from cogworks.components.ui.ui_transform import UITransform
from cogworks.pygame_wrappers.input_manager import InputManager
from cogworks.pygame_wrappers.window import Window


# --- Player Script ---
class SimplePlayerScript(ScriptComponent):
    def __init__(self, speed=200):
        super().__init__()
        self.speed = speed
        self.input_manager = InputManager.get_instance()

    def update(self, dt):
        transform = self.game_object.get_component(Transform)
        x, y = transform.get_local_position()

        if self.input_manager.is_key_down(pygame.K_LEFT):
            x -= self.speed * dt
        if self.input_manager.is_key_down(pygame.K_RIGHT):
            x += self.speed * dt
        if self.input_manager.is_key_down(pygame.K_UP):
            y -= self.speed * dt
        if self.input_manager.is_key_down(pygame.K_DOWN):
            y += self.speed * dt

        transform.set_local_position(x, y)


# --- Trigger Script ---
class PrintOnTriggerScript(ScriptComponent):
    def on_trigger_enter(self, other_collider):
        print(f"Triggered by {other_collider.game_object.name}!")
    def on_trigger_exit(self, other_collider):
        print(f"Exited by {other_collider.game_object.name}!")

# --- Setup Test Scene ---
def setup_trigger_test_scene(engine):
    scene = engine.create_scene("TriggerTest", (0, 0))
    window_width, window_height = Window.get_instance().get_size()

    # Player
    player = GameObject("Player")
    player.add_component(Sprite("images/player.png"))
    player.get_component(Transform).set_local_position(window_width // 4, window_height // 2)
    player.add_component(SimplePlayerScript())
    player_collider = TriggerCollider(shape="rect", debug=True, layer="Player", layer_mask=["Shape"])
    player.add_component(player_collider)
    scene.add_game_object(player)

    # Shape area
    shape = GameObject("ShapeArea")
    shape.add_component(Sprite("images/shape.png"))
    shape.get_component(Transform).set_local_position(window_width * 3 // 4, window_height // 2)
    shape.add_component(PrintOnTriggerScript())
    shape_collider = TriggerCollider(shape="rect", debug=True, layer="Shape", layer_mask=["Player"])
    shape.add_component(shape_collider)
    scene.add_game_object(shape)

    shape2 = GameObject("ShapeArea2")
    shape2.add_component(Sprite("images/shape.png"))
    shape2.get_component(Transform).set_local_position(window_width * 3 // 4, window_height)
    shape2.add_component(PrintOnTriggerScript())
    shape2_collider = TriggerCollider(shape="rect", debug=True, layer="Shape2", layer_mask=["Shape"])
    shape2.add_component(shape2_collider)
    scene.add_game_object(shape2)

    # --- Exit Button ---
    def exit_scene(go):
        engine.change_active_scene("Menu")

    exit_btn = GameObject("ExitButton")
    exit_btn.add_component(UITransform(width=0.1, height=0.05, x=1, anchor="topright"))
    exit_btn.add_component(UIButton("Exit", on_click=exit_scene, border_radius=20))
    scene.add_game_object(exit_btn)

    return scene
