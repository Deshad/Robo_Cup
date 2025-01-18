from utils import utils 
from models.player import Player
from utils.size import *
from utils import get_direction, get_distance
import math

class BlueGoalKeeper(Player):
    def __init__(self, x,y,name, number, color,radius,img=None, ban_cycles=0,role=None,direction=0):
        super().__init__(x,y,name, number, color,radius,img, ban_cycles,role,direction)

    def decide_action(self, ball, players):
        decisions = []
        if self.own_half(ball):
            if self.is_in_goal_area(ball):
                if ball['owner_number'] == self.number:
                    decisions.append(self.pass_to_teammates(players))
                else:
                    decisions.append(self.intercept_ball(ball))
            else:
                decisions.append(self.adjust_self(ball))
        else:
            decisions.append(self.stand_still())
        return decisions


    def owns_ball(self, ball):
        return ball['owner_number'] == self.number

    def is_in_goal_area(self,ball):#属于正坐标系
        x = ball['x']
        y = ball['y']
        x1 = 350
        x2 = 450
        y1 = -150
        y2 = 150
        return x1 < x < x2 and y1 < y < y2
    
    def own_half(self,ball):
        x = ball['x']
        x1 = 0
        x2 = 450
        return x1 < x < x2
    
    def kick(self, direction, power):
        # Placeholder for kicking logic. In a real game, this would interact with the ball object.
        print(f"Kicking in direction {direction} with power {power}")


    def serve_ball(self):
        return {'type': 'grab', 'player_number': self.number}

    def chase_ball(self, ball):
        direction = utils.get_direction({'x': self.x, 'y': self.y}, {'x': ball['x'], 'y': ball['y']})
        return {
            'type': 'move', 
            'player_number': self.number, 
            'destination': {'x': ball['x'], 'y': ball['y']}, 
            'direction': direction, 
            'speed': 10,
            'has_ball':False
        }
    
    def intercept_ball(self, ball):
        """Move towards the ball to intercept it."""
        direction_to_ball = get_direction({'x': self.x, 'y': self.y}, {'x': ball['x'], 'y': ball['y']})
        distance_to_ball = get_distance({'x': self.x, 'y': self.y}, {'x': ball['x'], 'y': ball['y']})
        if distance_to_ball > 24:
            if ball['owner_color'] == self.color:
                speed = 5
            else:
                speed = 10
            destination = {'x': ball['x'], 'y': ball['y']}
            return {
                'type': 'move',
                'player_number': self.number,
                'destination': destination,
                'direction': direction_to_ball,
                'speed': speed,  # This speed can be adjusted based on gameplay needs
                'has_ball':False
            }
        else:
            return self.grab_ball(ball)
    
    def grab_ball(self,ball):
        direction_to_ball = get_direction({'x': self.x, 'y': self.y}, {'x': ball['x'], 'y': ball['y']})
        return {
            'type': 'grab',
            'player_number': self.number,
            'direction': direction_to_ball,
        }

    def pass_to_teammates(self, players):
        teammate = self.find_closest_teammate(players)
        if teammate:
            direction = utils.get_direction({'x': self.x, 'y': self.y}, {'x': teammate['x'], 'y': teammate['y']})
            return {'type': 'kick', 'player_number': self.number, 'direction': direction, 'power': 50}
        else:
            return None

    def find_closest_teammate(self, players):
        closest_distance = float('inf')
        closest_player = None
        for player in players:
            if player['number'] != self.number:
                distance = utils.get_distance({'x': self.x, 'y': self.y}, {'x': player['x'], 'y': player['y']})
                if distance < closest_distance:
                    closest_distance = distance
                    closest_player = player
        return closest_player

    def adjust_self(self, ball):
        # goal_x = -460 if self.color == 'red' else 460
        goal_x = 450 #毕竟特化为蓝方守门员
        goal_y = 0  # Center of the goal
        player_x, player_y = self.x, self.y
        ball_x, ball_y = ball['x'], ball['y']

        # Calculate the angle from the goal to the ball
        angle_to_ball = math.atan2(ball_y - goal_y, ball_x - goal_x)

        # Ellipse semi-axes lengths
        a = utils.GOAL_WIDTH//2  #130 
        b = utils.GOAL_AREA_LENGTH//2 # 50

        # Find the intersection point on the ellipse boundary in the direction of the ball
        ellipse_x = goal_x + b * math.cos(angle_to_ball)
        ellipse_y = goal_y + a * math.sin(angle_to_ball)

        # Calculate the direction for the move action
        direction = math.degrees(math.atan2(ellipse_y - player_y, ellipse_x - player_x)) #注意，这里就是典型的出现direction为负的，atan2都要谨慎
        return {
            'type': 'move',
            'player_number': self.number,
            'destination': {'x': ellipse_x, 'y': ellipse_y},
            'direction': direction,
            'speed': 10,  # Speed adjustment for gameplay balance
            'has_ball':False
        }
        
    def stand_still(self):
        return {
            'type': 'move', 
            'player_number': self.number, 
            'destination': {'x':  400, 'y': 0}, 
            'direction': 0, 
            'speed': 8,
            'has_ball':False
        }