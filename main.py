import pygame
import random
from pygame import *


class GameManager:
    def __init__(self):
        # Define constants
        self.SCREEN_WIDTH = 800
        self.SCREEN_HEIGHT = 600
        self.FPS = 60
        self.ZOMBIE_WIDTH = 90
        self.ZOMBIE_HEIGHT = 81
        self.FONT_SIZE = 31
        self.FONT_TOP_MARGIN = 26
        self.LEVEL_SCORE_GAP = 5
        self.LEFT_MOUSE_BUTTON = 1
        self.GAME_TITLE = "Whack A Zombie"
        # Initialize player's score, number of missed hits and level
        self.score = 0
        self.misses = 0
        self.level = 1
        # Initialize screen
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption(self.GAME_TITLE)
        self.background = pygame.image.load("images/bg.png")
        # Font object for displaying text
        self.font_obj = pygame.font.Font('./fonts/GROBOLD.ttf', self.FONT_SIZE)
        # Initialize the zombie's sprite sheet
        # 6 different states
        sprite_sheet = pygame.image.load("images/zombie.png")
        self.zombie = []
        self.zombie.append(sprite_sheet.subsurface(16, 0, 67, 113))
        self.zombie.append(sprite_sheet.subsurface(90, 0, 67, 113))
        self.zombie.append(sprite_sheet.subsurface(184, 0, 67, 113))
        self.zombie.append(sprite_sheet.subsurface(270, 0, 120, 113))
        self.zombie.append(sprite_sheet.subsurface(400, 0, 120, 113))
        self.zombie.append(sprite_sheet.subsurface(530, 0, 120, 113))

        # Positions of the holes in background
        self.hole_positions = []
        self.hole_positions.append((381, 295))
        self.hole_positions.append((119, 366))
        self.hole_positions.append((179, 169))
        self.hole_positions.append((404, 479))
        self.hole_positions.append((636, 366))
        self.hole_positions.append((658, 232))
        self.hole_positions.append((464, 119))
        self.hole_positions.append((95, 43))
        self.hole_positions.append((603, 11))
        # Init debugger
        self.debugger = Debugger("debug")
        # Sound effects
        self.soundEffect = SoundEffect()
        # Initialize the timer
        self.timer_duration = 60  # 60 seconds

    # Calculate the player level according to his current score & the LEVEL_SCORE_GAP constant
    def get_player_level(self):
        newLevel = 1 + int(self.score / self.LEVEL_SCORE_GAP)
        if newLevel != self.level:
            # if player get a new level play this sound
            self.soundEffect.playLevelUp()
        return 1 + int(self.score / self.LEVEL_SCORE_GAP)

    # Get the new duration between the time the zombie pop up and down the holes
    # It's in inverse ratio to the player's current level
    def get_interval_by_level(self, initial_interval):
        new_interval = initial_interval - self.level * 0.15
        if new_interval > 0:
            return new_interval
        else:
            return 0.05

    # Check whether the mouse click hit the zombie or not
    def is_zombie_hit(self, mouse_position, current_hole_position):
        mouse_x = mouse_position[0]
        mouse_y = mouse_position[1]
        current_hole_x = current_hole_position[0]
        current_hole_y = current_hole_position[1]
        if (mouse_x > current_hole_x) and (mouse_x < current_hole_x + self.ZOMBIE_WIDTH) and (mouse_y > current_hole_y) and (mouse_y < current_hole_y + self.ZOMBIE_HEIGHT):
            return True
        else:
            return False

    # Update the game states, re-calculate the player's score, misses, level
    def update(self):
        # Update the player's score
        current_score_string = "SCORE: " + str(self.score)
        score_text = self.font_obj.render(current_score_string, True, (255, 255, 255))
        score_text_pos = score_text.get_rect()
        score_text_pos.centerx = self.background.get_rect().centerx
        score_text_pos.centery = self.FONT_TOP_MARGIN
        self.screen.blit(score_text, score_text_pos)
        # Update the player's misses
        current_misses_string = "MISSES: " + str(self.misses)
        misses_text = self.font_obj.render(current_misses_string, True, (255, 255, 255))
        misses_text_pos = misses_text.get_rect()
        misses_text_pos.centerx = self.SCREEN_WIDTH / 5 * 4
        misses_text_pos.centery = self.FONT_TOP_MARGIN
        self.screen.blit(misses_text, misses_text_pos)


    # Start the game's main loop
    # Contains some logic for handling animations, zombie hit events, etc..
    def game_over(self):
        # Display a game over screen

        final_score_text = self.font_obj.render("Final Score: " + str(self.score), True, (255, 255, 255))
        final_score_text_pos = final_score_text.get_rect()
        final_score_text_pos.centerx = self.SCREEN_WIDTH // 2
        final_score_text_pos.centery = self.SCREEN_HEIGHT // 2 -50

        final_misses_text = self.font_obj.render("Misses: " + str(self.misses), True, (255, 255, 255))
        final_misses_text_pos = final_misses_text.get_rect()
        final_misses_text_pos.centerx = self.SCREEN_WIDTH // 2
        final_misses_text_pos.centery = self.SCREEN_HEIGHT // 2

        restart_text = self.font_obj.render("Press 'R' to Restart", True, (255, 255, 255))
        restart_text_pos = restart_text.get_rect()
        restart_text_pos.centerx = self.SCREEN_WIDTH // 2
        restart_text_pos.centery = self.SCREEN_HEIGHT // 2 + 50

        self.screen.blit(final_score_text, final_score_text_pos)
        self.screen.blit(final_misses_text, final_misses_text_pos)
        self.screen.blit(restart_text, restart_text_pos)

        pygame.display.flip()

        # Wait for the player to press 'R' to restart
        restart_pressed = False
        while not restart_pressed:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        # Restart the game
                        self.score = 0
                        self.misses = 0
                        self.level = 1
                        self.start()
                        restart_pressed = True
    def start(self):
        cycle_time = 0
        num = -1
        loop = True
        is_down = False
        interval = 0.1
        initial_interval = 1
        frame_num = 0
        left = 0
        # Time control variables
        clock = pygame.time.Clock()
        start_time = pygame.time.get_ticks()

        for i in range(len(self.zombie)):
            self.zombie[i].set_colorkey((0, 0, 0))
            self.zombie[i] = self.zombie[i].convert_alpha()

        while loop:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    loop = False
                if event.type == MOUSEBUTTONDOWN and event.button == self.LEFT_MOUSE_BUTTON:
                    self.soundEffect.playFire()
                    if self.is_zombie_hit(mouse.get_pos(), self.hole_positions[frame_num]) and num > 0 and left == 0:
                        num = 3
                        left = 14
                        is_down = False
                        interval = 0
                        self.score += 1  # Increase player's score
                        self.level = self.get_player_level()  # Calculate player's level
                        # Stop popping sound effect
                        self.soundEffect.stopPop()
                        # Play hurt sound
                        self.soundEffect.playHurt()
                        self.update()
                    else:
                        self.misses += 1
                        self.update()
            if self.misses >= 5:
                # If misses reach 5, trigger game over
                self.soundEffect.gameOver()
                self.game_over()
                return  # Exit the loop to stop the game
            if num > 5:
                self.screen.blit(self.background, (0, 0))
                self.update()
                num = -1
                left = 0

            if num == -1:
                self.screen.blit(self.background, (0, 0))
                self.update()
                num = 0
                is_down = False
                interval = 0.5
                frame_num = random.randint(0, 8)

            mil = clock.tick(self.FPS)
            sec = mil / 1000.0
            cycle_time += sec
            if cycle_time > interval:
                pic = self.zombie[num]
                self.screen.blit(self.background, (0, 0))
                self.screen.blit(pic, (self.hole_positions[frame_num][0] - left, self.hole_positions[frame_num][1]))
                self.update()
                if is_down is False:
                    num += 1
                else:
                    num -= 1
                if num == 4:
                    interval = 0.3
                elif num == 3:
                    num -= 1
                    is_down = True
                    self.soundEffect.playPop()
                    interval = self.get_interval_by_level(initial_interval)  # get the newly decreased interval value
                else:
                    interval = 0.1
                cycle_time = 0
            # Update the display
            pygame.display.flip()
            elapsed_time = (pygame.time.get_ticks() - start_time) // 1000
            remaining_time = max(0, self.timer_duration - elapsed_time)

            # Display the timer
            timer_text = self.font_obj.render(f"TIME: {remaining_time}", True, (255, 255, 255))
            timer_text_pos = timer_text.get_rect()
            timer_text_pos.centerx = self.SCREEN_WIDTH / 5 * 1
            timer_text_pos.centery = self.FONT_TOP_MARGIN
            self.screen.blit(timer_text, timer_text_pos)
            # Check if time is up
            if remaining_time == 0:
                self.soundEffect.gameOver()
                self.game_over()
                return



