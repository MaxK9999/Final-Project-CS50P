import pygame, random, time


# Entities and their location
class Collectible:
    def __init__(self, x: float, y: float, sprite: pygame.Surface):
        self.x = x
        self.y = y
        self.sprite = sprite
        self.rect = self.sprite.get_rect()
    
    # Update entity sprite loaction and state
    def update(self):
        pass
    
    # Render entity sprite on the screen
    def render(self, screen: pygame.Surface):
        screen.blit(self.sprite, (self.x, self.y))

    # Randomize spawn location
    def randomize_position(self):
        self.x = random.randint(60, 1220)
        self.y = random.randint(60, 650)
        self.rect.x = self.x
        self.rect.y = self.y  



# Player class with all the attributes
class Player:
    def __init__(self, x: float, y: float, sprite: pygame.Surface):
        self.x = x
        self.y = y
        self.sprite = sprite
        self.speed = 200
        self.angle = 0
        self.health = 100
        self.direction = "up"
        self.moving = False
        self.rect = self.sprite.get_rect()

    # Update player's sprite location and state
    def update(self, deltatime):
        if self.moving:
            self.move(deltatime) 
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

    # Render player's sprite on the screen
    def render(self, screen: pygame.Surface):
        screen.blit(self.sprite, (self.x, self.y))


    def set_angle(self, new_angle: int) -> None:
        rotation = new_angle - self.angle
        self.sprite = pygame.transform.rotate(self.sprite, rotation)
        self.angle = new_angle


    def move(self, deltatime):
        # Values for directions
        if self.direction == "up":
            self.y -= self.speed * deltatime
        elif self.direction == "down":
            self.y += self.speed * deltatime
        elif self.direction == "left":
            self.x -= self.speed * deltatime
        elif self.direction == "right":
            self.x += self.speed * deltatime
        
        if self.x < 20 or self.x > 1260 or self.y < 20 or self.y > 700:
            self.decrease_health(self.health)

    def collect_item(self):
        self.score += 1

    
    def decrease_health(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.manager.set.scene("death")



class Text:
    def __init__(self, x, y, text: str):
        self.x = x
        self.y = y
        self.text = text
        self.font = pygame.font.SysFont("Arial Black", 36)
    

    def update(self):
        pass
    

    def render(self, screen: pygame.Surface):
        self.rendered = self.font.render(self.text, True, "white")
        screen.blit(self.rendered, (self.x, self.y))



class SceneManager:
    def __init__(self):
        self.scenes = {}
        self.quit = False

    def initialize(self, scenes: dict, starting_scene: str):
        self.scenes = scenes
        self.current_scene = self.scenes[starting_scene]
    
    def set_scene(self, new_scene: str):
        self.current_scene = self.scenes[new_scene]

    def get_scene(self):
        return self.current_scene
    
    def quit_game(self):
        self.quit = True
    
    def run(self):
        while not self.quit:
            self.current_scene.run()



class Scene:
    def __init__(self, manager: SceneManager, screen: pygame.Surface, sprites: dict):
        self.manager = manager 
        self.screen = screen
        self.sprites = sprites



class StartScene(Scene):
    def __init__(self, manager: SceneManager, screen: pygame.Surface, sprites: dict):
        super().__init__(manager, screen, sprites)


    def run(self):
        self.screen.fill((0, 0, 0))
        title_text = Text(600, 200, "2D DOOMSLAYER")
        start_text = Text(600, 400, "Press SPACE to start!")

        title_text.render(self.screen)
        start_text.render(self.screen)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.manager.set_scene("main")



class DeathScene(Scene):
    def __init__(self, manager: SceneManager, screen: pygame.Surface, sprites: dict, score: int):
        super().__init__(manager, screen, sprites)
        self.score = score

    def run(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.manager.set_scene("main")
                elif event.key == pygame.K_q:
                    self.manager.set_scene("start")



class MainScene(Scene):
    def __init__(self, manager: SceneManager, screen: pygame.Surface, sprites: dict):
        super().__init__(manager, screen, sprites)


    def run(self):
        if self.player.rect.colliderect(self.collectible.rect):
            self.collectible.randomize_position()
            self.player.speed += 50
            self.collect_sound.play()
            self.player.collect_item()
            self.score += 1
            self.text.text = f"Score: {self.score}"

        if self.player.health <= 0:
            self.manager.set_scene("death")



# Game class with all according properties
class Game:
    # Render screen and initialize game
    def __init__(self):
        pygame.init()
        self.running = True
        self.screen = pygame.display.set_mode((1280, 720))
        self.sprites = self.load_sprites()
        self.player = Player(600, 300, self.sprites["doom"])
        self.collectible = Collectible(200, 200, self.sprites["entity"])
        self.collectible.randomize_position()
        self.score = 0
        self.text = Text(600, 50, str(self.score))

        self.keybinds = {
            pygame.K_w: (0, "up"),
            pygame.K_d: (270, "right"),
            pygame.K_s: (180, "down"),
            pygame.K_a: (90, "left")
        }

        pygame.mixer.music.load("sfx/Eternal.mp3")
        pygame.mixer.music.set_volume(0.25)
        pygame.mixer.music.play()

        self.collect_sound = pygame.mixer.Sound("sfx/Die.mp3")
        self.collect_sound.set_volume(0.5)   

        self.scene_manager = SceneManager()
        self.scenes = {
            "start": StartScene(self.scene_manager, self.screen, self.sprites),
            "main": MainScene(self.scene_manager, self.screen, self.sprites),
            "death": DeathScene(self.scene_manager, self.screen, self.sprites, self.score)
        } 
        self.scene_manager.initialize(self.scenes, "start")


    # Poll events function
    def poll_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            if event.type == pygame.KEYDOWN and event.key in self.keybinds:
                self.player.set_angle(self.keybinds[event.key][0])
                self.player.direction = self.keybinds[event.key][1]
                self.player.moving = True
            
            if event.type == pygame.KEYUP and event.key in self.keybinds:
                if self.keybinds[event.key][1] == self.player.direction:
                    self.player.moving = False

    # Update screen
    def update(self):
        # Compute delta time
        now = time.time()
        deltatime = now - self.previous_time
        self.previous_time = now
        self.player.update(deltatime)
        self.collectible.update()

        # Detect collisions
        if self.player.rect.colliderect(self.collectible.rect):
            self.collectible.randomize_position()
            self.player.speed += 50
            self.collect_sound.play()
            self.score += 1
        
        self.text.update()
        self.text.text = str(self.score)
    
    # Render screen and sprites
    def render(self):
        self.screen.fill("black")
        self.screen.blit(self.sprites["background"], (0, 0))
        self.player.render(self.screen)
        self.collectible.render(self.screen)
        self.text.render(self.screen)
        pygame.display.update() 

    # Run game
    def run(self):
        self.previous_time = time.time()
        while self.running:
            self.poll_events()
            self.update()
            self.render()
        pygame.quit()

    # Load sprites
    def load_sprites(self) -> dict:
        sprites = {}
        sprites["doom"] = pygame.image.load("sprites/doom-guy-neutral.png").convert_alpha()
        sprites["background"] = pygame.image.load("sprites/hell.jpg").convert_alpha()
        sprites["entity"] = pygame.image.load("sprites/enemy.png").convert_alpha()

        # Downscale sprites
        sprites["doom"] = pygame.transform.scale(sprites["doom"], (60, 52))
        sprites["entity"] = pygame.transform.scale(sprites["entity"], (80, 80))


        return sprites
    



game = Game()
game.run()