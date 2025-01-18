from utils import get_direction, get_distance, is_within_angle_to_ball, reposition_around_ball, is_closest_to_ball
from models.player import Player


class BlueFlexible(Player):
    def __init__(self, x, y, name, number, color, radius, img=None, ban_cycles=0, role=None, direction=0):
        super().__init__(x, y, name, number, color, radius, img, ban_cycles, role, direction)

    def decide_action(self, ball, players):
        decisions = []
        strategic_position = self.calculate_strategic_position(ball, players)
        if self.own_half(ball):  # For blue team, the own half is the positive x 
            if ball['owner_color'] == self.color:
                if self.owns_ball(ball): 
                    print('blue flexible own ball')
                    pass_decision = self.pass_to_teammates(players, ball)
                    if pass_decision:
                        if is_within_angle_to_ball(self, ball, pass_decision['direction']):
                            print("blue flexible facing ball and pass to teammates")
                            decisions.append(pass_decision)
                        else:
                            decisions.append(reposition_around_ball(self, ball, pass_decision['direction']))
                    else:
                        direction = get_direction({'x': self.x, 'y': self.y}, {'x': -450, 'y': 0})
                        if is_within_angle_to_ball(self, ball, direction):
                            print("blue flexible facing ball and move towards goal")
                            decisions.append(self.move_towards_goal(ball))
                        else:
                            decisions.append(reposition_around_ball(self, ball, direction))
                else: #这个move_to_strategic_position
                    decisions.append(self.move_to_strategic_position(strategic_position))
            else:
                if is_closest_to_ball(self, ball, players): 
                    decisions.append(self.intercept_ball(ball, players))
                else:
                    decisions.append(self.move_to_strategic_position(strategic_position))
        elif is_closest_to_ball(self,ball,players):
            print('blue flexible is most closet')
            if ball['owner_color'] == self.color:
                if self.owns_ball(ball):
                    pass_decision = self.pass_to_teammates(players, ball)
                    if pass_decision:
                        if is_within_angle_to_ball(self, ball, pass_decision['direction']):
                            print("blue flexible facing ball")
                            decisions.append(pass_decision)
                        else:
                            print("blue flexible reposition around ball")
                            decisions.append(reposition_around_ball(self, ball, pass_decision['direction']))
                    else:
                        direction = get_direction({'x': self.x, 'y': self.y}, {'x': -450, 'y': 0})
                        if is_within_angle_to_ball(self, ball, direction):
                            print("blue flexible facing ball")
                            decisions.append(self.move_towards_goal(ball))
                        else:
                            print("blue flexible reposition around ball")
                            decisions.append(reposition_around_ball(self, ball, direction))
            else:
                decisions.append(self.intercept_ball(ball,players))
        else:
            decisions.append(self.move_to_strategic_position(strategic_position))
            # # print('球不在我方半场，进入了分支')
            # if not self.in_strategic_position():
                # decisions.append(self.move_to_strategic_position(strategic_position))
            # else:
            #     decisions.append(self.face_ball_direction(ball)) #行吧，这里有问题，这里会一直背对着球，这显然不合适

        return decisions

    def calculate_strategic_position(self, ball, players):
        # goal_x = 450
        # midpoint_x = (ball['x'] + goal_x) / 2
        # adjusted_x = min(midpoint_x, 350)  # Example adjustment

        # adjusted_y = self.choose_side_for_strategic_position(ball,players) #返回一侧的，
        
        # return {'x': adjusted_x, 'y': adjusted_y}
        return {'x': 350, 'y': -150} if self.number == 1 else {'x': 350, 'y': 150}

        
    # def choose_side_for_strategic_position(self,ball,players):
    #     other_defender = [player for player in players if player['role'] == 'defender' and player['number'] != self.number][0]
    #     other_defender_y = other_defender['y']
    #     other_forward_has_ball = ball['owner_color'] == self.color and ball['owner_number'] != other_defender['number']
    #     goalpost_y_left = -50
    #     goalpost_y_right = 50
    #     strategic_y_left = (ball['y'] + goalpost_y_left) // 2
    #     strategic_y_right = (ball['y'] + goalpost_y_right) // 2

    #     if other_forward_has_ball:#如果队友持球,我去另侧
    #         if other_defender_y < 0:
    #             return strategic_y_right
    #         else:
    #             return strategic_y_left
    #     else:# 如果队友也不持球
    #         if (self.y < 0 and other_defender_y >= 0) or (self.y >= 0 and other_defender_y < 0):# 如果我们在场地的不同侧，选择离自己近的侧翼
    #             return strategic_y_left if self.y < 0 else strategic_y_right
    #         else:# 如果我们在同一侧，选择离两人都较远但相对离自己更近的侧翼
    #             if self.y > other_defender_y: 
    #                 return strategic_y_right
    #             else:
    #                 return strategic_y_left

    # def in_strategic_position(self):
    #     # Adjust for blue team's strategic positioning checks
    #     strategic_x_min, strategic_x_max = 0, 400  # Adjusted range for blue team
    #     strategic_y_min, strategic_y_max = -100, 100
    #     return strategic_x_min <= self.x <= strategic_x_max and strategic_y_min <= self.y <= strategic_y_max


    # def move_to_middle(self,ball,players):
    #     for player in players:
    #         if player['role'] == 'defender' and player['number'] != self.number:
    #             another_defender = player
    #     destination = {'x':(ball['x'] + another_defender['x']) / 2,'y':(ball['y'] + another_defender['y']) / 2}
    #     return {
    #         'type': 'move',
    #         'player_number': self.number,
    #         'destination': destination,
    #         'direction': get_direction({'x': self.x, 'y': self.y},destination),
    #         'speed': 7,  # Adjust speed based on the urgency of repositioning
    #         'has_ball':False
    #     }

    def owns_ball(self, ball):
        return ball['owner_number'] == self.number and ball['owner_color'] == self.color
    
    def pass_to_teammates(self, players, ball):
        most_advanced_teammate = None
        max_advance_x = float('inf')  # Initialize with a very small number

        for player in players:
            if player['number'] != self.number and player['role'] != 'goalkeeper':
                # Check if this player is more advanced towards the opponent's goal
                if player['x'] < max_advance_x:
                    most_advanced_teammate = player
                    max_advance_x = player['x']
        
        if most_advanced_teammate:
            direction_to_teammate = get_direction({'x': self.x, 'y': self.y}, {'x': most_advanced_teammate['x'], 'y': most_advanced_teammate['y']})
            return {
                'type': 'kick',
                'player_number': self.number,
                'direction': direction_to_teammate,
                'power': 50,  # Adjust power as necessary
            }
        else:
            return None

    def move_towards_goal(self, ball):
        print('blue flexible move towards goal')
        if self.color == 'red':
            goal_position = {'x': 450, 'y': 0}
        else:
            goal_position = {'x': -450, 'y': 0}
        direction_to_goal = get_direction({'x': self.x, 'y': self.y}, goal_position)
        return {
            'type': 'move', 
            'player_number': self.number, 
            'destination': goal_position, 
            'direction': direction_to_goal, 
            'speed': 7,
            'has_ball':True
        }

    # def face_ball_direction(self, ball):
    #     direction_to_ball = get_direction({'x': self.x, 'y': self.y}, {'x': ball['x'], 'y': ball['y']})
    #     return {
    #         'type': 'move', 
    #         'player_number': self.number, 
    #         'destination': {'x': self.x, 'y': self.y}, 
    #         'direction': direction_to_ball,
    #         'speed': 1,
    #         'has_ball':False
    #     }

    # Example method to adjust for new strategic positioning
    def move_to_strategic_position(self, strategic_pos):
        direction_to_strategic_pos = get_direction({'x': self.x, 'y': self.y}, strategic_pos)
        return {
            'type': 'move',
            'player_number': self.number,
            'destination': strategic_pos,
            'direction': direction_to_strategic_pos,
            'speed': 7,  # Adjust speed based on the urgency of repositioning
            'has_ball':False
        }
    
    # def is_most_closet(self,ball,players):
    #     own_distance = get_distance({'x': self.x, 'y': self.y}, {'x': ball['x'], 'y': ball['y']})
    #     for player in players:
    #         if player['number'] != self.number:
    #             if get_distance({'x': player['x'], 'y': player['y']}, {'x': ball['x'], 'y': ball['y']}) < own_distance:
    #                 return False
    #     return True

    # def is_closest_to_ball(self, players, ball):
    #     """Check if this forward is the closest to the ball among two forwards."""
    #     own_distance = get_distance({'x': self.x, 'y': self.y}, {'x': ball['x'], 'y': ball['y']})
    #     other_denfender = [player for player in players if player['role'] == 'defender' and player['number'] != self.number][0]
    #     other_distance = get_distance({'x': other_denfender['x'], 'y': other_denfender['y']}, {'x': ball['x'], 'y': ball['y']})
    #     return own_distance < other_distance

    def intercept_ball(self, ball,players):
        """Move towards the ball to intercept it."""
        direction_to_ball = get_direction({'x': self.x, 'y': self.y}, {'x': ball['x'], 'y': ball['y']})
        distance_to_ball = get_distance({'x': self.x, 'y': self.y}, {'x': ball['x'], 'y': ball['y']})
        if distance_to_ball > 24:
            if ball['owner_color'] == self.color:
                speed = 5
                destination = self.calculate_strategic_position(ball,players)
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
    
    def own_half(self,ball):
        # print('难道此时没进入？',ball['x'])
        x = ball['x']
        x1 = 0
        x2 = 450
        return x1 < x < x2