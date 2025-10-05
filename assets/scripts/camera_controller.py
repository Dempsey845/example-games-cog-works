from cogworks.components.camera import Camera
from cogworks.components.script_component import ScriptComponent
from cogworks.components.transform import Transform


class CameraController(ScriptComponent):
    """
    CameraController allows a camera to follow a target Transform with optional smoothing and offsets.
    """

    def __init__(
        self,
        target_transform: Transform,
        offset_x: float = 0,
        offset_y: float = 0,
        smoothing: float = 5.0,
        fixed: bool = False
    ):
        """
        Args:
            target_transform (Transform): The Transform of the target GameObject.
            offset_x (float): Horizontal offset from the target position.
            offset_y (float): Vertical offset from the target position.
            smoothing (float): How fast the camera follows the target. Higher = snappier.
            fixed (bool): use fixed_update(). Good for following physics objects.
        """
        super().__init__()
        self.target_transform = target_transform
        self.start_offset_x = offset_x
        self.start_offset_y = offset_y
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.smoothing = smoothing
        self.camera_component: Camera | None = None
        self.fixed = fixed

    def start(self):
        self.camera_component = self.game_object.scene.camera_component
        self.offset_x = self.start_offset_x
        self.offset_y = self.start_offset_y

    def update(self, dt: float) -> None:
        if not self.fixed:
            self.control(dt)

    def fixed_update(self, dt: float) -> None:
        if self.fixed:
            self.control(dt)

    def control(self, dt):
        if not self.camera_component:
            return

        width, height = self.game_object.scene.get_window_size()

        # Target position with offset
        target_x = self.target_transform.local_x + self.offset_x
        target_y = self.target_transform.local_y + self.offset_y

        # Current camera centre
        current_x = self.camera_component.offset_x + (width / 2) / self.camera_component.zoom
        current_y = self.camera_component.offset_y + (height / 2) / self.camera_component.zoom

        # Smoothly interpolate towards target
        lerp_x = current_x + (target_x - current_x) * min(self.smoothing * dt, 1)
        lerp_y = current_y + (target_y - current_y) * min(self.smoothing * dt, 1)

        # Center camera on the interpolated position
        self.camera_component.center_on(lerp_x, lerp_y, width, height)
