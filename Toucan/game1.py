"""Test game using Toucan game engine."""
import random
from toucan import Toucan, Component, Node
from toucan import Vector2, Vector3
from toucan import SpriteRenderer
from toucan import AnimatedSpriteRenderer
from toucan import RectangleShape
from toucan import CircleShape
from toucan import BoxCollider
from toucan import CircleCollider

WIDTH = 500
HEIGHT = 400

class PlayerController(Component):
    """A component to control the player."""

    def __init__(self):
        """Initialize the component."""
        Component.__init__(self, "PlayerController")
        self.delta_x = 1
        self.delta_y = 1

    def update(self, time_delta: float):
        """Update this component."""
        self.parent.position.x += self.delta_x
        self.parent.position.y += self.delta_y

        if self.parent.position.x < 0 or self.parent.position.x > WIDTH:
            self.delta_x *= -1

        if self.parent.position.y < 0 or self.parent.position.y > HEIGHT:
            self.delta_y *= -1

    def draw(self):
        """Draw this component."""
        pass


class EnemyController(Component):
    """A component to control the enemy."""

    def __init__(self):
        """Initialize the component."""
        Component.__init__(self, "EnemyController")
        self.delta_x = random.random() * 2.0
        self.delta_y = random.random() * 2.0

    def update(self, time_delta: float):
        """Update this component."""
        self.parent.position.x += self.delta_x
        self.parent.position.y += self.delta_y

        if self.parent.position.x < 0 or self.parent.position.x > WIDTH:
            self.delta_x *= -1

        if self.parent.position.y < 0 or self.parent.position.y > HEIGHT:
            self.delta_y *= -1

    def draw(self):
        """Draw this component."""
        pass


def print_tree(node: Node, level: int = 1):
    """Print the node tree to the console."""

    indent = " " * level
    print(indent + node.name)
    for component in node.components:
        print(indent + " Component %s (%s)" % (component.name, type(component)))
    for node in node.children:
        print_tree(node, level + 1)

def main():
    """The entry point."""

    engine = Toucan("Toucan Game 1", WIDTH, HEIGHT)

    # player_sprite = engine.load_image("assets/player.png")

    player = Node("ThePlayer")
    player.position.x = 100
    player.position.y = 100
    #player.add_componenet(AnimatedSpriteRenderer(player_sprite))
    player.add_componenet(RectangleShape(20, 20))
    player.add_componenet(BoxCollider())
    player.add_componenet(PlayerController())

    bullets = Node("Bullets")
    enemies = Node("Enemies")

    for i in range(20):
        enemy = Node(f"Enemy-{i + 1}")
        enemy.position.x = random.randint(0, WIDTH)
        enemy.position.y = random.randint(0, HEIGHT)
        #enemie.add_componenet(CircleCollider(5))
        enemy.add_componenet(EnemyController())
        enemy.add_componenet(CircleShape(5))
        enemies.add_node(enemy)

    engine.add_node(enemies)
    engine.add_node(player)
    engine.add_node(bullets)

    print_tree(engine.root)

    engine.run()


if __name__ == "__main__":
    main()
