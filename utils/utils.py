import pygame as pg
import math
from .size import *
import random

def angle_difference(angle1, angle2):
    """
    Calculate the minimum difference between two angles.

    :param angle1: The first angle in degrees.
    :param angle2: The second angle in degrees.
    :return: The minimum angle difference in degrees.
    """
    # Normalize angles to be within 0 to 360 degrees
    angle1 = angle1 % 360
    angle2 = angle2 % 360

    # Calculate differences in two directions and return the smaller one
    diff = abs(angle1 - angle2) % 360
    return min(diff, 360 - diff)

def is_within_angle_to_ball(self, ball, direction):
    ball_direction = get_direction({'x': self.x, 'y': self.y}, {'x': ball['x'], 'y': ball['y']})
    # Compare the player-to-ball direction with the provided direction
    return angle_difference(direction, ball_direction) < 60

def reposition_around_ball(self, ball, direction):
    player_position = (self.x, self.y)
    print('player current position:',player_position)
    # Calculate the angle from the ball to the player
    current_angle = get_direction({'x': ball['x'], 'y': ball['y']}, {'x': self.x, 'y': self.y})
    print('current angle from ball to player:',current_angle)
    # Calculate self to ball angle
    self_to_ball_angle = get_direction({'x': self.x, 'y': self.y}, {'x': ball['x'], 'y': ball['y']})
    # Calculate self to goal angle
    self_to_goal_angle = direction
    if self_to_ball_angle - self_to_goal_angle > 0:
        angle_increment = -45
    else:
        angle_increment = 45
    new_angle = (current_angle + angle_increment) % 360
    print('new_angle:',new_angle)
    # Calculate the new position based on the new angle, with the player moving around the ball
    distance_to_ball = get_distance({'x': ball['x'], 'y': ball['y']}, {'x': self.x, 'y': self.y})
    new_x = ball['x'] + distance_to_ball * math.cos(math.radians(new_angle))
    new_y = ball['y'] + distance_to_ball * math.sin(math.radians(new_angle))
    print('new_x:',new_x)
    print('new_y:',new_y)
    # Update the player's position to the new coordinates
    return {
        'type': 'move',
        'player_number': self.number,
        'destination': {'x': new_x, 'y': new_y},
        # Keep the player facing in the original direction even after moving
        'direction': get_direction({'x': self.x, 'y': self.y}, {'x': new_x, 'y': new_y}),
        'speed': 5,
        'has_ball': False
    }

def convert_coordinate_cartesian_to_pygame(cartesian_x, cartesian_y):
    pygame_x = SCREEN_LENGTH // 2 + cartesian_x
    pygame_y = SCREEN_WIDTH // 2 - cartesian_y
    return pygame_x, pygame_y


def write_text_on_pygame_screen(screen, font_size, color, text, cartesian_x, cartesian_y, font=None):
    pygame_x, pygame_y = convert_coordinate_cartesian_to_pygame(cartesian_x, cartesian_y)
    font = pg.font.Font(font, font_size)
    text_render = font.render(text, True, color)
    screen.blit(text_render, (pygame_x, pygame_y))


#以下的代码考虑到复用性，所以暂时写在 utils，后续可以更改
def distance(cartesian_p1, cartesian_p2):
    return int(((cartesian_p1.x - cartesian_p2.x) ** 2 + (cartesian_p1.y - cartesian_p2.y) ** 2) ** 0.5)

def get_direction(p1, p2):
    x = p2['x']- p1['x']
    y = p2['y'] - p1['y']
    return math.degrees(math.atan2(y, x))


def get_distance(p1, p2):
    return int(((p1['x'] - p2['x'] ) ** 2 + (p1['y'] - p2['y'] ) ** 2) ** 0.5)

def cal_angle(player1, player2):
    delta_x = player2['x'] - player1['x']
    delta_y = player2['y'] - player1['y']
    # delta_x = player2.x - player1.x
    # delta_y = player2.y - player1.y
    angle_radians = math.atan2(delta_y, delta_x)
    angle_degrees = math.degrees(angle_radians)
    return angle_degrees


def just_grab(player1,players):
    for player in players:
        if get_distance(player1,player) <= 24:
            return False
    return True

def how_to_grab(player1,players):
    # player_position = (player1.x,player1.y)
    player_position = (player1['x'],player1['y'])
    goal = {'x':0,'y':0} 
    # 定义球场划分的网格大小
    grid_width = 100
    grid_height = 80
    # 确定周围的空区域
    empty_regions = []
    for x in range(0, SCREEN_LENGTH, grid_width):
        for y in range(0, SCREEN_WIDTH, grid_height):
            region_center = (x + grid_width // 2, y + grid_height // 2)
            is_empty = all(math.sqrt((player['x'] - region_center[0]) ** 2 + (player['y'] - region_center[1]) ** 2) > 100 for player in players)
            # is_empty = all(math.sqrt((player.x - region_center[0]) ** 2 + (player.y - region_center[1]) ** 2) > PLAYER_RADIUS for player in players)
            if is_empty:
                if -400 <= region_center[0] <= 400 and -250 <= region_center[1] <= 250:
                    empty_regions.append(region_center)

    # 计算方向
    kick_directions = []
    for region_center in empty_regions:
        direction_angle = math.atan2(region_center[1] - player_position[1], region_center[0] - player_position[0])
        if direction_angle >= 120:
            direction_degree = math.degrees(direction_angle)
            kick_directions.append(direction_degree)
    if kick_directions:
        random_direction = random.choice(kick_directions)
        return random_direction
    else:
        return get_direction(player1,goal)

def is_closest_to_ball(self,ball,players):
        own_distance = get_distance({'x': self.x, 'y': self.y}, {'x': ball['x'], 'y': ball['y']})
        for player in players:
            if player['number'] != self.number:
                if get_distance({'x': player['x'], 'y': player['y']}, {'x': ball['x'], 'y': ball['y']}) < own_distance:
                    return False
        return True