# forward.py
from utils import get_direction, get_distance, is_within_angle_to_ball, reposition_around_ball, is_closest_to_ball
from models import player
import math

class BlueForward(player.Player):
    def __init__(self, x,y,name, number, color,radius,img=None, ban_cycles=0,role=None,direction=0):
        super().__init__(x,y,name, number, color,radius,img, ban_cycles,role,direction)

    def decide_action(self, ball, players,opponent_players):
        strategic_position = self.calculate_strategic_position(ball, players)
        decisions = []
        if self.ball_in_attacking_area(ball):
            if self.blue_team_owns_ball(ball):
                if self.owns_ball(ball):
                    print("blue forward owns ball")
                    direction = get_direction({'x': self.x, 'y': self.y}, {'x': -450, 'y': 0})
                    if is_within_angle_to_ball(self, ball, direction):
                        print("blue forward attempts to score")
                        # if player faces the ball, attempt to score
                        decisions.append(self.attempt_to_score(ball))
                    else:
                        print("blue forward doesn't face the ball and repositions around the ball")
                        # if player doesn't face the ball, face the ball, looking at the goal
                        # direction to goal
                        decisions.append(reposition_around_ball(self, ball, direction))
                    
                else:#另一个就也跟着跑
                    decisions.append(self.move_to_strategic_position(strategic_position))
            else: #没球权
                if is_closest_to_ball(self, ball, players):#往球跑，跑到了就抓球，
                    if self.distance_to_ball_close_enough(ball):
                        print("blue forward grabs ball")
                        decisions.append(self.grab_ball(ball))
                    else: #往球跑，没跑到就继续跑
                        decisions.append(self.move_towards_ball(ball)) 
                else:
                    decisions.append(self.move_to_strategic_position(strategic_position))
        else:
            decisions.append(self.move_to_strategic_position(strategic_position)) 
            # if self.in_strategic_position():
            #     decisions.append(self.face_ball_direction(ball))
            # else:
            #     decisions.append(self.move_to_strategic_position(strategic_position))  
        return decisions
    
    def ball_in_attacking_area(self, ball):
        return ball['x'] < 75 #按定义来的，半场加中圆半径

    def blue_team_owns_ball(self, ball):
        return ball['owner_color'] == 'blue'
    
    def owns_ball(self, ball):
        return ball['owner_number'] == self.number and ball['owner_color'] == self.color
    
    def move_towards_ball(self,ball):
        # Example action to move towards the ball
        # print(f"Forward {self.number} moving towards the ball at {ball['x']}, {ball['y']}")
        direction = get_direction({'x': self.x, 'y': self.y}, {'x': ball['x'], 'y': ball['y']})
        return {
            'type': 'move',
            'player_number': self.number,
            'destination': ball,
            'direction': direction,
            'speed': 10,  # Speed might be adjusted based on the situation
            'has_ball':False
        }
    
    def grab_ball(self,ball):
        direction_to_ball = get_direction({'x': self.x, 'y': self.y}, {'x': ball['x'], 'y': ball['y']})
        return {
            'type': 'grab',
            'player_number': self.number,
            'direction': direction_to_ball,
        }

    def attempt_to_score(self, ball):
        # Example action to attempt scoring
        # print(f"Forward {self.number} attempting to score")
        goal_position = {'x': -450, 'y': 0}
        direction = get_direction({'x': self.x, 'y': self.y}, goal_position)
        if self.in_shoot_area():
            print("blue forward shoots")
            return {
                'type': 'kick',
                'player_number': self.number,
                'direction': direction,
                'power':50,  # Power might be adjusted based on distance to goal
                'has_ball':False
            }
        else:
            print("blue forward moves towards goal")
            return self.move_towards_goal()
    
    def in_shoot_area(self):
        if (self.color == 'red' and self.x > 300) or (self.color == 'blue' and self.x < -300):
            return True  #需要定义射门区域
        return False

    def calculate_strategic_position(self, ball, players):#3种情况
        if self.ball_in_attacking_area(ball):
            # Scenario 1: Ball in our attacking area
            if ball['owner_color'] != self.color and not is_closest_to_ball(self, ball, players):#(2)满足了
                # Move to a position that covers the farthest goal from the ball
                return self.calculate_offensive_strategic_position(ball, players)
            elif ball['owner_color'] == self.color and ball['owner_number'] != self.number: #(3)
                # Scenario when we own the ball or are closest to it
                return self.calculate_attacking_strategic_position(ball, players)
        else:
            return self.calculate_support_strategic_position(ball,players) #(1)满足了
        
    def choose_side_for_strategic_position(self,ball,players):#这个会返回你y选哪一个    
        #other_forward = [player for player in players if player['role'] == 'forward' and player['number'] != self.number][0]
        #other_forward_y = other_forward['y']
        #other_forward_has_ball = ball['owner_color'] == self.color and ball['owner_number'] != other_forward['number']
        # 如果队友持球,则我补弱侧,
        # 如果队友不持球,异侧则选离自己近的,同侧,则那个都离二者远的,谁相对离的近谁去
        strategic_y_left = -230
        strategic_y_right = 230

        #if other_forward_has_ball:#如果队友持球,我去另侧
        #    if other_forward_y < 0:
        #        return strategic_y_right
        #    else:
        #        return strategic_y_left
        #else:# 如果队友不持球
        #    if (self.y < 0 and other_forward_y >= 0) or (self.y >= 0 and other_forward_y < 0):# 如果我们在场地的不同侧，选择离自己近的侧翼
        #        return strategic_y_left if self.y < 0 else strategic_y_right
        #    else:# 如果我们在同一侧，选择离两人都较远但相对离自己更近的侧翼
        #        if self.y > other_forward_y: 
        #            return strategic_y_right
        #        else:
        return strategic_y_left

    def calculate_support_strategic_position(self, ball,players):
        adjusted_y = self.choose_side_for_strategic_position(ball,players)
        return {'x': 75, 'y': adjusted_y}  # Example value

    def calculate_attacking_strategic_position(self, ball, players):
        goal_area_x = -350 #我方持球,就以球门线为目标
        midpoint_x = (ball['x'] + goal_area_x) / 2 #
        # Adjustments to ensure the defender stays within a defensive zone
        adjusted_x = max(midpoint_x, -350)  # Example adjustment
        adjusted_y = self.choose_side_for_strategic_position(ball,players)
        return {'x': adjusted_x, 'y': adjusted_y}
    
    def calculate_offensive_strategic_position(self, ball, players):
        goal_x = -450 #我方不持球,就以球门为目标
        midpoint_x = (ball['x'] + goal_x) / 2
        # Adjustments to ensure the defender stays within a defensive zone
        adjusted_x = max(midpoint_x, -350)  # Example adjustment
        adjusted_y = self.choose_side_for_strategic_position(ball,players)
        return {'x': adjusted_x, 'y': adjusted_y}

    
    def in_strategic_position(self):
        # Check if the defender is in a strategic position
        strategic_x_min, strategic_x_max = 400, 0
        strategic_y_min, strategic_y_max = 100, 100
        return strategic_x_min <= self.x <= strategic_x_max and strategic_y_min <= self.y <= strategic_y_max


    # def is_closest_to_ball(self,ball,players):
    #     own_distance = get_distance({'x': self.x, 'y': self.y}, {'x': ball['x'], 'y': ball['y']})
    #     for player in players:
    #         if player['number'] != self.number:
    #             if get_distance({'x': player['x'], 'y': player['y']}, {'x': ball['x'], 'y': ball['y']}) < own_distance:
    #                 return False
    #     return True
    
    def distance_to_ball_close_enough(self,ball):
        return get_distance({'x': self.x, 'y': self.y}, {'x': ball['x'], 'y': ball['y']}) <= 24
    
    def move_towards_goal(self):
        print("blue forward moves towards goal")
        goal_position = {'x': -448, 'y': 0} #这里得设定的比球门大一点，不然会报错
        direction_to_goal = get_direction({'x': self.x, 'y': self.y}, goal_position)
        return {
            'type': 'move', 
            'player_number': self.number, 
            'destination': goal_position, 
            'direction': direction_to_goal, 
            'speed': 7,
            'has_ball':True
            }

    def move_to_strategic_position(self, strategic_pos):
        # Move to a predefined strategic position
        direction_to_strategic_pos = get_direction({'x': self.x, 'y': self.y}, strategic_pos)
        return {
            'type': 'move',
            'player_number': self.number,
            'destination': strategic_pos,
            'direction': direction_to_strategic_pos,
            'speed': 7,
            'has_ball':False
        }
    
    # def face_ball_direction(self, ball):
    #     direction_to_ball = get_direction({'x': self.x, 'y': self.y}, {'x': ball['x'], 'y': ball['y']})
    #     return {
    #         'type': 'move', 
    #         'player_number': self.number, 
    #         'destination': {'x': self.x, 'y': self.y}, 
    #         'direction': direction_to_ball, 
    #         'speed': 0,
    #         'has_ball':False
    #         }
