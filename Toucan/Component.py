import Toucan

class Component(object):

    def __init__(self, name: str = None):
        self.active: bool = True
        self.name: str = name
        self.parent: Node = None

    def update(self, time_delta: float):
        pass

    def draw(self):
        pass

    def set_active(self, flag: bool):
        self.active = flag

    def is_active(self) -> bool:
        return self.active


class SpriteRenderer(Component):

    def __init__(self, name: str = None):
        super().__init__(self, "SpriteRenderer" if name is None else name)

    def update(self, time_delta: float):
        pass

    def draw(self):
        pass
