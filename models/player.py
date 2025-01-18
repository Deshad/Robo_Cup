import math

import pygame as pg
import runner
import utils
from .point import Point
#from roles import goalkeeper,defender,forward

class Player:
    def __init__(self, x, y, name, number, color, radius=utils.PLAYER_RADIUS, img=None, ban_cycles=0,role=None,direction=0):
        img_link = utils.RED_PLAYER_IMG_LINK
        if color == 'blue':
            img_link = utils.BLUE_PLAYER_IMG_LINK
        default_img = pg.image.load(img_link)
        default_img = pg.transform.scale(default_img, (2 * radius, 2 * radius))
        default_img.convert_alpha()
        self.x = x
        self.y = y
        self.name = name
        self.number = number
        self.color = color
        self.radius = radius
        self.img = img or default_img
        self.ban_cycles = ban_cycles
        self.direction = direction
        self.set_role(role)
    def draw(self, screen):
        pygame_x, pygame_y = utils.convert_coordinate_cartesian_to_pygame(self.x , self.y)
        screen.blit(self.img, (int(pygame_x)-self.radius, int(pygame_y)-self.radius))
        utils.write_text_on_pygame_screen(
            screen,
            utils.PLAYER_NUMBER_FONT_SIZE,
            utils.PLAYER_TEXTS_COLOR,
            str(self.number),
            self.x - self.radius // 2,
            self.y + self.radius // 2,
        )
        utils.write_text_on_pygame_screen(
            screen,
            utils.PLAYER_NAME_FONT_SIZE,
            utils.PLAYER_TEXTS_COLOR,
            self.name,
            self.x - self.radius,
            self.y - self.radius,
        )

    def decide_action(self, ball, players, own_half, strategic_position):
        pass

    def move(self, destination,direction, speed):
        distance = utils.distance(self, destination)
        alpha = math.atan2((destination.y - self.y), (destination.x - self.x))
        
        if distance < speed:
            self.x = destination.x
            self.y = destination.y
            self.direction = alpha
        
        else:
            alpha = math.atan2((destination.y - self.y), (destination.x - self.x))
            #alpha = direction
            self.x += speed * math.cos(alpha)
            self.y += speed * math.sin(alpha)
            self.direction = alpha

    def is_in_own_penalty_area(self):
        if self.color == 'red':
            p = Point(-utils.FOOTBALL_PITCH_LENGTH // 2, 0)
        elif self.color == 'blue':
            p = Point(utils.FOOTBALL_PITCH_LENGTH // 2, 0)
        if utils.distance(self, p) < utils.PENALTY_AREA_LENGTH:
            return True
        else:
            return False
        

    # def role(self):
    #     if self.role == 'goalkeeper':
    #         role = goalkeeper.GoalKeeper(self,self.color,self.number)
    #     elif self.role == 'defender':
    #         role = defender.Defender(self,self.color,self.number)
    #     elif self.role == 'forward':
    #         role = forward.Forward(self,self.color,self.number)
    #     #需要异常处理
    #     else:
    #         print("不匹配的身份定义")
    #     return role
    
    def set_role(self, role_type):
        if role_type == 'goalkeeper':
            #self.role = goalkeeper.GoalKeeper(self.color, self.number)
            self.role = 'goalkeeper'
        elif role_type == 'defender':
            #self.role = defender.Defender(self.color, self.number)
            self.role = 'defender'
        elif role_type == 'forward':
            #self.role = forward.Forward(self.color, self.number)
            self.role = 'forward'
        else:
            self.role = None
            # print(f"Unmatched role definition for player {self.number}")
            
    @property
    def info(self):
        return {
            'x': self.x,
            'y': self.y,
            'name': self.name,
            'number': self.number,
            'radius': self.radius,
            'ban_cycles': self.ban_cycles,
            'role': self.role
        }

    @property
    def info_reversed(self):
        return {
            'x': -self.x,
            'y': -self.y,
            'name': self.name,
            'number': self.number,
            'radius': self.radius,
            'ban_cycles': self.ban_cycles,
            'role': self.role
        }
