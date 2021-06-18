"""This is a simple game which has been created to get familiar with the
pygame library. All credits go to Tech With Tim as his tutorial was followed.
Of course, I have made a few small changes, mostly with how the code is
organized, but the game itself is almost exactly the same as Tim's. Again, a
huge thank you to him for his great tutorial.
"""

__author__ = ["Sam Kasbawala"]
__credits__ = ["Sam Kasbawala"]
__license__ = "MIT"
__maintainer__ = "Sam Kasbawala"
__email__ = "samarth.kasbawala@uconn.edu"
__status__ = "Production"


import pygame
import os


# Initialize fonts -----------------------------------------------------------
pygame.font.init()
HEALTH_FONT = pygame.font.SysFont("comicsans", 40)
WINNER_FONT = pygame.font.SysFont("comicsans", 100)


# Initialize sounds ----------------------------------------------------------
pygame.mixer.init()
BULLET_HIT = pygame.mixer.Sound(os.path.join("assets", "hit.mp3"))
BULLET_FIRE = pygame.mixer.Sound(os.path.join("assets", "fire.mp3"))


# Constants ------------------------------------------------------------------
WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
FPS = 60

SPACE = pygame.transform.scale(
    pygame.image.load(os.path.join("assets", "space.png")), (WIDTH, HEIGHT))


# Spacship constants ---------------------------------------------------------
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40
SPACESHIP_VELOCITY = 5
BULLET_VELO = 10
BULLET_HEIGHT = 4
BULLET_WIDTH = 8
MAX_BULLETS = 3
MAX_HEALTH = 7


# Middle border constants ----------------------------------------------------
BORDER_WIDTH = 10
BORDER = pygame.Rect(WIDTH/2 - BORDER_WIDTH/2,
                     0,
                     BORDER_WIDTH,
                     HEIGHT)


# Colors ---------------------------------------------------------------------
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)


# Events ---------------------------------------------------------------------
LEFT_HIT = pygame.USEREVENT + 1
RIGHT_HIT = pygame.USEREVENT + 2


# Game items -----------------------------------------------------------------
class Spaceship(pygame.Rect):
    """Superclass for Spaceship object. Inherits from pygame.Rect."""

    def __init__(self, left, top, width, height):
        """Custom constructor for Spaceship base class. This class is not
        mean to be instantiated.

        Args:
            left (int): left most coordinate of object
            top (int): top most coordinate of object
            width (int): width (in pixels) of object
            height (int): height (in pixels) of object
        """

        # Call constructor of super class
        super(Spaceship, self).__init__(left, top, width, height)

        # Initialize object attributes
        self.velo = SPACESHIP_VELOCITY
        self.max_bullets = MAX_BULLETS
        self.health = MAX_HEALTH
        self.fire_sound = BULLET_FIRE
        self.bullets = []

    def _load_image(self, image_path, angle):
        """[summary]

        Args:
            image_path (string): path to image file
            angle (int): integer value on how much to rotate image
        """

        # Load image and rotate. save as object attribute
        image = pygame.image.load(image_path)
        self.entity = pygame.transform.rotate(
            pygame.transform.scale(image, (self.width, self.height)), angle)


class LeftSpaceship(Spaceship):
    """Spaceship object for the left sided player. Extends the Spaceship
    baseclass.
    """

    def __init__(self, left, top, width, height, image_path):
        """Custom constructor for left player spaceship class.

        Args:
            left (int): left most coordinate of object
            top (int): top most coordinate of object
            width (int): width (in pixels) of object
            height (int): height (in pixels) of object
            image_path (string): string indicating path to image file
        """

        # Call base class constructor and load the image
        super().__init__(left, top, width, height)
        self._load_image(image_path, 90)

        # Switch height and width because the image was rotated 90 degrees
        self.height, self.width = self.width, self.height

    def move(self, keys_pressed):
        """Move spaceship object depending on the key that is pressed. 'A' moves
        left, 'D' moves right, 'W' moves up, and 'S' moves down.

        Args:
            keys_pressed (bools): sequence of boolean values representing the
                state of every key on the keyboard
        """

        # Moving the left spaceship
        if keys_pressed[pygame.K_a] and self.x - self.velo > 0:
            self.x -= self.velo
        if keys_pressed[pygame.K_d] and self.x + self.width + self.velo < BORDER.x:
            self.x += self.velo
        if keys_pressed[pygame.K_w] and self.y - self.velo > 0:
            self.y -= self.velo
        if keys_pressed[pygame.K_s] and self.y + self.height + self.velo < HEIGHT:
            self.y += self.velo

    def shoot(self):
        """Method to shoot the bullet from the spaceship"""

        bullet = pygame.Rect(self.x + self.width, self.y + self.height /
                             2 - BULLET_HEIGHT/2, BULLET_WIDTH, BULLET_HEIGHT)
        self.bullets.append(bullet)
        self.fire_sound.play()


