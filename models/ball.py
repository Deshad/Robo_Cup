import math

import pygame as pg

import utils

class Ball:
    def __init__(self, x=None, y=None, radius=None, img=None, owner=None, speed=None, direction=None):
        default_ball_image = pg.image.load(utils.BALL_IMG_LINK)
        default_ball_image = pg.transform.scale(default_ball_image, (2 * utils.BALL_RADIUS, 2 * utils.BALL_RADIUS))
        default_ball_image.convert_alpha()
        self.x = x or 0
        self.y = y or 0
        self.radius = radius or utils.BALL_RADIUS
        self.img = img or default_ball_image
        self.owner = owner
        self.speed = speed or 0
        self.direction = direction
        self.grab_direction = None 
        self.grab_x = None
        self.grab_y = None #the point where the ball is grabbed
        self.movable = True

    def draw(self, screen):
        pygame_x, pygame_y = utils.convert_coordinate_cartesian_to_pygame(self.x, self.y)
        screen.blit(
            self.img,
            (int(pygame_x) - self.radius, int(pygame_y) - self.radius)
        )
    def move(self, player):
        if self.owner:
            # print owner' color and owner'snumber
            print("owner color:",self.owner.color)
            print("owner number:",self.owner.number)
            if self.movable:
                print("ball is movable")
                self.x = self.owner.x + math.cos(self.grab_direction) * (self.owner.radius + self.radius)
                self.y = self.owner.y + math.sin(self.grab_direction) * (self.owner.radius + self.radius)
                self.grab_x = self.x
                self.grab_y = self.y
                print("ball x:",self.x, "ball y:",self.y)
                print("owner x:",self.owner.x, "owner y:",self.owner.y)
            else:
                print("ball is not movable")
                self.x = self.grab_x
                self.y = self.grab_y
                print("ball x:",self.x, "ball y:",self.y)
                print("owner x:",self.owner.x, "owner y:",self.owner.y)
        elif self.direction is not None:
            if self.speed == 0 or self.direction is None:
                return
            # Predict the ball's next position
            next_x = self.x + self.speed * math.cos(math.radians(self.direction))
            next_y = self.y + self.speed * math.sin(math.radians(self.direction))

            # Check for potential collision with each player
            for player in player:
                if player != self.owner:  # Ignore the owner of the ball
                    distance = math.hypot(next_x - player.x, next_y - player.y)
                    if distance <= (self.radius + player.radius):
                        # Adjust the ball's position to just outside the player's radius
                        overlap_distance = (self.radius + player.radius) - distance
                        adjust_x = overlap_distance * math.cos(math.radians(self.direction))
                        adjust_y = overlap_distance * math.sin(math.radians(self.direction))
                        next_x -= adjust_x
                        next_y -= adjust_y
                        # Stop the ball's movement as it has reached the player
                        self.speed = 0
                        break

            # Update the ball's position to the new calculated position
            self.x, self.y = next_x, next_y
            self.speed -= utils.FRICTION
            if self.speed < 0:
                self.speed = 0
                self.direction = None

            # Check for goal conditions
            if self.x < -utils.FOOTBALL_PITCH_LENGTH // 2 and not (-utils.GOAL_WIDTH // 2 <= self.y <= utils.GOAL_WIDTH // 2):
                self.x = -utils.FOOTBALL_PITCH_LENGTH // 2 + self.radius + 1
                self.direction = 180 - self.direction
            elif self.x > utils.FOOTBALL_PITCH_LENGTH // 2 and not (-utils.GOAL_WIDTH // 2 <= self.y <= utils.GOAL_WIDTH // 2):
                self.x = utils.FOOTBALL_PITCH_LENGTH // 2 - self.radius - 1
                self.direction = 180 - self.direction
            # Boundary conditions for top and bottom
            if self.y < -utils.FOOTBALL_PITCH_WIDTH // 2:
                self.y = -utils.FOOTBALL_PITCH_WIDTH // 2 + self.radius + 1
                self.direction = -self.direction
            elif self.y > utils.FOOTBALL_PITCH_WIDTH // 2:
                self.y = utils.FOOTBALL_PITCH_WIDTH // 2 - self.radius - 1
                self.direction = -self.direction
    # whether the owner face the ball
    def is_owner_facing(self):
        # Calculate the angle from the player to the ball
        relative_x = self.x - self.owner.x
        relative_y = self.y - self.owner.y
        angle_to_ball = math.atan2(relative_y, relative_x)
        
        # Normalize angles to be within 0 to 2*pi
        angle_to_ball = math.degrees(angle_to_ball) % 360
        owner_direction = self.owner.direction % 360

        # Calculate the absolute difference in angles and adjust for angle wrap-around
        angle_difference = min(abs(angle_to_ball - owner_direction), 360 - abs(angle_to_ball - owner_direction))

        # Check if the player is facing the ball within a 90-degree arc
        return angle_difference <= 90

    def grab(self, player):
        self.owner = player
        # relative_x = self.x - player.x
        # relative_y = self.y - player.y
        # self.grab_direction = math.atan2(relative_y, relative_x)
        # self.grab_x = player.x
        # self.grab_y = player.y
        self.grab_x = self.x
        self.grab_y = self.y
        self.movable = False
    
    def move_with_ball(self, player):
        # remember the place "has ball" occured
        self.owner = player
        relative_x = self.x - player.x
        relative_y = self.y - player.y
        self.grab_direction = math.atan2(relative_y, relative_x)
        self.grab_x = self.x
        self.grab_y = self.y
        self.movable = True
    
    @property
    def info(self):
        return {
            'x': self.x,
            'y': self.y,
            'radius': self.radius,
            'owner_color': None if self.owner is None else self.owner.color,
            'owner_number': None if self.owner is None else self.owner.number,
            'direction': self.direction,
            'speed': self.speed,
        }

    @property
    def info_reversed(self):
        owner_color = None
        if self.owner is not None:
            # print("change color")
            if self.owner.color == 'blue':
                owner_color = 'red'
            else:
                owner_color = 'blue'
        direction = self.direction
        if direction is not None:
            direction = (direction + 180) % 360
        return {
            'x': -self.x,
            'y': -self.y,
            'radius': self.radius,
            'owner_color': owner_color,
            'owner_number': None if self.owner is None else self.owner.number,
            'direction': direction,
            'speed': self.speed,
        }