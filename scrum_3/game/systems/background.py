from config import Config


class ParallaxManager:
    def __init__(self):
        self.layers = [
            {
                "image": Config.load_image("background/blue_grass.png"),
                "speed": 0.5,
                "offset": 0
            },
            {
                "image": Config.load_image("background/colored_grass.png"),
                "speed": 0.3,
                "offset": 0
            }
        ]

    def update(self, camera_x):
        for layer in self.layers:
            layer["offset"] = camera_x * layer["speed"]

    def draw(self, screen):
        screen.fill((135, 206, 235))  
        for layer in self.layers:
            img = layer["image"]
            # Calculate tiling
            x = -layer["offset"] % img.get_width()
            screen.blit(img, (x - img.get_width(), 0))
            screen.blit(img, (x, 0))