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
        
# Text class 
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

# Initializes a score that keeps track of how many sprites have been collected
class Score:
    def __init__(self, x, y) -> None:
        self.font = pygame.font.SysFont("Arial Black", 40)
        self.score = 0
        self.text = str(self.score)
        self.x = x
        self.y = y

    def add_score(self):
        self.score += 1

    def update(self):
        self.text = str(self.score)
    
    def render(self, screen: pygame.Surface):
        screen.blit(self.font.render(self.text, True, "white"), (self.x, self.y))

# Manager of all scenes, includes score mapping
class SceneManager:
    def __init__(self):
        self.scenes = {}
        self.quit = False
        self.score = Score(600, 80)  # Initialize score here
        self.highscore = 0

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
        self.score.score = 0
        new_scene = MainScene(self,
                              self.scenes["main"].screen,
                              self.scenes["main"].sprites,
                              )
        self.scenes["main"] = new_scene

    def get_score(self):
        return self.score

    def add_score(self):
        self.score.add_score()

        # Update highscore if current score is higher
        if self.score.score > self.highscore:
            self.highscore = self.score.score
    
    def get_highscore(self):
        return self.highscore


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


# Main scene, main gameplay 
class MainScene(Scene):
    def __init__(self, manager: SceneManager, screen: pygame.Surface, sprites: dict):
        super().__init__(manager, screen, sprites)
        self.previous_time = None
        self.player = Player(600, 300, self.sprites["doom"], self.manager)
        self.collectible = Collectible(200, 200, self.sprites["entity"])
        self.collectible.randomize_position()
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
            pygame.K_UP: (0, "up"),
            pygame.K_d: (270, "right"),
            pygame.K_RIGHT: (270, "right"),
            pygame.K_s: (180, "down"),
            pygame.K_DOWN: (180, "down"),
            pygame.K_a: (90, "left"),
            pygame.K_LEFT: (90, "left")
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
            if self.manager.get_score().score >= milestone and milestone not in self.displayed_milestones:
                self.display_message(message)
                self.displayed_milestones.add(milestone)
    
        # Detect collisions
        if self.player.rect.colliderect(self.collectible.rect):
            self.collectible.randomize_position()
            self.player.speed += 50
            self.collect_sound.play()
            self.manager.add_score()

            for milestone, message in self.milestones.items():
                if self.manager.get_score() == milestone:
                    self.display_message(message)
                    self.displayed_milestones.add(milestone)
        
        self.manager.get_score().update()
    

    def display_message(self, message):
        self.displayed_message = message
    

    def render(self):
        self.screen.fill("black")
        self.screen.blit(self.sprites["background"], (0, 0))
        self.player.render(self.screen)
        self.collectible.render(self.screen)
        self.manager.get_score().render(self.screen)

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
    
    def get_score(self):
        return self.manager.get_score()


# Start scene
class StartScene(Scene):
    def __init__(self, manager: SceneManager, screen: pygame.Surface, sprites: dict):
        super().__init__(manager, screen, sprites)
        self.font = pygame.font.SysFont("Arial Black", 36)
        self.text = "Press SPACE to start!"
        self.text_x = 400
        self.text_y = 300

    def update(self):
        pass

    def render(self):
        self.screen.blit(self.sprites["start-background"], (0, 0))
        self.screen.blit(self.font.render(self.text, True, "white"), (self.text_x, self.text_y))
        pygame.display.update()

    def poll_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.manager.quit_game()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.manager.set_scene("main")


# Scene that plays upon death
class DeathScene(Scene):
    def __init__(self, manager: SceneManager, screen: pygame.Surface, sprites: dict):
        super().__init__(manager, screen, sprites)
        self.font = pygame.font.SysFont("Arial Black", 36)
        self.screen.fill("black")
        self.text1 = "Press R to restart, or Q to exit game."
        self.text1_x = 300
        self.text1_y = 500
        self.text2_x = 550
        self.text2_y = 100

        
    def update(self):
        pass

    def render(self):
        self.screen.blit(self.sprites["death-background"], (0, 0))
        self.screen.blit(self.font.render(self.text1, True, "#8B2323"), (self.text1_x, self.text1_y))
        self.screen.blit(self.font.render(f"Score: {self.manager.get_score().score}", True, "white"), (self.text2_x, self.text2_y))
        self.screen.blit(self.font.render(f"Highscore: {self.manager.get_highscore()}", True, "white"), (self.text2_x, self.text2_y + 50))
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
        

# Game class with all according properties
class Game:
    # Render screen and initialize game
    def __init__(self):
        pygame.init()
        self.running = True
        self.screen = pygame.display.set_mode((1280, 720))
        self.display = pygame.display.set_caption("2D BOOM SNAKE")
        self.icon = pygame.image.load("sprites/doom-guy.png")
        pygame.display.set_icon(self.icon)
        self.sprites = self.load_sprites()
        self.scene_manager = SceneManager()

        pygame.mixer.music.load("sfx/Eternal.mp3")
        pygame.mixer.music.set_volume(0.25)
        pygame.mixer.music.play(-1)

        self.scenes = {
            "start": StartScene(self.scene_manager, self.screen, self.sprites),
            "main": MainScene(self.scene_manager, self.screen, self.sprites),
            "death": DeathScene(self.scene_manager, self.screen, self.sprites)
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
        sprites["start-background"] = pygame.image.load("sprites/start-background.png").convert_alpha()
        sprites["background"] = pygame.image.load("sprites/hell.jpg").convert_alpha()
        sprites["death-background"] = pygame.image.load("sprites/dead.jpg").convert_alpha()
        sprites["entity"] = pygame.image.load("sprites/enemy.png").convert_alpha()

        # Downscale sprites
        sprites["doom"] = pygame.transform.scale(sprites["doom"], (60, 52))
        sprites["entity"] = pygame.transform.scale(sprites["entity"], (80, 80))

        return sprites


def main():
    game = Game()
    game.run()

if __name__ == "__main__":
    main()