# The Debugger class - use this class for printing out debugging information
class Debugger:
    def __init__(self, mode):
        self.mode = mode

    def log(self, message):
        if self.mode is "debug":
            print("> DEBUG: " + str(message))


class SoundEffect:
    def __init__(self):
        self.mainTrack = pygame.mixer.music.load("sounds/themesong.wav")
        self.fireSound = pygame.mixer.Sound("sounds/fire.wav")
        self.fireSound.set_volume(1.0)
        self.popSound = pygame.mixer.Sound("sounds/pop.wav")
        self.hurtSound = pygame.mixer.Sound("sounds/hurt.wav")
        self.levelSound = pygame.mixer.Sound("sounds/point.wav")
        self.gameoverSound = pygame.mixer.Sound("sounds/gameover.wav")
        pygame.mixer.music.play(-1)

    def playFire(self):
        self.fireSound.play()

    def stopFire(self):
        self.fireSound.stop()

    def playPop(self):
        self.popSound.play()

    def stopPop(self):
        self.popSound.stop()

    def playHurt(self):
        self.hurtSound.play()

    def stopHurt(self):
        self.hurtSound.stop()

    def playLevelUp(self):
        self.levelSound.play()

    def stopLevelUp(self):
        self.levelSound.stop()

    def gameOver(self):
        self.gameoverSound.play()

###############################################################
# Initialize the game
pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
pygame.init()

# Run the main loop
my_game = GameManager()
my_game.start()
# Exit the game if the main loop ends
pygame.quit()
