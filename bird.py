class Bird():
    def __init__(self, bird_width, bird_height, window_height, window_width, bird_img, game_display):
        self.width = bird_width
        self.height = bird_height
        self.x = (window_width - self.width)/2
        self.y = (window_height - self.height)/2
        self.speed = 0
        self.suface = bird_img
        self.game_display = game_display
        self.gravity = 0.5
        self.speed_fly = -8

    def draw(self):
        self.game_display.blit(self.suface, (int(self.x), int(self.y)))

    def update(self, mouse_click):
        self.y += self.speed + 0.5 * self.gravity
        self.speed += self.gravity
        if mouse_click == True:
            self.speed = self.speed_fly