class RightSpaceship(Spaceship):
    """Spaceship object for the right sided player. Extends the Spaceship
    baseclass.
    """

    def __init__(self, left, top, width, height, image_path):
        """Custom constructor for right player spaceship class.

        Args:
            left (int): left most coordinate of object
            top (int): top most coordinate of object
            width (int): width (in pixels) of object
            height (int): height (in pixels) of object
            image_path (string): string indicating path to image file
        """

        # Call base class constructor and load the image
        super().__init__(left, top, width, height)
        self._load_image(image_path, -90)

        # Switch height and width because the image was rotated 90 degrees
        self.height, self.width = self.width, self.height

    def move(self, keys_pressed):
        """Move spaceship object depending on the key that is pressed.
        'ARROW_LEFT' moves left, 'ARROW_RIGHT' moves right, 'ARROW_UP' moves
        up, and 'ARROW_DOWN' moves down.

        Args:
            keys_pressed (bools): sequence of boolean values representing the
                state of every key on the keyboard
        """

        # Moving the right spaceship
        if keys_pressed[pygame.K_LEFT] and self.x - self.velo > BORDER.x + BORDER.width:
            self.x -= self.velo
        if keys_pressed[pygame.K_RIGHT] and self.x + self.width + self.velo < WIDTH:
            self.x += self.velo
        if keys_pressed[pygame.K_UP] and self.y - self.velo > 0:
            self.y -= self.velo
        if keys_pressed[pygame.K_DOWN] and self.y + self.height + self.velo < HEIGHT:
            self.y += self.velo

    def shoot(self):
        """Method to shoot the bullet from the spaceship"""

        bullet = pygame.Rect(self.x, self.y + self.height /
                             2 - BULLET_HEIGHT/2, BULLET_WIDTH, BULLET_HEIGHT)
        self.bullets.append(bullet)
        self.fire_sound.play()


# Set Caption ----------------------------------------------------------------
pygame.display.set_caption("Spaceship Battle")


# Functions to edit the window -----------------------------------------------
def draw_window(left_ship, right_ship):
    """Updates the display with the proper movements of the spaceship objects
    and the bullets that are fired.

    Args:
        left_ship (LeftSpaceship): instance of left spaceship object
        right_ship (RightSpaceship): instance of right spaceship object
    """

    # Load space background and middle border
    WIN.blit(SPACE, (0, 0))
    pygame.draw.rect(WIN, BLACK, BORDER)

    # Place left and right player objects
    WIN.blit(right_ship.entity, (right_ship.x, right_ship.y))
    WIN.blit(left_ship.entity, (left_ship.x, left_ship.y))

    # Indicate the health for both players
    left_health = HEALTH_FONT.render(f'Health: {left_ship.health}', 1, WHITE)
    right_health = HEALTH_FONT.render(f'Health: {right_ship.health}', 1, WHITE)
    WIN.blit(left_health, (10, 10))
    WIN.blit(right_health, (WIDTH - right_health.get_width() - 10, 10))

    # Draw bullets
    for bullet in left_ship.bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)
    for bullet in right_ship.bullets:
        pygame.draw.rect(WIN, RED, bullet)

    # Update the screen
    pygame.display.update()


