from project import StartScene, DeathScene, Player, Collectible, SceneManager, Score, MainScene
import pygame
import pytest
pygame.font.init()


# Player class tests
def test_move():
    player = Player(100, 100, pygame.Surface((10, 10)), None)
    player.direction = "up"
    player.move(0.1)

    assert player.x == 100
    assert player.y < 100

def test_collision():
    player = Player(100, 100, pygame.Surface((10, 10)), None)
    collectible = Collectible(105, 105, pygame.Surface((10, 10)))

    player.direction = "right"

    assert player.rect.colliderect(collectible.rect)


def test_set_angle():
    player = Player(100, 100, pygame.Surface((10, 10)), None)
    player.set_angle(90)
    assert player.angle == 90

    player.set_angle(180)
    assert player.angle == 180


# Start scene class test
def test_start_scene_init():
    scene_manager = SceneManager()
    start_scene = StartScene(scene_manager, pygame.Surface((800, 600)), {})
    assert start_scene.manager == scene_manager


# Death scene class test
def test_death_scene_initialization():
    scene_manager = SceneManager()
    death_scene = DeathScene(scene_manager, pygame.Surface((800, 600)), {})
    assert death_scene.manager == scene_manager
    assert death_scene.manager.get_score().score == 0


# Score class test
def test_score_initialization():
    score = Score(600, 80)
    assert score.score == 0

def test_add_score():
    score = Score(600, 80)
    score.add_score()
    assert score.score == 1

def test_update_score():
    score = Score(600, 80)
    score.score = 10
    score.update()
    assert score.text == "10"
