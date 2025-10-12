from cogworks.components.audio_source import AudioSource
from cogworks.components.script_component import ScriptComponent


class BackgroundMusic(ScriptComponent):
    def __init__(self):
        super().__init__()

    def start(self) -> None:
        source = AudioSource()
        source.set_clip("sounds/background.mp3")
        source.loop = True
        source.volume = 0.35
        source.play(bypass_spatial=True)
        self.game_object.add_component(source)