def handle_bullets(left_ship, right_ship):
    """Method to move fired bullets and detect collisions between objects.

    Args:
        left_ship (LeftSpaceship): instance of left spaceship object
        right_ship (RightSpaceship): instance of right spaceship object
    """

    # Loop through left spaceship bullets
    for bullet in left_ship.bullets:

        # Move bullet
        bullet.x += BULLET_VELO

        # Check if the bullet hit the other player
        if right_ship.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RIGHT_HIT))
            left_ship.bullets.remove(bullet)

        # Check if the bullet is out of bounds
        elif bullet.x > WIDTH:
            left_ship.bullets.remove(bullet)

        # Check if bullet hit other bullet
        else:
            for bullet_right in right_ship.bullets:
                if bullet_right.colliderect(bullet):
                    left_ship.bullets.remove(bullet)
                    right_ship.bullets.remove(bullet_right)
                    BULLET_HIT.play()
                    break

    # Loop through right spaceship bullets
    for bullet in right_ship.bullets:

        # Move bullet
        bullet.x -= BULLET_VELO

        if left_ship.colliderect(bullet):
            pygame.event.post(pygame.event.Event(LEFT_HIT))
            right_ship.bullets.remove(bullet)

        # Check if the bullet is out of bounds
        elif bullet.x < 0:
            right_ship.bullets.remove(bullet)

        # Check if bullet hit other bullet
        else:
            for bullet_left in left_ship.bullets:
                if bullet_left.colliderect(bullet):
                    right_ship.bullets.remove(bullet)
                    left_ship.bullets.remove(bullet_left)
                    BULLET_HIT.play()
                    break


def handle_winner(winner_text):
    """Method to show winner screen if there is a winner.

    Args:
        winner_text (string): text to be displayed
    """

    # Load the text to be displayed
    text = WINNER_FONT.render(winner_text, 1, WHITE)
    WIN.blit(text, (WIDTH/2 - text.get_width()/2,
                    HEIGHT/2 - text.get_height()/2))

    # Update the window and keep the winner screen for 5 seconds
    pygame.display.update()
    pygame.time.delay(5000)


# Main function to run game --------------------------------------------------
def main():
    """Main function for the game. Contains a forever loop to keep game
    running unless user exits out.
    """

    # Create left player and right player space ship objects
    left_ship = LeftSpaceship(100,
                              HEIGHT/2,
                              SPACESHIP_WIDTH,
                              SPACESHIP_HEIGHT,
                              os.path.join("assets", "spaceship_yellow.png"))

    right_ship = RightSpaceship(800,
                                HEIGHT/2,
                                SPACESHIP_WIDTH,
                                SPACESHIP_HEIGHT,
                                os.path.join("assets", "spaceship_red.png"))

    # Clock to control framerate
    clock = pygame.time.Clock()

    run = True
    while run:

        clock.tick(FPS)

        # Check for events
        for event in pygame.event.get():

            # If user issues clicks the exit button
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            # Check which keys have been pressed down
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(left_ship.bullets) < left_ship.max_bullets:
                    left_ship.shoot()

                if event.key == pygame.K_RCTRL and len(right_ship.bullets) < right_ship.max_bullets:
                    right_ship.shoot()

            # If the left player has been hit
            if event.type == LEFT_HIT:
                left_ship.health -= 1
                BULLET_HIT.play()

            # If the right player has been hit
            if event.type == RIGHT_HIT:
                right_ship.health -= 1
                BULLET_HIT.play()

        # Declare a winner if there is one
        winner = ""

        if left_ship.health <= 0:
            winner = "Red Wins!"

        if right_ship.health <= 0:
            winner = "Yellow Wins!"

        if winner != "":
            handle_winner(winner)
            break

        # Get the key press and move the player objects
        keys_pressed = pygame.key.get_pressed()
        left_ship.move(keys_pressed)
        right_ship.move(keys_pressed)

        # Handle the fired bullets and update the window
        handle_bullets(left_ship, right_ship)
        draw_window(left_ship, right_ship)

    # Restart the game once a player wins
    main()


# Main is called when the module is run directly
if __name__ == "__main__":
    main()
