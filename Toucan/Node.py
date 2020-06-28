# from Component import Component
import Toucan

class Node(object):

    def __init__(self, name: str):
        self.position: Toucan.Vector3 = Toucan.Vector3(0, 0, 0)
        self.rotation: float = 0.0
        self.scale: Toucan.Vector3 = Toucan.Vector3(0, 0, 0)
        self.active: bool = True
        self.name: str = name

        self.parent = None
        self.children = []
        self.components = []

    def add_node(self, node: "Node"):
        self.children.append(node)
        node.parent = self

    def add_componenet(self, component: "Component"):
        for c in self.components:
            if type(c) == type(component):
                print(f"Component type {str(type(component))} already exists")
                return
        self.componenet.append(component)
        component.parent = self

    def get_component_by_name(self, component_name: str):
        for c in self.components:
            if n.name == component_name:
                return c
        return None

    def get_component_by_type(self, component_type: type):
        for c in self.components:
            if type(c) == component_type:
                return c
        return None

    def set_active(self, flag: bool):
        self.active = flag

    def is_active(self) -> bool:
        return self.active

