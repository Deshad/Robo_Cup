from utils import get_direction, get_distance, is_within_angle_to_ball, reposition_around_ball, is_closest_to_ball
from models.player import Player
import math
class RedDefender(Player):
    def __init__(self, x, y, name, number, color, radius, img=None, ban_cycles=0, role=None, direction=0):
        super().__init__(x, y, name, number, color, radius, img, ban_cycles, role, direction)

    def decide_action(self, ball, players,opponents):
        decisions = []
        # Define the strategic position based on the ball's location and possession status     
        if self.own_half(ball):
            if ball['owner_color'] == self.color:
                if self.owns_ball(ball):
                    print('red_defender owns ball')
                    pass_decision = self.pass_to_teammates(players, opponents)
                    if pass_decision:
                        print("red_defender is passing the ball")
                        if is_within_angle_to_ball(self, ball, pass_decision['direction']):
                            print("Red Defender is passing the ball to teammate")
                            decisions.append(pass_decision)
                        else:
                            print("Red Defender is repositioning around ball")
                            decisions.append(reposition_around_ball(self, ball, pass_decision['direction']))
                    else:
                        direction = get_direction({'x': self.x, 'y': self.y}, {'x': 450, 'y': 0})
                        if is_within_angle_to_ball(self, ball, direction):
                            print("Red Defender is moving towards goal")
                            decisions.append(self.move_towards_goal(ball))
                        else:
                            print("Red Defender is repositioning around ball")
                            decisions.append(reposition_around_ball(self, ball, direction))
                else:
                    #decisions.append(self.move_to_strategic_position(self.calculate_strategic_position(ball,players)))
                    #decisions.append(self.move_to_middle(ball,players))
                    decisions.append(self.move_to_point(ball))
            elif is_closest_to_ball(self, ball, players): 
                print('red_defender is closest to ball and intercepts')
                decisions.append(self.intercept_ball(ball,players))
            else: 
                decisions.append(self.move_to_point(ball))
        #elif self.in_strategic_position():
        #    decisions.append(self.face_ball_direction(ball))
        else:
            #decisions.append(self.move_to_middle(ball,players))
            decisions.append(self.move_to_point(ball))

        return decisions


    def calculate_strategic_position(self, ball, players):
        # Adjusted to dynamically calculate strategic positions
        if self.own_half(ball):
            if ball['owner_color'] == self.color:
                # Offensive positioning when our team possesses the ball
                return self.calculate_offensive_strategic_position(ball, players)
            else:
                # Defensive positioning when the opposing team possesses the ball
                return self.calculate_defensive_strategic_position(ball, players)
        else:
            # Default strategic position when the ball is not on our half
            return self.default_strategic_position()
       

    def default_strategic_position(self):
        # Return a default strategic position based on the side of the field
        return {'x': -300, 'y': 100}  # Example value

    def calculate_defensive_strategic_position(self, ball, players):
        # Calculates defensive strategic position based on the ball's location and potential goal threats
        # Example logic: Positioning based on the midpoint between the ball and the most threatened goalpost
        goal_x = -450 if self.color == 'red' else 450
        goal_y = 0
        midpoint_x = (ball['x'] + goal_x) / 2
        midpoint_y = (ball['y'] + goal_y) / 2
        # Adjustments to ensure the defender stays within a defensive zone
        adjusted_x = max(min(midpoint_x, -300), -350)  # Example adjustment
        adjusted_y = max(min(midpoint_y, 300), -100)
        return {'x': adjusted_x, 'y': adjusted_y}

    def calculate_offensive_strategic_position(self, ball, players):
        # Calculates offensive strategic position to maximize scoring opportunities
        # Example logic: Positioning to support the attacker with the ball or to open up for receiving a pass
        if self.owns_ball(ball):
            return {'x': self.x, 'y': self.y}  # Stay in position if the defender owns the ball
        else:
            # Find a position that supports the attack or prepares for a pass
            supporting_x = min(self.x + 100, 300)  # Example logic to move forward but not too close to the attack
            supporting_y = self.y  # Stay in line with current y position to maintain width
            print({'x': supporting_x, 'y': supporting_y})
            return {'x': supporting_x, 'y': supporting_y}
    
    
    def in_strategic_position(self):
        # Check if the defender is in a strategic position
        strategic_x_min, strategic_x_max = -400, 0
        strategic_y_min, strategic_y_max = -100, 100
        return strategic_x_min <= self.x <= strategic_x_max and strategic_y_min <= self.y <= strategic_y_max

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

    def move_to_middle(self,ball,players):
        for player in players:
            if player['role'] == 'defender' and player['number'] != self.number:
                another_defender = player
        #destination = {'x':(ball['x'] + another_defender['x']) / 2,'y':(ball['y'] + another_defender['y']) / 2}
        if (ball['x'] + another_defender['x']) / 2 > 0:
            destination = {'x':0,'y':(ball['y'] + another_defender['y']) / 2}
        else:
            destination = {'x':(ball['x'] + another_defender['x']) / 2,'y':(ball['y'] + another_defender['y']) / 2}

        return {
            'type': 'move',
            'player_number': self.number,
            'destination': destination,
            'direction': get_direction({'x': self.x, 'y': self.y},destination),
            'speed': 7,  # Adjust speed based on the urgency of repositioning
            'has_ball':False
        }

    def move_to_point(self,ball):
        goal_x = -450 if self.color == 'red' else 450
        goal_y = 130
        if self.number == 1:
            side = {'x':goal_x,'y':goal_y}
        else:
            side = {'x':goal_x,'y':-goal_y}

        destination = {'x':(ball['x'] + side['x']) / 2,'y':(ball['y'] + side['y']) / 2}

        return {
            'type': 'move',
            'player_number': self.number,
            'destination': destination,
            'direction': get_direction({'x': self.x, 'y': self.y},destination),
            'speed': 7,  # Adjust speed based on the urgency of repositioning
            'has_ball':False
        }


    def owns_ball(self, ball):
        return ball['owner_number'] == self.number and ball['owner_color'] == self.color
    

    def get_angle(self,ax,ay,bx,by,cx,cy):
        # b为顶点
        ba = [ax - bx, ay - by]
        bc = [cx - bx, cy - by]
        cosine_angle = (ba[0] * bc[0] + ba[1] * bc[1]) / (math.sqrt(ba[0]**2 + ba[1]**2) * math.sqrt(bc[0]**2 + bc[1]**2))
        angle = math.acos(cosine_angle)
        return math.degrees(angle)

    def pass_to_teammates(self, players, opponents):
        best_teammate = None
        max_angle = -float('inf')

        for player in players:
            if player['role'] == 'forward':
                closest_opponent = None
                min_distance_to_line = float('inf')

                for opponent in opponents:
                    if self.x < opponent['x'] < player['x'] or self.x > opponent['x'] > player['x']:
                        distance_to_line = abs((player['y'] - self.y) * opponent['x'] - (player['x'] - self.x) * opponent['y'] + player['x'] * self.y - player['y'] * self.x) / math.sqrt((player['y'] - self.y)**2 + (player['x'] - self.x)**2)
                        if distance_to_line < min_distance_to_line:
                            min_distance_to_line = distance_to_line
                            closest_opponent = opponent

                if closest_opponent:
                    angle = self.get_angle(player['x'],player['y'],self.x,self.y,opponent['x'],opponent['y'])
                    if angle > max_angle:
                        best_teammate = player
                        max_angle = angle

        if best_teammate:
            direction_to_teammate = get_direction({'x': self.x, 'y': self.y}, {'x': best_teammate['x'], 'y': best_teammate['y']})
            return {
                'type': 'kick',
                'player_number': self.number,
                'direction': direction_to_teammate,
                'power': 50  # Adjust power as necessary
            }
        else:
            return None

    def move_towards_goal(self, ball):
        goal_position = {'x': 0, 'y': 0}
        direction_to_goal = get_direction({'x': self.x, 'y': self.y}, goal_position)
        return {
            'type': 'move', 
            'player_number': self.number, 
            'destination': goal_position, 
            'direction': direction_to_goal, 
            'speed': 7,
            'has_ball':True
        }

    def face_ball_direction(self, ball):
        direction_to_ball = get_direction({'x': self.x, 'y': self.y}, {'x': ball['x'], 'y': ball['y']})
        return {
            'type': 'move', 
            'player_number': self.number, 
            'destination': {'x': self.x, 'y': self.y}, 
            'direction': direction_to_ball,
            'speed': 0,
            'has_ball':False
        }

    def move_to_strategic_position(self, strategic_position):
        strategic_pos = strategic_position
        direction_to_strategic_pos = get_direction({'x': self.x, 'y': self.y}, strategic_pos)
        return {
            'type': 'move', 
            'player_number': self.number, 
            'destination': strategic_pos, 
            'direction': direction_to_strategic_pos, 
            'speed': 7,
            'has_ball':False
        }
    
    def distance_to_ball(self,ball):
        return get_distance({'x': self.x, 'y': self.y}, {'x': ball['x'], 'y': ball['y']})


    # def is_closest_to_ball(self, players, ball):
    #     """Check if this defender is the closest to the ball among all defenders."""
    #     own_distance = get_distance({'x': self.x, 'y': self.y}, {'x': ball['x'], 'y': ball['y']})
    #     #defenders = [players[1],players[2]]
    #     #forwards = [player for player in players if player['role'] == 'forward']
    #     for player in players:
    #         if player['number'] != self.number:
    #             if get_distance({'x': player['x'], 'y': player['y']}, {'x': ball['x'], 'y': ball['y']}) < own_distance:
    #                 return False
    #     return True

    def intercept_ball(self, ball,players):
        """Move towards the ball to intercept it."""
        direction_to_ball = get_direction({'x': self.x, 'y': self.y}, {'x': ball['x'], 'y': ball['y']})
        distance_to_ball = get_distance({'x': self.x, 'y': self.y}, {'x': ball['x'], 'y': ball['y']})
        print('distance_to_ball:',distance_to_ball)
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
            print("red_defender is grabbing ball")
            return self.grab_ball(ball)
    
    def grab_ball(self,ball):
        direction_to_ball = get_direction({'x': self.x, 'y': self.y}, {'x': ball['x'], 'y': ball['y']})
        return {
            'type': 'grab',
            'player_number': self.number,
            'direction': direction_to_ball,
        }
    
    def own_half(self,ball):
        if self.color == 'red':
            x = ball['x']
            x1 = -450
            x2 = 0
        elif self.color == 'blue':
            x = ball['x']
            x1 = 0
            x2 = 450
        else:
            print("错误的后卫属性")
        return x1 <= x <= x2