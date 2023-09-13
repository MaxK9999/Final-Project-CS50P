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
    def __init__(self, x: float, y: float, sprite: pygame.Surface, scene_manager):
        self.x = x
        self.y = y
        self.sprite = sprite
        self.speed = 200
        self.angle = 0
        self.health = 100
        self.direction = "up"
        self.moving = False
        self.rect = self.sprite.get_rect()
        self.scene_manager = scene_manager

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
        
        # Death screen when out of bounds
        if self.x < 20 or self.x > 1260 or self.y < 20 or self.y > 700:
            self.scene_manager.set_scene("death")
        

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
    
    def reset_main(self) -> None:
        new_scene = MainScene(self,
                              self.scenes["main"].screen,
                              self.scenes["main"].sprites,
                              )
        self.scenes["main"] = new_scene


class Scene:
    def __init__(self, manager: SceneManager, screen: pygame.Surface, sprites: dict):
        self.manager = manager 
        self.screen = screen
        self.sprites = sprites
    
    def update(self):
        pass

    def render(self):
        pass

    def poll_events(self):
        pass


class MainScene(Scene):
    def __init__(self, manager: SceneManager, screen: pygame.Surface, sprites: dict):
        super().__init__(manager, screen, sprites)
        self.previous_time = None
        self.player = Player(600, 300, self.sprites["doom"], self.manager)
        self.collectible = Collectible(200, 200, self.sprites["entity"])
        self.collectible.randomize_position()
        self.score = 0
        self.text = Text(600, 80, str(self.score))
        self.milestones = {5: "Penta Kill!", 
                           10: "Killing Frenzy!", 
                           15: "Murder Spree!",
                           20: "Killtastrophe!",
                           25: "Mother of god...",
                           30: "Nuclear!!!",
                           40: "George Bush would be proud",
                           50: "G E N O C I D E",
                           60: "Genghis Khan reincarnate",
                           70: "BLACK DEATH",
                           100: "G O D L I K E"}
        
        self.displayed_milestones = set()
        self.displayed_message = None

        self.keybinds = {
            pygame.K_w: (0, "up"),
            pygame.K_d: (270, "right"),
            pygame.K_s: (180, "down"),
            pygame.K_a: (90, "left")
        }
    
        self.collect_sound = pygame.mixer.Sound("sfx/Die.mp3")
        self.collect_sound.set_volume(0.5)  

    def update(self):
        # Compute delta time
        if self.previous_time is None:
            self.previous_time = time.time()
        now = time.time()
        deltatime = now - self.previous_time
        self.previous_time = now

        self.player.update(deltatime)
        self.collectible.update()

        for milestone, message in self.milestones.items():
            if self.score >= milestone and milestone not in self.displayed_milestones:
                self.display_message(message)
                self.displayed_milestones.add(milestone)
    
        # Detect collisions
        if self.player.rect.colliderect(self.collectible.rect):
            self.collectible.randomize_position()
            self.player.speed += 50
            self.collect_sound.play()
            self.score += 1

            for milestone, message in self.milestones.items():
                if self.score == milestone:
                    self.display_message(message)
                    self.displayed_milestones.add(milestone)
        
        self.text.update()
        self.text.text = str(self.score)
    

    def display_message(self, message):
        self.displayed_message = message
    

    def render(self):
        self.screen.fill("black")
        self.screen.blit(self.sprites["background"], (0, 0))
        self.player.render(self.screen)
        self.collectible.render(self.screen)
        self.text.render(self.screen)

        if self.displayed_message:
            message_text = Text(80, 30, self.displayed_message)
            message_text.render(self.screen)

        pygame.display.update() 

        
    def poll_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.manager.quit_game()
            
            if event.type == pygame.KEYDOWN and event.key in self.keybinds:
                self.player.set_angle(self.keybinds[event.key][0])
                self.player.direction = self.keybinds[event.key][1]
                self.player.moving = True
            
            if event.type == pygame.KEYUP and event.key in self.keybinds:
                if self.keybinds[event.key][1] == self.player.direction:
                    self.player.moving = True


