from cogworks.components.ui.ui_button import UIButton
from cogworks.components.ui.ui_image import UIImage
from cogworks.components.ui.ui_label import UILabel
from cogworks.components.ui.ui_layout import UILayout
from cogworks.components.ui.ui_transform import UITransform
from cogworks.game_object import GameObject


def setup_menu_scene(engine):
    menu_scene = engine.create_scene("Menu")

    def start_physics(go):
        engine.set_active_scene("Physics")

    def start_pong(go):
        engine.set_active_scene("Pong")

    def start_snake(go):
        print("Starting snake game")
        engine.set_active_scene("SnakeGame")

    def start_trigger_test(go):
        engine.set_active_scene("TriggerTest")

    def exit_game(go):
        engine.quit()

    # Create a layout
    layout = GameObject("MenuLayout")
    layout.add_component(UITransform(x=0.5, y=0.3, width=0.4, height=0.6, anchor="center"))
    layout.add_component(UILayout(vertical=True, spacing=10))
    menu_scene.add_game_object(layout)

    # Logo
    logo = GameObject("LogoImage")
    logo.add_component(UITransform(width=0.5, height=0.5))
    logo.add_component(UIImage("images/cog_works_icon_2.png", True))
    layout.add_child(logo)

    # Label
    title_label = GameObject("TitleLabel")
    title_label.add_component(UITransform(width=1, height=0.1))
    title_label.add_component(UILabel("Cog Works Engine Examples", bg_color=(0, 0, 0), border_radius=20))
    layout.add_child(title_label)

    # Add buttons
    pong_btn = GameObject("PongButton")
    pong_btn.add_component(UITransform(width=1, height=0.1))
    pong_btn.add_component(UIButton("Play Pong", on_click=start_pong, border_radius=20))
    layout.add_child(pong_btn)

    snake_btn = GameObject("SnakeButton")
    snake_btn.add_component(UITransform(width=1, height=0.1))
    snake_btn.add_component(UIButton("Play Snake", on_click=start_snake, border_radius=20))
    layout.add_child(snake_btn)

    physics_btn = GameObject("PhysicsButton")
    physics_btn.add_component(UITransform(width=1, height=0.1))
    physics_btn.add_component(UIButton("Play Physics Example", on_click=start_physics, border_radius=20))
    layout.add_child(physics_btn)

    trigger_btn = GameObject("TriggerButton")
    trigger_btn.add_component(UITransform(width=1, height=0.1))
    trigger_btn.add_component(UIButton("Play Trigger Example", on_click=start_trigger_test, border_radius=20))
    layout.add_child(trigger_btn)

    exit_btn = GameObject("ExitButton")
    exit_btn.add_component(UITransform(width=1, height=0.1))
    exit_btn.add_component(UIButton("Exit", on_click=exit_game, border_radius=20))
    layout.add_child(exit_btn)

    return menu_scene
