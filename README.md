# Final-Project-CS50P

Video demo: https://www.youtube.com/watch?v=YAnV49_B2kc

# Description

Boom Snake is a 2D game using Pygame in Python. It's a simple game based off of the original Snake game but implemented with a Doom theme over it 
(since I'm quite a Doom fan myself). The game is controlled with either WASD or UP, DOWN, LEFT, RIGHT keys and the character gets to kill(collect) enemy sprites. 
For every sprite collected the game logs +1 to the score which is displayed in the middle of the screen and in the end your score and highscore of the session are displayed. 
For every set of "kills" there is a milestone displayed in the top left corner with a funny message.

Once a player dies by hitting the edge of the screen he/she can either restart or quit the game with the R an Q keys respectively. 
When the player restarts the background music continues playing but the score resets back to 0 so the player is given a fresh start.
Like previously mentioned the highscore for the session get's logged but as soon as the player closes the game window the progress get's lost.

I intend to learn more about JSON notation further down my coding career so I can learn how to write down the highscore in a JSON file so the progress doesn't get lost, 
and will instead be logged in the database.


# Source Files

  - project.py - Contains all the main code necessary to run the game

  - test_project.py - Contains all the test cases ran on the main file 

  - requirements.txt - Features the one and only dependency to run the game: Pygame version 2.0.1

  - sprites folder - Here you will find all the sprites used in the game

  - sfx folder - All the sound fx used in the game
    

# Tech Stack

Just Python for this project with only one external library (Pygame)

# Test Cases

Player class tests:
- test_move():
  Checks whether the movement system works correctly for the input keys.

- test_collision():
  Checks whether collision between the player sprite and the collectible works correctly.

- test_set_angle():
  Tests the set angle function to see whether the sprite is pointed towards the right angle on key input.

Start and death scene class test:
- def test_start_scene_init():
  Checks whether start_scene initializes and loads correctly through the scene manager.

- def test_death_scene_initialization():
  Same as the previous start scene test but this time with the death scene.

Score class tests:
- def test_score_initialization():
  Checks whether score initializes correctly 
  
- def test_add_score():
  Checks to see if score adding system works properly
  
- def test_update_score():
  Checks whether score updates throughout the whole game


# Future Plans

As previously mentioned I might return back to this project to change the way the highscore get's logged to log the progress inside of a JSON instead of a list as it currently does.


# About Me

My name is Maxim Koltypin, born and raised in The Netherlands in 1999 and currently working as a Marine 1st Class in the Royal Dutch Marine Corps. 

After finishing CS50X I decided to continue with my CS50 journey by taking Python next and I thouroughly enjoyed the course aswell as working on this project. 
Being my first ever experience with game development I decided to start with something small and something I could grasp easily. 
I plan on taking CS50Web next as I've noticed that I did prefer working on my first project (WRKOUT, fullstack website for CS50X final project) over this project.