class StartScene(Scene):
    def __init__(self, manager: SceneManager, screen: pygame.Surface, sprites: dict):
        super().__init__(manager, screen, sprites)
        self.font = pygame.font.SysFont("Arial Black", 36)
        self.text1 = "Welcome Mortal"
        self.text1_x = 450
        self.text1_y = 200
        self.text2 = "Press SPACE to start!"
        self.text2_x = 400
        self.text2_y = 300

    def update(self):
        pass

    def render(self):
        self.screen.fill("#1A1A1A")
        self.screen.blit(self.font.render(self.text1, True, "#8B2323"), (self.text1_x, self.text1_y))
        self.screen.blit(self.font.render(self.text2, True, "white"), (self.text2_x, self.text2_y))
        pygame.display.update()

    def poll_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.manager.quit_game()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.manager.set_scene("main")


class DeathScene(Scene):
    def __init__(self, manager: SceneManager, screen: pygame.Surface, sprites: dict, score: int):
        super().__init__(manager, screen, sprites)
        self.font = pygame.font.SysFont("Arial Black", 36)
        self.screen.fill("black")
        self.text1 = "Press R to restart, or Q to exit game."
        self.text1_x = 300
        self.text1_y = 500
        self.text2 = f"Score: {score}"
        self.text2_x = 400
        self.text2_y = 500

        self.death_sound = pygame.mixer.Sound("sfx/dead.mp3")
        self.death_sound.set_volume(0.25)

    def update(self):
        pass

    def render(self):
        self.screen.blit(self.sprites["death-background"], (0, 0))
        self.screen.blit(self.font.render(self.text1, True, "#8B2323"), (self.text1_x, self.text1_y))
        pygame.display.update()
    
    def poll_events(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.manager.reset_main()
                    self.manager.set_scene("main")
                if event.key == pygame.K_q:
                    self.manager.quit_game()
            elif event.type == pygame.QUIT:
                self.manager.quit_game()
        
        pygame.mixer.music.pause()
        self.death_sound.play()


# Game class with all according properties
class Game:
    # Render screen and initialize game
    def __init__(self):
        pygame.init()
        self.running = True
        self.screen = pygame.display.set_mode((1280, 720))
        self.sprites = self.load_sprites()
        self.scene_manager = SceneManager()

        pygame.mixer.music.load("sfx/Eternal.mp3")
        pygame.mixer.music.set_volume(0.25)
        pygame.mixer.music.play()

        self.scenes = {
            "start": StartScene(self.scene_manager, self.screen, self.sprites),
            "main": MainScene(self.scene_manager, self.screen, self.sprites),
            "death": DeathScene(self.scene_manager, self.screen, self.sprites, 0)
        } 
        self.scene_manager.initialize(self.scenes, "start")


    # Run game
    def run(self):
        while self.running:
            self.scene_manager.current_scene.poll_events()
            self.scene_manager.current_scene.update()
            self.scene_manager.current_scene.render()
        
            if self.scene_manager.quit == True:
                self.running = False

        pygame.quit()

    # Load sprites
    def load_sprites(self) -> dict:
        sprites = {}
        sprites["doom"] = pygame.image.load("sprites/doom-guy-neutral.png").convert_alpha()
        sprites["background"] = pygame.image.load("sprites/hell.jpg").convert_alpha()
        sprites["death-background"] = pygame.image.load("sprites/dead.jpg").convert_alpha()
        sprites["entity"] = pygame.image.load("sprites/enemy.png").convert_alpha()

        # Downscale sprites
        sprites["doom"] = pygame.transform.scale(sprites["doom"], (60, 52))
        sprites["entity"] = pygame.transform.scale(sprites["entity"], (80, 80))

        return sprites
    

game = Game()
game.run()